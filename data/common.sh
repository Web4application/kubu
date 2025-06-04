#!/bin/bash

# Define paths
TRAIN_DATA_PATH="data/train"
TEST_DATA_PATH="data/test"
MODEL_PATH="kubu_hai_model.mat"
PYTHON_ENV="venv"
LOG_FILE="logs/common.log"

# Function to log messages
log() {
echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# Function to set up the Python virtual environment
setup_env() {
log "Setting up Python virtual environment..."
python3 -m venv $PYTHON_ENV
source $PYTHON_ENV/bin/activate
pip install -r requirements.txt
log "Environment setup complete."
}

# Function to preprocess data
preprocess_data() {
log "Preprocessing data..."
source $PYTHON_ENV/bin/activate
python preprocess_data.py
log "Data preprocessing complete."
}

# Function to train the model
train_model() {
log "Training the model..."
source $PYTHON_ENV/bin/activate
python train_model.py --config model_config.py
log "Model training complete."
}

# Function to evaluate the model
evaluate_model() {
log "Evaluating the model..."
source $PYTHON_ENV/bin/activate
python evaluate_model.py --config model_config.py
log "Model evaluation complete."
}

# Function to clean up generated files
clean() {
log "Cleaning up generated files..."
rm -rf __pycache__ checkpoints logs $MODEL_PATH
log "Cleanup complete."
}

# Function to run all steps
run_all() {
setup_env
preprocess_data
train_model
evaluate_model
}

# Function to run a custom Python script
run_custom_script() {
local script_name=$1
log "Running custom script: $script_name"
source $PYTHON_ENV/bin/activate
python $script_name
log "Custom script $script_name execution complete."
}

# Check command line arguments
case "$1" in
setup_env)
setup_env
;;
preprocess_data)
preprocess_data
;;
train_model)
train_model
;;
evaluate_model)
evaluate_model
;;
clean)
clean
;;
run_all)
run_all
;;
run_custom_script)
if [ -z "$2" ]; then
echo "Usage: $0 run_custom_script <script_name>"
exit 1
fi
run_custom_script $2
;;
*)
echo "Usage: $0 {setup_env|preprocess_data|train_model|evaluate_model|clean|run_all|run_custom_script <script_name>}"
exit 1
esac
