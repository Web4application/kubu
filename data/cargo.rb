require 'rake'
require 'fileutils'

# Define paths
TRAIN_DATA_PATH = 'data/train'
TEST_DATA_PATH = 'data/test'
MODEL_PATH = 'kubu_hai_model.mat'
PYTHON_ENV = 'venv'

# Task to set up the Python virtual environment
task :setup_env do
puts "Setting up Python virtual environment..."
sh "python3 -m venv #{PYTHON_ENV}"
sh "#{PYTHON_ENV}/bin/pip install -r requirements.txt"
end

# Task to preprocess data
task :preprocess_data do
puts "Preprocessing data..."
sh "#{PYTHON_ENV}/bin/python preprocess_data.py"
end

# Task to train the model
task :train_model => [:setup_env, :preprocess_data] do
puts "Training the model..."
sh "#{PYTHON_ENV}/bin/python train_model.py --config model_config.py"
end

# Task to evaluate the model
task :evaluate_model => [:setup_env] do
puts "Evaluating the model..."
sh "#{PYTHON_ENV}/bin/python evaluate_model.py --config model_config.py"
end

# Task to clean up generated files
task :clean do
puts "Cleaning up generated files..."
FileUtils.rm_rf(['__pycache__', 'checkpoints', 'logs', MODEL_PATH])
end

# Task to run all steps
task :all => [:train_model, :evaluate_model]

# Default task
task :default => [:all]

# Additional custom tasks
namespace :custom do
desc "Run custom Python script"
task :run_script, [:script_name] do |t, args|
script_name = args[:script_name] || 'custom_script.py'
puts "Running custom script: #{script_name}"
sh "#{PYTHON_ENV}/bin/python #{script_name}"
end

desc "Deploy model"
task :deploy do
puts "Deploying the model..."
# Add deployment commands here
end
end
