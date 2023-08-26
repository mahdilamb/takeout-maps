import datetime
from typing import TypeVar

import pydantic
from loguru import logger
from sqlalchemy import and_, column, func, select, union_all
from sqlalchemy.orm import Session

from takeout_maps.api.takeout import records, semantic_location_history
from takeout_maps.takeout import index, models, utils

BaseModel = TypeVar("BaseModel", bound=pydantic.BaseModel)


def validate_json_with_id(model: type[BaseModel]):
    def wrapper(json_data: str, id: int, *args, **kwargs) -> BaseModel:
        validated = model.model_validate_json(json_data, *args, **kwargs)
        validated.id = id
        return validated

    return wrapper


@index.requires_records
@index.inject_session()
def records_by_date(session: Session, date: datetime.date) -> records.Records:
    """Get all the records for a date."""
    next_date = date + datetime.timedelta(days=1)
    try:
        db_result = (
            session.query(models.Record)
            .filter(
                and_(
                    models.Record.timestamp >= date,
                    models.Record.timestamp <= next_date,
                ),
            )
            .order_by(models.Record.timestamp)
            .with_entities(models.Record.id, models.Record.json)
            .all()
        )
        return records.Records(
            locations=tuple(
                validate_json_with_id(records.Location)(json_data=json[1], id=json[0])
                for json in db_result
            )
        )
    except Exception as e:
        logger.exception(e)
        return records.Records(locations=())


@index.requires_records
@index.inject_session()
def records_by_range(
    session: Session,
    start: datetime.datetime,
    end: datetime.datetime | datetime.timedelta,
):
    """Get all the records from a date range."""
    if isinstance(end, datetime.timedelta):
        end = start + end
    start, end = sorted((start, end))
    try:
        db_result = (
            session.query(models.Record)
            .filter(
                and_(
                    models.Record.timestamp >= start,
                    models.Record.timestamp < end,
                ),
            )
            .order_by(models.Record.timestamp)
            .with_entities(models.Record.id, models.Record.json)
            .all()
        )
        return records.Records(
            locations=tuple(
                validate_json_with_id(records.Location)(json[1], json[0])
                for json in db_result
            )
        )
    except Exception as e:
        logger.exception(e)
        return records.Records(locations=())


@index.requires_semantic_location_history
@index.inject_session()
def semantic_location_history_by_date(
    session: Session, date: datetime.date
) -> semantic_location_history.SemanticLocationHistory:
    """Get the semantic location history for a date."""
    table = models.semantic_location_histories[(date.year, date.month)]
    next_date = date + datetime.timedelta(days=1)
    db_result = (
        session.query(table)
        .filter(
            and_(
                table.end_timestamp >= date,
                table.start_timestamp < next_date,
            ),
        )
        .order_by(table.start_timestamp)
        .with_entities(table.id, table.json)
        .all()
    )
    return semantic_location_history.SemanticLocationHistory(
        timelineObjects=tuple(
            validate_json_with_id(semantic_location_history.TimelineObject)(
                json[1], json[0]
            )
            for json in db_result
        )
    )


@index.requires_semantic_location_history
@index.inject_session()
def semantic_location_history_by_range(
    session: Session,
    start: datetime.datetime,
    end: datetime.datetime | datetime.timedelta,
) -> semantic_location_history.SemanticLocationHistory:
    """Get the semantic location history for a timestamp range."""
    if isinstance(end, datetime.timedelta):
        end = start + end
    start, end = sorted((start, end))

    tables = [
        models.semantic_location_histories[date] for date in utils.months(start, end)
    ]

    histories = union_all(
        *[
            select(*[column(col.name) for col in tables[0].__table__.c]).select_from(
                table
            )
            for table in tables
        ]
    ).subquery("histories")
    db_result = (
        session.query(histories)
        .filter(column("id") == 1)
        .order_by(column("start_timestamp"))
        .with_entities(histories.c.id, histories.c.json)
        .all()
    )
    return semantic_location_history.SemanticLocationHistory(
        timelineObjects=tuple(
            validate_json_with_id(semantic_location_history.TimelineObject)(
                json[1], json[0]
            )
            for json in db_result
        )
    )


@utils.local_cache
@index.requires_records
@index.inject_session()
def records_range(session) -> tuple[datetime.datetime, datetime.datetime]:
    """Get the first and last timestamp for the records."""
    return session.query(
        func.min(models.Record.timestamp), func.max(models.Record.timestamp)
    ).first()
