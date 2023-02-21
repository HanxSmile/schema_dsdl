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


def Struct(**schema):
    optional = schema.pop("$optional", [])
    struct = StructSchema()
    for name, prop in schema.items():
        if callable(prop):
            prop = prop()
        struct.add_property(name, prop, name not in optional)
    return struct()
