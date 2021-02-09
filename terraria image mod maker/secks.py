import sys
from PIL import Image
from shutil import copytree

def diepls(error):
	print(f"bro pls {error}\npress enter to d i e")
	input()
	exit()


try: image_path = sys.argv[1]
except IndexError: diepls("drag n' drop a png onto secks")

if not image_path.endswith(".png"):
	diepls("use a png u rarted")


img = Image.open(image_path)

if img.size[0] > 1024 or img.size[1] > 1024:
	if img.size[0] > img.size[1]: 	img = img.resize((1024, int(1024/img.size[0] * img.size[1]) ), Image.LANCZOS)
	else:							img = img.resize(( int(1024/img.size[1] * img.size[0]), 1024), Image.LANCZOS)
upscaled_img_size = img.size[0]*2, img.size[1]*2

image_path = image_path.replace("\\","/")
folder_path= image_path[:image_path.rfind("/")]
copytree(folder_path + "/mod skeleton", folder_path + "/h")

with open("h\\InputTile.cs","r+") as file:
	lines = file.readlines()
	lines[9] = f"\t\tprivate const int WIDTH = {upscaled_img_size[0]}, HEIGHT = {upscaled_img_size[1]};\n"
	file.seek(0)

	for line in lines: file.write(line)
	file.truncate()

img.resize(upscaled_img_size, Image.NEAREST).save("h\\InputTile.png")
img.resize((12,12), Image.LANCZOS).resize((24,24), Image.NEAREST).save("h\\InputItem.png")