import numpy as np
import cv2
import os
import shutil



for x in os.listdir('pages'):
    print(x)
    img = cv2.imread('pages/'+x, cv2.IMREAD_COLOR)
    raw = img.copy()
    img[np.where((img != [255, 255, 255]).all(axis=2))] = [200, 0, 0]
    cv2.imwrite(x, img)

if os.path.exists('pages'):
    shutil.rmtree('pages')

if os.path.exists('images'):
    shutil.rmtree('images')
