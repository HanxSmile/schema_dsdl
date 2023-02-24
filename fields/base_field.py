from copy import deepcopy
from jsonschema import validate, FormatChecker
from geometry import GEOMETRY, CLASSDOMAIN, PlaceHolder
from .struct_entry import Struct
from typing import Union, List


class BaseField:
    data_schema = {}
    args_schema = {
        "type": "object",
        "minProperties": 0,
        "maxProperties": 0,
    }
    default_args = {}
    geometry_class = None

    def __init__(self, **kwargs):
        all_kwargs = deepcopy(self.default_args)
        all_kwargs.update(kwargs)
        self.validate_schema(all_kwargs, self.args_schema)
        self.kwargs = all_kwargs

    @classmethod
    def get_schema(cls, **kwargs):
        schema = deepcopy(cls.data_schema)
        default_args = deepcopy(cls.default_args)
        default_args.update(kwargs)

        cls.validate_schema(default_args, cls.args_schema)
        schema["dsdl_args"] = default_args
        return schema

    @staticmethod
    def validate_schema(data, schema):
        validate(data, schema, format_checker=FormatChecker())

    def validate(self, value):
        self.validate_schema(value, self.data_schema)
        if self.geometry_class is None:
            return value
        if self.geometry_class.__class__.__name__ == "GeometryMeta":
            return self.geometry_class(value, **self.kwargs)
        return GEOMETRY.get(self.geometry_class)(value, **self.kwargs)

    @classmethod
    def extract_key(cls):
        field_cls_name = cls.__name__
        return "$" + field_cls_name.lower()


class BaseFieldWithDomain(BaseField):

    _single_dom_schema = {"oneOf": [
        {"enum": CLASSDOMAIN.names_contained()},
        {"type": "string", "pattern": "^\$[a-zA-Z_]\w*$"}
    ]}

    dom_schema = {
        "type": "object",
        "properties": {
            "dom":
                {"oneOf": [
                    _single_dom_schema,
                    {"type": "array", "items": _single_dom_schema}
                ]}
        },
        "minProperties": 1,
        "maxProperties": 1,
        "required": ["dom"]
    }



    def __init__(self, dom: Union[str, List[str]], **kwargs):
        super().__init__(**kwargs)
        self.namespace = None
        if isinstance(dom, list):
            dom =
        if dom.startswith(self.PLACEHOLDER_PREFIX):
            self.dom = PlaceHolder(dom)
        else:
            self.validate_schema(data=dom, schema=self.dom_schema)
            self.dom = dom

    def set_namespace(self, struct: Struct):
        self.namespace = struct

    def validate(self, value):
        if self.namespace is not None:

        self.validate_schema(value, self.data_schema)
        if self.geometry_class is None:
            return value
        if self.geometry_class.__class__.__name__ == "GeometryMeta":
            return self.geometry_class(value, dom=self.dom, **self.kwargs)
        return GEOMETRY.get(self.geometry_class)(value, dom=self.dom, **self.kwargs)


class List(BaseField):
    data_schema = {
        "$id": "/generic/list",
        "title": "ListField",
        "description": "List field in dsdl.",
        "type": "array",
        "items": {}
    }

    default_args = {"ordered": False}

    args_schema = {
        "type": "object",
        "properties": {
            "ele_type": {"type": "object"},
            "ordered": {"type": "boolean"}
        },
        "minProperties": 2,
        "maxProperties": 2,
        "required": ["ordered"]
    }

    def __init__(self, **kwargs):
        all_kwargs = deepcopy(self.default_args)
        all_kwargs.update(kwargs)
        self.validate_schema(all_kwargs, self.args_schema)
        self.kwargs = all_kwargs

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
