from fields import *
from jsonschema import validate, FormatChecker

Label_ = LabelStruct(
    uid=UniqueID,
    name=Str,
    color=List(Int),
)

coco_classdomain = ClassDomain(
    name="coco",
    label_type=Label_,
    classes=["dog", "cat", "mouse"],
    skeleton=[[1, 2], [2, 3]]
)

ImageMedia = Struct(
    image=Image,
    image_shape=ImageShape(mode="hw"),
    depth=Int,
    folder=Str,
    source=Dict,
    owner=Dict,
    segmented=Bool
)

LocalObjectEntry = Struct(
    bbox=BBox,
    category=Label(dom="coco"),
    pose=Str,
    truncated=Bool,
    difficult=Bool
)

ObjectDetectionSample = Struct(
    media=ImageMedia,
    objects=List(ele_type=LocalObjectEntry)
)


schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "children": {"type": "array", "items": {"$ref": "#"}}
    },
    "required": ["name", "children"]
}

data = {"name": "bbb", "children": [{"name": "ccc", "children": []}]}


validate(data, schema, format_checker=FormatChecker())

if __name__ == '__main__':
    schema = ObjectDetectionSample

    print(schema)

    data = {
        "media": {
            "image": "JPEGImages/007762.jpg",
            "image_shape": [
                375,
                500
            ],
            "folder": "VOC2007",
            "source": {
                "database": "The VOC2007 Database",
                "annotation": "PASCAL VOC2007",
                "image": "flickr",
                "flickrid": [
                    "22574264"
                ]
            },
            "depth": 3,
            "segmented": 0,
            "owner": {
                "flickrid": "the food pornographer",
                "name": "the food pornographer"
            }
        },
        "objects": [
            {
                "bbox": [
                    217.0,
                    90.0,
                    145.0,
                    162.0
                ],
                "category": "tvmonitor",
                "pose": "Frontal",
                "truncated": 1,
                "difficult": 0
            },
            {
                "bbox": [
                    252.0,
                    29.0,
                    20.0,
                    60.0
                ],
                "category": "bottle",
                "pose": "Unspecified",
                "truncated": 0,
                "difficult": 0
            },
            {
                "bbox": [
                    292.0,
                    32.0,
                    19.0,
                    39.0
                ],
                "category": "bottle",
                "pose": "Unspecified",
                "truncated": 1,
                "difficult": 0
            },
            {
                "bbox": [
                    58.0,
                    330.0,
                    209.0,
                    45.0
                ],
                "category": "chair",
                "pose": "Unspecified",
                "truncated": 1,
                "difficult": 1
            },
            {
                "bbox": [
                    147.0,
                    16.0,
                    27.0,
                    37.0
                ],
                "category": "cat",
                "pose": "Frontal",
                "truncated": 1,
                "difficult": 0
            }
        ]
    }

    validate(data, schema, format_checker=FormatChecker())
