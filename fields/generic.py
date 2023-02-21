from .base_field import BaseField
from copy import deepcopy


class BoolField(BaseField):
    data_schema = {
        "$id": "/generic/boolean",
        "title": "BoolField",
        "description": "Bool field in dsdl.",
        "oneOf": [
            {"type": "boolean"},
            {"enum": [0, 1]}
        ]
    }


class IntField(BaseField):
    data_schema = {
        "$id": "/generic/int",
        "title": "IntField",
        "description": "Int field in dsdl.",
        "type": "integer",
    }


class NumField(BaseField):
    data_schema = {
        "$id": "/generic/num",
        "title": "NumField",
        "description": "Num field in dsdl.",
        "type": "number",
    }


class StrField(BaseField):
    data_schema = {
        "$id": "/generic/str",
        "title": "StrField",
        "description": "Str field in dsdl.",
        "type": "string",
    }


class DictField(BaseField):
    data_schema = {
        "$id": "/generic/dict",
        "title": "DictField",
        "description": "Dict field in dsdl.",
        "type": "object",
    }


class ListField(BaseField):
    data_schema = {
        "$id": "/generic/list",
        "title": "ListField",
        "description": "List field in dsdl.",
        "type": "array",
        "items": {}
    }

    args_schema = {
        "type": "object",
        "properties": {
            "ele_type": {"type": "object"}
        },
        "minProperties": 1,
        "maxProperties": 1,
        "required": ["ele_type"]
    }

    @classmethod
    def get_field(cls, **kwargs):
        schema = deepcopy(cls.data_schema)
        kwargs = deepcopy(kwargs)
        cls.validate_schema(kwargs, cls.args_schema)
        ele_type = kwargs["ele_type"]
        if callable(ele_type):
            ele_type = ele_type()
        schema["items"] = ele_type
        return schema
