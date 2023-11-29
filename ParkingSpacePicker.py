import cv2
import pickle

width, height = 107, 48

try:
    with open('CarParkPos', 'rb') as f:
        pos_list = pickle.load(f)
except FileNotFoundError:
    pos_list = []


def mouse_click(events, x, y, flags, params):
    global pos_list

    if events == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        pos_list = [pos for pos in pos_list if not (pos[0] < x < pos[0] + width and pos[1] < y < pos[1] + height)]

    with open('CarParkPos', 'wb') as f:
        pickle.dump(pos_list, f)


while True:
    img = cv2.imread('carParkImg.png')
    for pos in pos_list:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouse_click)
    key = cv2.waitKey(30)
    if key == 27:
        break

cv2.destroyAllWindows()
