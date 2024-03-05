from datetime import datetime
import time
import cv2
from pyzbar.pyzbar import decode
import utils


def main():
    """Program takes webcam stream and reads qr-codes that may appear.
    Qr-code should store username information. If that user is in the whitelist,
    we grant them access to the system, otherwise we don't grant access."""

    # read whitelist of allowed users
    with open("whitelist.txt") as f:
        whitelist = f.read().split(",")

    # store one most recent user, so we don't give them access twice or more
    most_recent_user = tuple()
    # time in seconds when the same user can get access to the system
    logs_threshold = 5

    # get webcam stream
    cap = cv2.VideoCapture(0)

    print("Press 'q' to quit.")
    while True:
        # start reading frames
        ret, frame = cap.read()

        # if qr-code in frame we get a lot of information
        qr_info = decode(frame)

        if qr_info:
            # decode information to data, rectangle coordinates and polygon points
            user, rect, polygon = utils.decode_qr(qr_info)

            # if qr-code user is the user in the whitelist
            if user in whitelist:
                text = "ACCESS GRANTED"
                color = (0, 255, 0)

                # if current user not in most_recent_user or last attempt was 5 seconds ago
                if user not in most_recent_user or time.time() - most_recent_user[1] > logs_threshold:
                    # remember that user's name and accessing time
                    most_recent_user = (user, time.time())
                    # add user and date and time information to log file
                    with open("log.txt", "a") as f:
                        f.write(f"{user},{datetime.now()}\n")

            # if user not in the whitelist
            else:
                text = "ACCESS DENIED"
                color = (0, 0, 255)

            # draw text and polygons on the frame
            frame = utils.put_text(frame, text, "bottom-left", color)
            frame = utils.draw_polygon(frame, polygon, color)

        # show frame after reading qr-code information
        cv2.imshow("webcam", frame)
        # if 'q' were pressed we quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # release memory
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
