import io

from PIL import Image


def resize_image(image_data, width):
    # Open the image using PIL
    image = Image.open(io.BytesIO(image_data))

    # Resize the image
    original_width, original_height = image.size
    new_height = int((width / original_width) * original_height)
    resized_image = image.resize((width, new_height), Image.LANCZOS)

    # Save the resized image to a buffer
    buffer = io.BytesIO()
    resized_image.save(buffer, format=image.format)
    buffer.seek(0)

    return buffer