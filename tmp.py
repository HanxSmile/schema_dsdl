string = """
from 

class KeyPointLocalObject(Struct):
    __params__ = ["cdom0"]
    __fields__ = {
        "num_keypoints": Int(xx=""),
        "keypoints": Keypoint()
    }

    __required__ = ["keypoints"]


class KeyPointSample(Struct):
    __params__ = ["cdom0"]
    __fields__ = {
        "media": Image,
        "source": Str,
        "type": Str,
        "height": Int,
        "width": Int,
        "annotations": List(ele_type=KeyPointLocalObject(cdom0="$cdom0"))
    }


sample_type = KeyPointSample(cdom0="coco")"""
exec(string)
# register = dict()
#
#
# class Father:
#     def __init__(self, name):
#         register[name] = self
#
#     def say(self):
#         print("i am father.")
#
#     def __new__(cls, *args, **kwargs):
#         print(cls)
#         print(args)
#         print(kwargs)
#         instance = super().__new__(cls)
#         print(dir(instance))
#         instance.say()
#         print(instance.name)
#         return instance
#
#
# class Son(Father):
#     def __init__(self, name):
#         self.name = name
#         super().__init__(name)
#
#     def say(self):
#         print("i am son")
#
# s = Son("son")
# s2 = register['son']
# s2.say()

