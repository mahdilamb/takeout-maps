"""SQLALchemy models for the indexer."""
import datetime
from types import MappingProxyType
from typing import Mapping

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from takeout_maps.takeout import paths, utils

Base = declarative_base()


class Completed(Base):
    """Table storing information about files that have been indexed."""

    __tablename__ = "completed_tables"
    table_name: Mapped[str] = mapped_column(primary_key=True)
    completed_on: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(), nullable=False
    )


class Record(Base):
    """Table for the Records.json file."""

    __tablename__ = utils.table_name(paths.records_path)
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(index=True)
    json: Mapped[str] = mapped_column()

    def __str__(self) -> str:
        return f"Record ({self.id}) at {self.timestamp}"

    def __repr__(self) -> str:
        return f"<{self.id}>@{self.timestamp}"


class SemanticLocationHistory(Base):
    """Mixin for the SemanticLocationHistory files."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    start_timestamp: Mapped[datetime.datetime] = mapped_column(index=True)
    end_timestamp: Mapped[datetime.datetime] = mapped_column(index=True)
    json: Mapped[str] = mapped_column()


@utils.local_cache
def semantic_location_histories() -> (
    Mapping[tuple[int, int], type[SemanticLocationHistory]]
):
    """Get a mapping of the dates for semantic location history to the models."""
    return MappingProxyType(
        {
            utils.semantic_location_history_to_date(path): type(
                f"{SemanticLocationHistory.__name__}{''.join(list(str(el) for el in utils.semantic_location_history_to_date(path)))}",
                (SemanticLocationHistory,),
                {"__tablename__": utils.table_name(path)},
            )
            for path in paths.semantic_location_histories
        }
    )
