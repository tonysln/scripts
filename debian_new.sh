#!/bin/bash

# Debian Post Install Automation


# Update
sudo apt -y update
sudo apt -y upgrade
sudo apt -y clean
sudo apt -y autoclean
sudo apt -y autoremove


# Install Libraries & Tools
sudo apt -y install git build-essential cmake wget net-tools ffmpeg default-jdk doxygen libhackrf-dev hackrf aircrack-ng gcc haxe neko libusb-1.0-0 libusb-1.0-0-dev pcsc-tools pcscd swig python3-pip texlive ca-certificates gnupg curl lsb-release 

# Docker
sudo mkdir -p /etc/apt/keyrings
sudo chmod a+r /etc/apt/keyrings/docker.gpg
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install NVIDIA Drivers
#sudo add-apt-repository ppa:graphics-drivers/ppa -y
#sudo apt -y update
#sudo apt -y install nvidia-driver


# Install Apps
sudo apt -y install audacity chromium wireshark 

# JetBrains Apps
curl -s https://s3.eu-central-1.amazonaws.com/jetbrains-ppa/0xA6E8698A.pub.asc | sudo apt-key add -
echo "deb http://jetbrains-ppa.s3-website.eu-central-1.amazonaws.com any main" | sudo tee /etc/apt/sources.list.d/jetbrains-ppa.list > /dev/null
sudo apt -u update
sudo apt -y install clion intellij-idea-ultimate


# Final Cleanup
sudo apt -y clean
sudo apt -y autoclean
sudo apt -y autoremove
