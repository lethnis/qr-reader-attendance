import os
import sys
import cv2
from pyzbar.pyzbar import decode
import utils


def main():
    """Program reads files from a directory and detects qr-codes.
    You may specify folder or image in command line the following way:
    'python main.py data/' or 'python main.py data/image.jpg'.
    Default directory is 'data/' with test images"""

    # get file names
    images, videos = parse_args()

    os.makedirs("output", exist_ok=True)

    for image in images:
        save_img(image)

    for video in videos:
        save_video(video)


def save_img(img_path):
    """Save image with information from qr-code."""

    img = cv2.imread(img_path)

    img = read_img(img)

    cv2.imwrite(f"output/{os.path.basename(img_path)}", img)


def save_video(video_path):
    """Save video with information from qr-code."""

    # open video file and take the first frame
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()

    # get properties for writer
    w, h, _ = frame.shape
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter.fourcc(*"mp4v")

    writer = cv2.VideoWriter(f"output/{os.path.basename(video_path)}", fourcc, fps, (h, w))

    # process frame and read next one
    while ret:
        writer.write(read_img(frame))
        ret, frame = cap.read()

    # release memory
    cap.release()
    writer.release()


def read_img(img):
    """Read one image and draw fount info on it."""
    # exctract all information from qr-code
    qr_info = decode(img)

    # if we found qr-code and there is some information
    if qr_info:

        # get data(text, url, etc.), rectange coordinates and polygon points
        data, rect, polygon = utils.decode_qr(qr_info)

        # draw polygon
        img = utils.draw_polygon(img, polygon)

        # draw text
        img = utils.put_text(img, data, rect)

    return img


def parse_args():

    MESSAGE = """QR-reader. Usage:
    Please provide a path to a folder or an image/video file.
    Results will be saved to the 'output' directory."""

    base_dir = "data"

    if len(sys.argv) == 2:
        base_dir = sys.argv[1]

    assert len(sys.argv) <= 2, f"Too many arguments. \n\n{MESSAGE}"

    assert os.path.exists(base_dir), f"Couldn't find '{base_dir}'. \n\n{MESSAGE}"

    return split_images_videos(base_dir)


def get_paths(base_dir):
    """Get all paths to files in base folder and all subfolders."""

    paths = []

    # if provided path is directory we search inside it
    if os.path.isdir(base_dir):
        # for every file and folder in base dir
        for i in os.listdir(base_dir):
            # update path so it will be full
            new_path = os.path.join(base_dir, i)
            # check if new path is a file or a folder
            if os.path.isdir(new_path):
                paths.extend(get_paths(new_path))
            else:
                paths.append(new_path)

    # Else path is a file, just add it to the resulting list
    else:
        paths.append(base_dir)

    return paths


def split_images_videos(base_dir):
    """Take all paths and extract only image and video formats."""

    paths = get_paths(base_dir)

    images, videos = [], []

    for path in paths:
        if any([path.endswith(i) for i in [".png", ".jpg", "jpeg"]]):
            images.append(path)
        elif any([path.endswith(i) for i in [".mp4", ".avi"]]):
            videos.append(path)

    return images, videos


if __name__ == "__main__":
    main()
