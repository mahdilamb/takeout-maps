"""Module for indexing takeout."""
import datetime
import functools
import io
import json
from decimal import Decimal
from typing import Callable, Concatenate, ParamSpec, TypeVar

import ijson
import sqlalchemy
import tqdm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import takeout_maps.constants
from takeout_maps.takeout import models, paths

P = ParamSpec("P")
T = TypeVar("T")


def inject_session(**engine_kwargs):
    """Decorate a function that requires the indexes."""
    engine = functools.cache(create_engine)(
        takeout_maps.constants.SQLALCHEMY_URL, **engine_kwargs
    )
    models.Completed.__table__.create(bind=engine, checkfirst=True)

    def outer(fn: Callable[Concatenate[Session, P], T]) -> Callable[P, T]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            with Session(engine) as session:
                return fn(session, *args, **kwargs)

        return wrapper

    return outer


@inject_session()
def completed(session, table: type[models.Base]) -> bool:
    """Check if an index has been completed."""
    return (
        sqlalchemy.inspect(session.bind).has_table(models.Completed.__tablename__)
        and session.query(
            session.query(models.Completed)
            .filter(
                models.Completed.table_name == table.__tablename__,
                models.Completed.completed_on != None,
            )
            .exists()
        ).scalar()
    )


@inject_session()
def _create_index(
    session: Session,
    src_file: str,
    table: type[models.Base],
    json_array: str,
    fields: Callable[[dict], dict],
    refresh_every: int = 1000,
):
    """Create an index for a file."""
    table.__table__.create(bind=session.bind, checkfirst=True)

    def decimal_encoder(o):
        if isinstance(o, Decimal):
            return float(o)
        raise TypeError(repr(o) + " is not JSON serializable")

    if not completed(table):
        i = session.query(table).count()
        try:
            with open(src_file, "r") as fp:
                fp.seek(0, io.SEEK_END)
                end = fp.tell()
                fp.seek(0)
                progress = tqdm.tqdm(total=end, desc=f"Indexing {table.__name__}...")
                parser = ijson.items(fp, json_array + ".item")
                for j, o in enumerate(parser):
                    if j % refresh_every == 0:
                        progress.update(fp.tell() - progress.n)
                    if j < i:
                        continue
                    session.add(
                        table(
                            id=j,
                            json=json.dumps(o, default=decimal_encoder),
                            **fields(o),
                        )
                    )

                    if j % refresh_every == 0:
                        session.commit()
            session.add(models.Completed(table_name=table.__tablename__))
            session.commit()
        finally:
            session.commit()


def requires_records(fn: Callable[P, T]) -> Callable[P, T]:
    """Decorate a function tha requires the records."""
    _create_index(
        paths.records_path,
        models.Record,
        "locations",
        fields=lambda data: dict(
            timestamp=datetime.datetime.fromisoformat(data["timestamp"])
        ),
    )

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return fn(*args, **kwargs)

    return wrapper


def requires_semantic_location_history(fn: Callable[P, T]) -> Callable[P, T]:
    """Decorate a function tha requires the semantic location history."""
    for date, table in models.semantic_location_histories.items():
        _create_index(
            paths.semantic_location_history(*date),
            table,
            "timelineObjects",
            fields=lambda data: dict(
                start_timestamp=datetime.datetime.fromisoformat(
                    data.get("activitySegment", data.get("placeVisit"))["duration"][
                        "startTimestamp"
                    ]
                ),
                end_timestamp=datetime.datetime.fromisoformat(
                    data.get("activitySegment", data.get("placeVisit"))["duration"][
                        "endTimestamp"
                    ]
                ),
            ),
        )

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return fn(*args, **kwargs)

    return wrapper
