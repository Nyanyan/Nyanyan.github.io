from glob import glob
from PIL import Image

files = glob('task/*.png')
print(files)

MAX_SIZE = 256

for file in files:
    img = Image.open(file)
    longer_side = max(img.width, img.height)
    ratio = min(1, MAX_SIZE / longer_side)
    width = int(img.width * ratio)
    height = int(img.height * ratio)
    img_resized = img.resize((width, height))
    file_name = file.split('\\')[1]
    print(file_name, img.width, img.height, ratio, width, height)
    img_resized.save('resized/' + file_name, quality=90)
    