import io
from PIL import Image
from exception import FileReadError
from .base_geometry import BaseGeometry
from .utils import bytes_to_numpy


class ImageMedia(BaseGeometry):

    def __init__(self, value):
        self._loc = value
        self._reader = None
        self.namespace = None

    def set_namespace(self, struct_obj):
        self.namespace = struct_obj
        self._reader = struct_obj.file_reader

    @property
    def location(self):
        return self._loc

    def to_bytes(self):
        """
        turn ImageMedia object to bytes
        """
        return io.BytesIO(self._reader.read(self._loc))

    def to_image(self):
        """
        turn ImageMedia object to PIL.Image
        """
        try:
            img = Image.open(self.to_bytes())
        except Exception as e:
            raise FileReadError(f"Failed to convert bytes to an array. {e}") from None
        return img

    def to_array(self):
        """
        turn ImageMedia object to numpy.ndarray
        """
        return bytes_to_numpy(self.to_bytes())

    def __repr__(self):
        return f"path:{self.location}"
