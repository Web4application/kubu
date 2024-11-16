#include <stdio.h>
#include "printer.h"

// Function to print a message
void print_message(const char *message) {
    printf("%s\n", message);
}

// Function to print CPU information (example implementation)
void print_cpu_info() {
    printf("CPU Model: Example CPU\n");
    printf("CPU Cores: 4\n");
    printf("CPU Frequency: 3.5 GHz\n");
}
