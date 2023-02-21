from .base_field import BaseField


class ImageField(BaseField):
    default_args = {"reader": None}

    data_schema = {
        "$id": "/unstructure/image",
        "title": "ImageField",
        "description": "Image field in dsdl.",
        "type": "string",
    }

    args_schema = {
        "type": "object",
        "properties": {
            "reader": {"type": ["string", "null"]}
        },
        "minProperties": 1,
        "maxProperties": 1,
        "required": ["reader"]
    }


class LabelMapField(BaseField):
    default_args = {"reader": None}

    data_schema = {
        "$id": "/unstructure/labelmap",
        "title": "LabelMapField",
        "description": "LabelMap field in dsdl.",
        "type": "string",
    }

    args_schema = {
        "type": "object",
        "properties": {
            "reader": {"type": ["string", "null"]}
        },
        "minProperties": 1,
        "maxProperties": 1,
        "required": ["reader"]
    }


class InstanceMapField(BaseField):
    default_args = {"reader": None}

    data_schema = {
        "$id": "/unstructure/instancemap",
        "title": "InstanceMapField",
        "description": "InstanceMap field in dsdl.",
        "type": "string",
    }

    args_schema = {
        "type": "object",
        "properties": {
            "reader": {"type": ["string", "null"]}
        },
        "minProperties": 1,
        "maxProperties": 1,
        "required": ["reader"]
    }
