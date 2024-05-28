from src.config.settings.base import Environment, Settings


class ProdSettings(Settings):
    DESCRIPTION: str | None = "Production Environment."
    ENVIRONMENT: Environment = Environment.PROD
