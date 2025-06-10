#include <stdio.h>
#include <stdlib.h>
#include <libudev.h>
#include "udev.h"

// Function to initialize udev and retrieve device information
int initialize_udev() {
    struct udev *udev;
    struct udev_enumerate *enumerate;
    struct udev_list_entry *devices, *dev_list_entry;
    struct udev_device *dev;

    // Create udev object
    udev = udev_new();
    if (!udev) {
        fprintf(stderr, "Cannot create udev object\n");
        return 0;
    }

    // Create enumerate object to scan /sys/class
    enumerate = udev_enumerate_new(udev);
    udev_enumerate_add_match_subsystem(enumerate, "block");
    udev_enumerate_scan_devices(enumerate);
    devices = udev_enumerate_get_list_entry(enumerate);

    // Iterate through the list of devices and print their information
    udev_list_entry_foreach(dev_list_entry, devices) {
        const char *path;

        // Get the device path
        path = udev_list_entry_get_name(dev_list_entry);
        dev = udev_device_new_from_syspath(udev, path);

        // Print device information
        printf("Device Node Path: %s\n", udev_device_get_devnode(dev));
        printf("  Subsystem: %s\n", udev_device_get_subsystem(dev));
        printf("  Devtype: %s\n", udev_device_get_devtype(dev));

        // Release the device
        udev_device_unref(dev);
    }

    // Cleanup
    udev_enumerate_unref(enumerate);
    udev_unref(udev);

    return 1;
}

// Function to finalize udev (cleanup resources)
void finalize_udev() {
    // Placeholder for any cleanup if needed
    printf("Finalizing udev...\n");
}
