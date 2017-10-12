#!/bin/bash
DATE=$(date +"%Y-%m-%d_%H%M")
sudo raspistill -t 1 -o /var/www/html/webcam/$DATE.jpg
