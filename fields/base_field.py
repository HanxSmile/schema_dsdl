from copy import deepcopy
from jsonschema import validate, FormatChecker
from geometry import GEOMETRY


class BaseField:
    data_schema = {}
    args_schema = {
        "type": "object",
        "minProperties": 0,
        "maxProperties": 0,
    }
    default_args = {}
    geometry_class = None

    @classmethod
    def get_field(cls, **kwargs):
        schema = deepcopy(cls.data_schema)
        default_args = deepcopy(cls.default_args)
        default_args.update(kwargs)

        if default_args:
            cls.validate_schema(default_args, cls.args_schema)
            schema["dsdl_args"] = default_args
        return schema

    @staticmethod
    def validate_schema(data, schema):
        validate(data, schema, format_checker=FormatChecker())

    @classmethod
    def validate(cls, value, **kwargs):
        if cls.geometry_class is None:
            return value
        if cls.geometry_class.__class__.__name__ == "GeometryMeta":
            return cls.geometry_class(value, **kwargs)
        return GEOMETRY.get(cls.geometry_class)(value, **kwargs)
