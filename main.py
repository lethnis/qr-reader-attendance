import os
import sys
import cv2
from pyzbar.pyzbar import decode
import utils


def main():
    """Program reads image or images from a directory and detects qr-codes.
    You may specify folder or image in command line the following way:
    python main.py data/ or python main.py data/image.jpg.
    Default directory is data/ with test images"""

    base_path = "./data/"

    # if different path was specified
    if len(sys.argv) == 2:
        base_path = sys.argv[1]

    # if that path is a directory we show every image
    if os.path.isdir(base_path):
        for img in os.listdir(base_path):
            read_img(os.path.join(base_path, img))

    # if that path is a single image we show that image
    elif os.path.isfile(base_path):
        read_img(sys.argv[1])


def read_img(img_path):
    """Function takes image path and shows information from qr-code if found"""
    # read image from a path
    img = cv2.imread(img_path)
    # exctract all information from qr-code
    qr_info = decode(img)

    # if we found qr-code and there is some information
    if qr_info:

        # get data(text, url, etc.), rectange coordinates and polygon points
        data, rect, polygon = utils.decode_qr(qr_info)

        # draw polygon
        img = utils.draw_polygon(img, polygon)

        # draw text
        img = utils.put_text(img, data, "bottom-left")

    # show image and wait for key pressed
    cv2.imshow(img_path, img)
    cv2.waitKey()


if __name__ == "__main__":
    main()
