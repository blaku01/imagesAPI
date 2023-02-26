from io import BytesIO
from typing import Tuple

from PIL import Image


def get_test_image_file(
    size: Tuple[int, int] = (600, 600),
    filename: str = "tmp_testing_name.png",
    extension: str = "png",
):
    in_memory_file = BytesIO()
    image = Image.new("RGBA", size=size, color=(155, 0, 0))
    image.save(in_memory_file, extension)
    in_memory_file.name = filename
    in_memory_file.seek(0)
    return in_memory_file
