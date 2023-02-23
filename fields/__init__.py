import sys
from .special import *
from .generic import *
from .unstructure import *
from .struct_entry import *
from .classdomain import ClassDomain

__all__ = ["Struct", "ClassDomain"]

_module = sys.modules[__name__]
for k in dir():
    if k.endswith("Field"):
        v = getattr(_module, k)
        k = k.replace("Field", "")
        setattr(_module, k, v.get_field)
        __all__.append(k)

# __special_fields__ = [
#     "Coord",
#     "Coord3D",
#     "Interval",
#     "BBox",
#     "RotatedBBox",
#     "Polygon",
#     "Label",
#     "Keypoint",
#     "Text",
#     "ImageShape",
#     "InstanceID",
#     "UniqueID",
#     "Date",
#     "Time"
# ]
#
# __generic_fields__ = [
#     "Bool",
#     "Int",
#     "Num",
#     "Str",
#     "Dict",
#     "List"
# ]
#
# __unstructure_fields__ = [
#     "Image",
#     "LabelMap",
#     "InstanceMap"
# ]
#
# __all__ = __unstructure_fields__ + __generic_fields__ + __special_fields__
