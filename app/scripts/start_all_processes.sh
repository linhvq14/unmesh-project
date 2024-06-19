#!/bin/bash

# Start all specified services
sudo systemctl start facial1.service
sudo systemctl start get_gps_data1.service
sudo systemctl start images_upload.service
sudo systemctl start delete_old_data.service
sudo systemctl start delete_old_images.service

# List the services that were started and stopped
echo "Services started and started:"
echo "facial1.service"
echo "get_gps_data1.service"
echo "images_upload.service"
echo "delete_old_data.service"
echo "delete_old_images.service"
