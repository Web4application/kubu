# Example: utils/data_augmentation.py
import imgaug.augmenters as iaa
import cv2
import os

def augment_image(image):
    """
    Apply data augmentation to an image.

    Parameters:
    image (numpy.ndarray): Input image.

    Returns:
    numpy.ndarray: Augmented image.
    """
    seq = iaa.Sequential([
        iaa.Fliplr(0.5),  # Horizontal flip
        iaa.Affine(rotate=(-20, 20)),  # Random rotation
        iaa.GaussianBlur(sigma=(0, 3.0)),  # Gaussian blur
        iaa.AdditiveGaussianNoise(scale=(0, 0.05*255)),  # Add Gaussian noise
        iaa.Multiply((0.8, 1.2)),  # Random brightness
    ])
    augmented_image = seq(image=image)
    return augmented_image

def augment_images_in_directory(input_dir, output_dir):
    """
    Apply data augmentation to all images in a directory.

    Parameters:
    input_dir (str): Directory containing input images.
    output_dir (str): Directory to save augmented images.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path)
        augmented_image = augment_image(image)
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, augmented_image)

# Example usage
if __name__ == "__main__":
    input_dir = "path/to/input/images"
    output_dir = "path/to/output/images"
    augment_images_in_directory(input_dir, output_dir)
