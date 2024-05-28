import os
from functools import lru_cache

from src.config.settings.base import Settings
from src.config.settings.prod import ProdSettings
from src.config.settings.test import TestSettings


class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> Settings:
        if self.environment == "TEST":
            return TestSettings()
        return ProdSettings()


@lru_cache()
def get_settings() -> Settings:
    return BackendSettingsFactory(environment=os.getenv("ENVIRONMENT", default="TEST"))()


settings: Settings = get_settings()
