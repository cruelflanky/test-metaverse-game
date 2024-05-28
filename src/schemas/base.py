import datetime
import typing

import pydantic

from src.utilities.formatters.datetime_formatter import format_datetime_into_isoformat
from src.utilities.formatters.field_formatter import format_dict_key_to_camel_case


class BaseSchemaModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        from_attributes: bool = True
        populate_by_name: bool = True
        validate_assignment: bool = True
        json_encoders: dict = {datetime.datetime: format_datetime_into_isoformat}
        alias_generator: typing.Any = format_dict_key_to_camel_case
