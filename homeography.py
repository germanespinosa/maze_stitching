import numpy as np
from util import Camera
import cv2
from PIL import Image

size = (980,800)
camera = Camera(size)
images = []
images.append(cv2.imread("camera_0.png"))
images.append(cv2.imread("camera_1.png"))
images.append(cv2.imread("camera_2.png"))
images.append(cv2.imread("camera_3.png"))


def create_point(coordinates, size):
    coordinates_x = coordinates["x"]
    coordinates_y = coordinates["y"]
    width, height = size
    center_x, center_y = width/2, height/2
    offset_x = -(width / 41 * coordinates_x)
    offset_y = height / 21 * coordinates_y
    return (center_x+offset_x , center_y+ offset_y)

colors = ["red", "green", "yellow", "blue"]
output_images = []
key_points = [{"x":0,"y":0},{"x":0,"y":6},{"x":1,"y":-5},{"x":-10,"y":0},{"x":10,"y":0},{"x":-20,"y":0},{"x":20,"y":0},{"x":0,"y":10},{"x":0,"y":-10},{"x":-10,"y":-10},{"x":-10,"y":10},{"x":10,"y":10},{"x":10,"y":-10}]
for c, ca in enumerate(camera.associations):
    src_l = []
    dst_l = []
    for i, a in enumerate(ca):
        if a["cell_coordinates"] in key_points:
            src_l.append([a["centroid"]["x"], a["centroid"]["y"]])
            dst_l.append(list(create_point(a["cell_coordinates"], size)))
    src = np.array(src_l)
    dst = np.array(dst_l)
    h, status = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    output_images.append(cv2.warpPerspective(images[c], h, size))
    cv2.imwrite("dst_" + str(c) +".png", output_images[c])

def merging (images, merging_area = 50):
    complete = np.zeros((size[1], size[0], 3), np.uint8)
    complete[0:400, 0:490] = images[1][0:400, 0:490]
    complete[0:400, 490:980] = images[2][0:400, 490:980]
    complete[400:800, 0:490] = images[0][400:800, 0:490]
    complete[400:800, 490:980] = images[3][400:800, 490:980]
    return complete

complete = merging(output_images)
cv2.imshow("final",complete)
cv2.imwrite("composite.png", complete)
cv2.waitKey(0)

