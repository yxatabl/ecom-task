from src.commons.postgres import database
from src.commons.unit_of_work import UnitOfWork


def get_uow() -> UnitOfWork:
    return UnitOfWork(database)