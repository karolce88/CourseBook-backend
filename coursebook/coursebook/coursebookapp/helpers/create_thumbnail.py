from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageOps
from io import BytesIO
import sys
import os


def create_thumbnail(image, output_size=(200, 150), quality=80, thumb_name="thumb"):
    output_thumb = BytesIO()
    processed_image = Image.open(image)
    thumbnail_image = ImageOps.fit(
        processed_image, output_size, method=0, bleed=0.0, centering=(0.5, 0.5)
    )
    image_name, image_extension = os.path.splitext(image.name)
    thumb_name = f"{image_name}_{thumb_name}{image_extension}"
    thumbnail_image.save(output_thumb, format="JPEG", quality=quality)
    thumb = InMemoryUploadedFile(
        output_thumb,
        None,
        thumb_name,
        "image/jpeg",
        sys.getsizeof(output_thumb),
        None,
    )
    return thumb
