from PIL import Image
import numpy as np
import sys
import os

"""
	This script accepts a source folder containing
	PNG images with 3840x2400 size and resize each 
	of the image to 1280x2400(RGB).

	It does it in the same directory, with same file
	name since that directory came from an sliced file
	and it can always be replaced with a new one.

"""


def modify_num_channels(img_path, num_channel=3):
    with Image.open(img_path) as img_source:
        img_source = Image.open(img_path)
        data_source = np.array(img_source)
        data_destination = data_source.reshape(2400, 1280, num_channel)
        img_destination = Image.fromarray(data_destination, 'RGB')
        img_destination.save(img_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[DEBUG]", "Missing argument, need source dir.")
        print("[DEBUG]", "python3 trans_to_1224.py", "/dir/source")
        sys.exit(1)

    source_dir = sys.argv[1]

    if not os.path.exists(source_dir):
        print("[DEBUG]", "Directory is invalid.")

    source_png_name_list = os.listdir(source_dir)
    source_png_name_list = [os.path.join(
        source_dir, i) for i in source_png_name_list if i.endswith(".png")]
    source_png_name_list.sort()

    for img_path in source_png_name_list:
        modify_num_channels(img_path, num_channel=3)
