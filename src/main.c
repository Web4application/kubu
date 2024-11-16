#include <stdio.h>
#include "cpu.h"
#include "printer.h"
#include "args.h"
#include "global.h"

int main(int argc, char *argv[]) {
    // Initialize the program arguments
    if (!initialize_args(argc, argv)) {
        fprintf(stderr, "Failed to initialize arguments.\n");
        return 1;
    }

    // Initialize CPU information
    if (!initialize_cpu()) {
        fprintf(stderr, "Failed to initialize CPU information.\n");
        return 1;
    }

    // Print CPU information
    print_cpu_info();

    // Finalize and clean up
    finalize_cpu();
    finalize_args();

    return 0;
}
