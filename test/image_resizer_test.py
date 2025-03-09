from src.image_resizer import resize_image
import time

file_path = "20250303_205001.jpg"

with open(file_path, "rb") as image_file:
    image_data = image_file.read()

tik = time.time()
buffer = resize_image(image_data, 500)
tok = time.time()

print("elapsed %f second." % (tok - tik))

test_file_path = "20250303_205001.webp"

with open(test_file_path, "wb") as image_file:
    image_file.write(buffer.getvalue())