import json

# Load the configuration file
with open('config.json', 'r') as f:
config = json.load(f)

# Access data paths
train_data_path = config['data']['train_data_path']
test_data_path = config['data']['test_data_path']
batch_size = config['data']['batch_size']
image_size = tuple(config['data']['image_size'])

# Access model parameters
input_shape = tuple(config['model']['input_shape'])
num_classes = config['model']['num_classes']
dropout_rate = config['model']['dropout_rate']

# Access training parameters
epochs = config['training']['epochs']
learning_rate = config['training']['learning_rate']
validation_split = config['training']['validation_split']

Data Loading
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Create data generators
train_datagen = ImageDataGenerator(
rescale=1./255,
rotation_range=config['data_augmentation']['rotation_range'],
width_shift_range=config['data_augmentation']['width_shift_range'],
height_shift_range=config['data_augmentation']['height_shift_range'],
shear_range=config['data_augmentation']['shear_range'],
zoom_range=config['data_augmentation']['zoom_range'],
horizontal_flip=config['data_augmentation']['horizontal_flip'],
fill_mode=config['data_augmentation']['fill_mode'],
validation_split=validation_split
)

train_generator = train_datagen.flow_from_directory(
train_data_path,
target_size=image_size,
batch_size=batch_size,
class_mode='categorical',
subset='training'
)

validation_generator = train_datagen.flow_from_directory(
train_data_path,
target_size=image_size,
batch_size=batch_size,
class_mode='categorical',
subset='validation'
)

Model Building
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Build the model
model = Sequential([
Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
MaxPooling2D((2, 2)),
Conv2D(64, (3, 3), activation='relu'),
MaxPooling2D((2, 2)),
Flatten(),
Dense(128, activation='relu'),
Dropout(dropout_rate),
Dense(num_classes, activation='softmax')
])

Model Compilation and Training
from tensorflow.keras.optimizers import Adam

# Compile the model
model.compile(
optimizer=Adam(learning_rate=learning_rate),
loss='categorical_crossentropy',
metrics=['accuracy']
)

# Train the model
model.fit(
train_generator,
epochs=epochs,
validation_data=validation_generator
)
