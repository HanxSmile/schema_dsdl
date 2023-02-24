class KeyPointLocalObject(Struct):
    __params__ = ["cdom0"]
    __fields__ = {
        "num_keypoints": Int,
        "keypoints": Keypoint[dom = "$cdom0"]
    }

    __optional__ = ["num_keypoints"]


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



sample_type = KeyPointSample(cdom0="coco")
