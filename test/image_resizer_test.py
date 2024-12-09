from src.image_resizer import resize_image

file_path = "003.png"

with open(file_path, "rb") as image_file:
    image_data = image_file.read()

buffer = resize_image(image_data, 300)

test_file_path = "003-width300.png"

with open(test_file_path, "wb") as image_file:
    image_file.write(buffer.getvalue())