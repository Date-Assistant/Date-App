#!/bin/bash

sudo systemctl disable mariadb
sudo systemctl stop mariadb
sudo systemctl status mariadb
sudo systemctl enable mariadb
sudo systemctl start mariadb
sudo systemctl status mariadb
