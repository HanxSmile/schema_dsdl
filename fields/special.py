from .base_field import BaseField
from geometry import Polygon as Polygon_, PolygonItem as PolygonItem_


class CoordField(BaseField):
    data_schema = {
        "$id": "/special/coord",
        "title": "CoordField",
        "description": "Coord 2D field in dsdl.",
        "type": "array",
        "items": {
            "type": "number",
        },
        "minItems": 2,
        "maxItems": 2
    }


class Coord3DField(BaseField):
    data_schema = {
        "$id": "/special/coord3d",
        "title": "Coord3DField",
        "description": "Coord 3D field in dsdl.",
        "type": "array",
        "items": {
            "type": "number",
        },
        "minItems": 3,
        "maxItems": 3
    }


class IntervalField(BaseField):
    data_schema = {  # 无法定义顺序
        "$id": "/special/interval",
        "title": "IntervalField",
        "description": "Interval field in dsdl.",
        "type": "array",
        "items": {
            "type": "number",
        },
        "minItems": 2,
        "maxItems": 2,
    }


class BBoxField(BaseField):
    data_schema = {
        "$id": "/special/bbox",
        "title": "BBoxField",
        "description": "Bounding box field in dsdl.",
        "type": "array",
        "items": [
            {"type": "number"},
            {"type": "number"},
            {"type": "number", "minimum": 0.},
            {"type": "number", "minimum": 0.},
        ],
        "minItems": 4,
        "maxItems": 4,
    }

    geometry_class = "BBox"


class RotatedBBoxField(BaseField):
    default_args = {
        "mode": "xywht",
        "measure": "radian"
    }

    data_schema = {
        "$id": "/special/rotatedbbox",
        "title": "RotatedBBoxField",
        "description": "Rotated bounding box field in dsdl.",
        "type": "array",
        "oneOf": [
            {"minItems": 5, "maxItems": 5,
             "items": [{"type": "number"}, {"type": "number"}, {"type": "number", "minimum": 0},
                       {"type": "number", "minimum": 0}, {"type": "number"}]},
            {"minItems": 8, "maxItems": 8, "items": {"type": "number"}}
        ]
    }

    args_schema = {
        "type": "object",
        "properties": {
            "measure": {"enum": ["radian", "degree"]},
            "mode": {"enum": ["xywht", "xyxy"]}
        },
        "minProperties": 2,
        "maxProperties": 2,
        "required": ["measure", "mode"]
    }


class PolygonField(BaseField):
    data_schema = {
        "$id": "/special/polygon",
        "title": "PolygonField",
        "description": "Polygon field in dsdl.",
        "type": "array",
        "items": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "number"},
                "minItems": 2,
                "maxItems": 2,
            }
        }
    }

    @classmethod
    def validate(cls, value, **kwargs):
        polygon_lst = []
        for idx, points in enumerate(value):
            polygon_lst.append(PolygonItem_(points))
        return Polygon_(polygon_lst)


class LabelField(BaseField):
    data_schema = {
        "$id": "/special/label",
        "title": "LabelField",
        "description": "Label field in dsdl.",
        "type": ["string", "integer"]
    }
    args_schema = {
        "type": "object",
        "properties": {
            "dom": {"type": "string"}
        },
        "minProperties": 1,
        "maxProperties": 1,
        "required": ["dom"]
    }

    @classmethod
    def validate(cls, value, **kwargs):
        pass  # TODO


class KeypointField(BaseField):
    data_schema = {
        "$id": "/special/keypoint",
        "title": "KeypointField",
        "description": "Keypoint Field in dsdl.",
        "type": "array",
        "items": {
            "type": "array",
            "items": {
                "type": "number"
            },
            "minItems": 3,
            "maxItems": 3,
        }
    }

    args_schema = {
        "type": "object",
        "properties": {
            "dom": {"type": "string"}
        },
        "minProperties": 1,
        "maxProperties": 1,
        "required": ["dom"]
    }


class TextField(BaseField):
    data_schema = {
        "$id": "/special/text",
        "title": "TextField",
        "description": "Text field in dsdl.",
        "type": "string"
    }


class ImageShapeField(BaseField):
    default_args = {"mode": "hw"}

    data_schema = {
        "$id": "/special/imageshape",
        "title": "ImageShapeField",
        "description": "ImageShape field in dsdl.",
        "type": "array",
        "items": {"type": "integer"},
        "minItems": 2,
        "maxItems": 2,
    }

    args_schema = {
        "type": "object",
        "properties": {
            "mode": {"enum": ["hw", "wh"]}
        },
        "minProperties": 1,
        "maxProperties": 1,
        "required": ["mode"]
    }


class InstanceIDField(BaseField):
    data_schema = {
        "$id": "/special/instanceid",
        "title": "TextField",
        "description": "InstanceID field in dsdl.",
        "type": "string"
    }


class UniqueIDField(BaseField):
    default_args = {"id_type": None}
    data_schema = {
        "$id": "/special/uniqueid",
        "title": "UniqueIDField",
        "description": "InstanceID field in dsdl.",
        "type": "string"
    }
    args_schema = {
        "type": "object",
        "properties": {
            "id_type": {"type": ["string", "null"]}
        },
        "minProperties": 1,
        "maxProperties": 1,
        "required": ["id_type"]
    }


class DateField(BaseField):
    data_schema = {
        "$id": "/special/date",
        "title": "DateField",
        "description": "Date field in dsdl.",
        "type": "string",
        "format": "date"
    }


class TimeField(BaseField):
    data_schema = {
        "$id": "/special/time",
        "title": "TimeField",
        "description": "Time field in dsdl.",
        "type": "string",
        "format": "time"
    }
