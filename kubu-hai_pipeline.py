import os
import numpy as np
from imgaug import augmenters as iaa
from PIL import Image
import nlpaug.augmenter.word as naw
from tsaug import TimeWarp, Crop, Quantize, Drift, Reverse
import boto3
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from kerastuner.tuners import RandomSearch
from sagemaker import get_execution_role
from sagemaker.tensorflow import TensorFlow

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

# Example Usage for Image Data
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

# AWS S3 for Data Storage
s3 = boto3.client('s3')
s3.upload_file('local_file_path', 'bucket_name', 's3_file_path')

# Launch EC2 Instance for Training
ec2 = boto3.client('ec2')
response = ec2.run_instances(
ImageId='ami-0abcdef1234567890',  # Replace with your desired AMI ID
InstanceType='p2.xlarge',  # Choose an instance type with GPU support
MinCount=1,
MaxCount=1,
KeyName='your-key-pair-name'
)
instance_id = response['Instances'][0]['InstanceId']
print(f'Launched EC2 instance with ID: {instance_id}')

# SageMaker for Managed Training
sagemaker_session = sagemaker.Session()
role = get_execution_role()
estimator = TensorFlow(
entry_point='train.py',  # Your training script
role=role,
instance_count=1,
instance_type='ml.p2.xlarge',
framework_version='2.3.0',
py_version='py37',
script_mode=True
)
estimator.fit({'training': 's3://your-bucket/path/to/training/data'})

# AWS Lambda for Serverless Preprocessing
def lambda_handler(event, context):
data = event['data']
processed_data = preprocess(data)
s3.put_object(Bucket='your-bucket', Key='processed_data.json', Body=json.dumps(processed_data))
return {
'statusCode': 200,
'body': json.dumps('Preprocessing complete')
}

def preprocess(data):
return data

# Transfer Learning with Hyperparameter Tuning and Model Optimization
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False
x = Flatten()(base_model.output)
x = Dense(512, activation='relu')(x)
x = Dense(1, activation='sigmoid')(x)  # Assuming binary classification
model = Model(inputs=base_model.input, outputs=x)
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

train_datagen = ImageDataGenerator(
rescale=1./255,
rotation_range=40,
width_shift_range=0.2,
height_shift_range=0.2,
shear_range=0.2,
zoom_range=0.2,
horizontal_flip=True,
fill_mode='nearest'
)

train_generator = train_datagen.flow_from_directory(
'path/to/train/data',
target_size=(224, 224),
batch_size=32,
class_mode='binary'
)

def build_model(hp):
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False
x = Flatten()(base_model.output)
x = Dense(hp.Int('units', min_value=128, max_value=512, step=32), activation='relu')(x)
x = Dense(1, activation='sigmoid')(x)
model = Model(inputs=base_model.input, outputs=x)
model.compile(optimizer=Adam(learning_rate=hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
loss='binary_crossentropy',
metrics=['accuracy'])
return model

tuner = RandomSearch(
build_model,
objective='val_accuracy',
max_trials=5,
executions_per_trial=3,
directory='my_dir',
project_name='kubu_hai_tuning'
)

tuner.search(train_generator, epochs=10, validation_data=validation_generator)
best_model = tuner.get_best_models(num_models=1)[0]

for layer in base_model.layers[-4:]:
layer.trainable = True

best_model.compile(optimizer=Adam(learning_rate=1e-5), loss='binary_crossentropy', metrics=['accuracy'])
history = best_model.fit(train_generator, epochs=10, validation_data=validation_generator)
best_model.save('kubu_hai_model.h5')
