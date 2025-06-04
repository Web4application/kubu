import os
import numpy as np
from imgaug import augmenters as iaa
from PIL import Image
import nlpaug.augmenter.word as naw
from tsaug import TimeWarp, Crop, Quantize, Drift, Reverse

# Data Collection (Example: Load images from a directory)
def load_images_from_folder(folder):
images = []
for filename in os.listdir(folder):
img = Image.open(os.path.join(folder, filename))
if img is not None:
images.append(np.array(img))
return images

# Data Augmentation for Images
def augment_images(images):
aug = iaa.Sequential([
iaa.Fliplr(0.5),  # horizontal flips
iaa.Crop(percent=(0, 0.1)),  # random crops
iaa.LinearContrast((0.75, 1.5)),  # improve or worsen the contrast
iaa.AdditiveGaussianNoise(scale=(0, 0.05*255)),  # add gaussian noise
iaa.Multiply((0.8, 1.2)),  # change brightness
iaa.Affine(rotate=(-25, 25))  # rotate by -25 to +25 degrees
])
return aug(images=images)

# Save Augmented Images
def save_images(images, folder):
if not os.path.exists(folder):
os.makedirs(folder)
for i, img in enumerate(images):
img = Image.fromarray(img)
img.save(os.path.join(folder, f"augmented_{i}.png"))

# Example Usage
input_folder = 'path/to/input/images'
output_folder = 'path/to/output/images'

# Load images
images = load_images_from_folder(input_folder)

# Augment images
augmented_images = augment_images(images)

# Save augmented images
save_images(augmented_images, output_folder)

# Text Data Augmentation (Example)
def augment_text(text):
aug = naw.SynonymAug(aug_src='wordnet')
return aug.augment(text)

# Time Series Data Augmentation (Example)
def augment_time_series(series):
my_augmenter = (
TimeWarp() * 3  # random time warping 3 times in parallel
+ Crop(size=0.5)  # random cropping
+ Quantize(n_levels=[10, 20, 30])  # random quantize to 10-, 20-, or 30- level sets
+ Drift(max_drift=(0.1, 0.5))  # random drift
+ Reverse()  # random reverse the sequence
)
return my_augmenter.augment(series)

# Example Usage for Text and Time Series
text = "This is an example sentence."
augmented_text = augment_text(text)

time_series = np.array([1, 2, 3, 4, 5])
augmented_series = augment_time_series(time_series)
