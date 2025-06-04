# Example: utils/data_loader.rb
require 'csv'

def load_data(file_path)
  data = []
  CSV.foreach(file_path, headers: true) do |row|
    data << row.to_hash
  end
  data
end

def preprocess_data(data)
  # Example preprocessing steps
  data.reject { |row| row.values.any?(&:nil?) }
end

if __FILE__ == $0
  file_path = 'path/to/data.csv'
  data = load_data(file_path)
  preprocessed_data = preprocess_data(data)
  puts preprocessed_data
end
