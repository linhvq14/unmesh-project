#!/bin/bash

# Stop all specified services
sudo systemctl stop facial1.service
sudo systemctl stop get_gps_data1.service
sudo systemctl stop images_upload.service
sudo systemctl stop delete_old_data.service
sudo systemctl stop delete_old_images.service

# List the services that were started and stopped
echo "Services started and stopped:"
echo "facial1.service"
echo "get_gps_data1.service"
echo "images_upload.service"
echo "delete_old_data.service"
echo "delete_old_images.service"