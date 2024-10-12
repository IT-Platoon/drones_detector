from uuid import uuid4

from app.config.default import DefaultSettings


class TestSettings(DefaultSettings):
    """
    Test configs for application.
    """

    POSTGRES_DB = ".".join([uuid4().hex, "pytest"])
