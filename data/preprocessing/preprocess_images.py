import os
import cv2
import numpy as np

def preprocess_images(input_dir, output_dir, image_size=(150, 150)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for class_name in os.listdir(input_dir):
        class_dir = os.path.join(input_dir, class_name)
        output_class_dir = os.path.join(output_dir, class_name)

        if not os.path.exists(output_class_dir):
            os.makedirs(output_class_dir)

        for image_name in os.listdir(class_dir):
            image_path = os.path.join(class_dir, image_name)
            image = cv2.imread(image_path)
            image = cv2.resize(image, image_size)
            output_image_path = os.path.join(output_class_dir, image_name)
            cv2.imwrite(output_image_path, image)

input_dir = 'data/raw_images'
output_dir = 'data/train'
preprocess_images(input_dir, output_dir)
