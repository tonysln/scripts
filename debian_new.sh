#!/bin/bash

# Debian Post Install Automation


# [1] Update
sudo apt -y update
sudo apt -y upgrade
sudo apt -y clean
sudo apt -y autoclean
sudo apt -y autoremove


# [2] Install Libraries & Tools
sudo apt -y install git build-essential cmake wget net-tools ffmpeg default-jdk doxygen libhackrf-dev hackrf aircrack-ng gcc haxe neko libusb-1.0-0 libusb-1.0-0-dev pcsc-tools pcscd swig python3-pip


# [3] Install NVIDIA Drivers
sudo add-apt-repository ppa:graphics-drivers/ppa -y
sudo apt -y update
sudo apt -y install nvidia-driver


# [4] Install Apps
sudo apt -y install audacity chromium wireshark 


# [5] Final Cleanup
sudo apt -y clean
sudo apt -y autoclean
sudo apt -y autoremove
