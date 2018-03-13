from sqlalchemy import create_engine, pool
from auditorium import config
from sqlalchemy.orm import sessionmaker
from auditorium.db.models import Base


class DBSession:
    """
    Session class
    """
    def __init__(self):
        """
        Constructor
        """
        engine = create_engine(config.DB_CONNECTION, poolclass=pool.NullPool)
        Base.metadata.bind = engine

        self.session = sessionmaker(bind=engine)()

    def __enter__(self):
        """
        Return DB session
        :return:
        """
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close DB connection
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.session.close()
