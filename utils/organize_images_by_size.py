import argparse
import os

import cv2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("input_folder_path", help="Path to folder with images.")
    parser.add_argument("output_folder_path",
                        help="Path to location where txt with images path by size will be written.")

    args = parser.parse_args()

    listdir = os.listdir(args.input_folder_path)

    for element in listdir:
        image_file_path = os.path.join(args.input_folder_path, element)
        if os.path.isfile(image_file_path):
            img = cv2.imread(image_file_path, cv2.IMREAD_UNCHANGED)
            if img is not None:
                try:
                    height, width, channels = img.shape
                except ValueError as error:
                    print("Error at image: {}".format(element))
                    print(error.__cause__)
                print("Heigh: {} Width: {} for {}".format(height, width, element))
                if height <= 150 and width <= 150:
                    with open(os.path.join(args.output_folder_path, "small_pictures_path.txt"),
                              mode='a') as output_file:
                        output_file.write(image_file_path + "\n")
