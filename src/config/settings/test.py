from src.config.settings.base import Environment, Settings


class TestSettings(Settings):
    DESCRIPTION: str | None = "Test Environment."
    ENVIRONMENT: Environment = Environment.TEST
