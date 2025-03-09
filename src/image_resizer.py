import io
from PIL import Image, ImageOps


def resize_image(image_data, width):
    try:
        # Open the image using PIL
        image = Image.open(io.BytesIO(image_data))
        image = ImageOps.exif_transpose(image)

        if type(width) is int and width > 0:
            # Resize the image
            original_width, original_height = image.size
            new_height = int((width / original_width) * original_height)
            image = image.resize((width, new_height))

        # Save the resized image to a buffer
        buffer = io.BytesIO()
        image.save(buffer, format="webp")
        buffer.seek(0)
        return buffer

    except IOError:
        return image_data
