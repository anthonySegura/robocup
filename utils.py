import cv2
import numpy as np
from PIL import Image, ImageDraw
import json
from math import atan, pi

with open('./config.json', 'r') as file:
    config = json.load(file)

# Variables globales
calibration_data = config['camera_calibration']

def plot_img(image, box, probs, thickness=1):
    image = Image.fromarray((image).astype(np.uint8))
    draw = ImageDraw.Draw(image)
    if probs[0] > 0.5:
        x, y = box 
        # Dibuja una cruz en el centro del bbox
        draw.line((x, y - 5, (x, y + 5)), fill='#FF0000', width=thickness)
        draw.line((x - 5, y, (x + 5, y)), fill='#FF0000', width=thickness)
        
    return image

def toRGB(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def scale_values(org_size, target_size, value):
    scale = target_size / org_size 
    scaled = value * scale
    return scaled

def get_focal_length(object):
    known_width = calibration_data[object]['known_width_cm']
    distance = calibration_data[object]['distance_cm']
    pixels_width = calibration_data[object]['pixels_width']

    return (pixels_width * distance) / known_width

focal_lengths = {
    'ball': get_focal_length('ball'),
    'mark': get_focal_length('mark')
}

def get_distance_to_object(object_name, pixels_width):
    known_width = calibration_data[object_name]['known_width_cm']
    focal_length = focal_lengths[object_name]
    return (known_width * focal_length) / pixels_width 

def rotation_angle(object_name, object_center, image_center):
    focal_length = focal_lengths[object_name]
    x_ = object_center[0] - image_center[0] 
    angle = atan(x_ / focal_length) * (180 / pi) # Se convierte a grados
    return angle
