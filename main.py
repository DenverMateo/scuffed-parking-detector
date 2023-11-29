import cv2
import pickle
import cvzone
import numpy as np

def load_parking_positions(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def detect_parking_space(img_proc, pos_list, width, height):
    space_counter = 0

    for pos in pos_list:
        x, y = pos

        img_crop = img_proc[y:y + height, x:x + width]
        count = cv2.countNonZero(img_crop)

        if count < 900:
            status = "Available"
            color = (0, 255, 0)
            thickness = 1
            space_counter += 1
        else:
            status = "Occupied"
            color = (0, 0, 255)
            thickness = 1

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, status, (x, y + height - 3), scale=1,
                           thickness=1, offset=0, colorR=color)
        
        
    text = f"Car Slots: {space_counter}/{len(pos_list)}"
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

if __name__ == "__main__":
    # Video feed
    cap = cv2.VideoCapture('parkingVid.mp4')
    posList = load_parking_positions('carPositions')
    width, height = 107, 48

    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY_INV, 25, 16)
        img_median = cv2.medianBlur(img_threshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)

        detect_parking_space(img_dilate, posList, width, height)
        cv2.imshow("Image", img)
        key = cv2.waitKey(30)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
