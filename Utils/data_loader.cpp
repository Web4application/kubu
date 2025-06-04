// Example: utils/data_loader.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <string>

std::vector<std::vector<std::string>> loadData(const std::string& filePath) {
    std::vector<std::vector<std::string>> data;
    std::ifstream file(filePath);
    std::string line;

    if (file.is_open()) {
        while (getline(file, line)) {
            std::vector<std::string> row;
            std::string cell;
            std::istringstream lineStream(line);

            while (getline(lineStream, cell, ',')) {
                row.push_back(cell);
            }
            data.push_back(row);
        }
        file.close();
    } else {
        std::cerr << "Unable to open file: " << filePath << std::endl;
    }

    return data;
}

int main() {
    std::string filePath = "path/to/data.csv";
    std::vector<std::vector<std::string>> data = loadData(filePath);

    for (const auto& row : data) {
        for (const auto& cell : row) {
            std::cout << cell << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}
