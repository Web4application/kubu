#ifndef MY_HEADER_H
#define MY_HEADER_H

// Include standard libraries
#include <stdio.h>
#include <stdlib.h>

// Include project-specific headers
#include "cpu.h"
#include "udev.h"
#include "printer.h"
#include "args.h"
#include "global.h"
#include "ascii.h"

// Macro definitions
#define SUCCESS 0
#define FAILURE 1

#include "my_header.h"

// Function to print a welcome message
void print_welcome_message() {
    printf("Welcome to the project!\n");
}

// Function to print an error message
void print_error_message(const char *message) {
    fprintf(stderr, "Error: %s\n", message);
}
