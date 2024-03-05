import numpy as np
import cv2
import pyzbar


def decode_qr(qr_info):
    """Takes a qr info.
    Returns (data, rect, polygon) information."""

    # if there are several qr-code we take only one
    # decode data(url, text, etc.) from bytes
    data = qr_info[0].data.decode()
    # rectangle coordinates: left, top, width, height
    rect = qr_info[0].rect
    # list of points(x, y)
    polygon = qr_info[0].polygon

    return data, rect, polygon


def draw_polygon(img, polygon, color=(0, 255, 0)):
    """Returns an image with drawn polygons. Default color is green."""
    return cv2.polylines(
        img=img,
        pts=[np.array(polygon)],
        isClosed=True,
        color=color,
        thickness=2,
    )


def put_text(img, text, position="top-left", color=(0, 0, 255)):
    """Returns an image with printed text.
    Position may be:
        rect object from decode_qr function,
        'top-left' to place text at the top-left corner of the image,
        'bottom-left' to place text at the bottom-left corner of the image"""
    if isinstance(position, pyzbar.locations.Rect):
        x = position.left
        y = position.top - 15
    elif position == "top-left":
        x = 10
        y = 30
    elif position == "bottom-left":
        x = 10
        y = img.shape[0] - 10

    return cv2.putText(
        img=img,
        text=text,
        org=(x, y),
        fontFace=cv2.FONT_HERSHEY_COMPLEX,
        fontScale=1,
        color=color,
        thickness=2,
    )
