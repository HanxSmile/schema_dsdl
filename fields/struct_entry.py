class StructSchema:

    def __init__(self):
        self.schema = {
            "title": "Struct",
            "type": "object",
            "properties": {},
            "required": []
        }

    def add_property(self, name, prop, required=False):
        prop = prop.copy()
        self.schema["properties"][name] = prop
        if required:
            self.schema["required"].append(name)

    def __call__(self):
        return self.schema


class StructMetaclass(type):
    def __new__(mcs, name, bases, attributes):

        super_new = super().__new__
        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, StructMetaclass)]
        if not parents:
            return super_new(mcs, name, bases, attributes)

        _params_name = attributes.pop("__params__", [])
        params = {_: DomainPlaceholder() for _ in _params_name}
        _fields = attributes.pop("__fields__ ", {})
        _required_fields_name = attributes.pop("__optional__", [])

        for k, v in _fields:
            if isin

        required = dict()  # 所有必须填写的field对象
        optional = dict()  # 所有可不填写的field对象
        mappings = dict()  # 所有的field对象
        struct_mappings = dict()  # 所有的Struct对象

        for k, v in attributes.items():
            if isinstance(v, Field):
                mappings[k] = v
                if v.is_optional:
                    optional[k] = v
                else:
                    required[k] = v
            elif isinstance(v, Struct):
                struct_mappings[k] = v

        for k in required.keys():
            attributes.pop(k)
        for k in optional.keys():
            attributes.pop(k)
        for k in struct_mappings.keys():
            attributes.pop(k)

        attributes["__required__"] = required
        attributes["__optional__"] = optional
        attributes["__mappings__"] = mappings
        attributes["__struct_mappings__"] = struct_mappings

        new_class = super_new(mcs, name, bases, attributes)
        STRUCT.register(name, new_class)
        return new_class


class Struct:
    pass
