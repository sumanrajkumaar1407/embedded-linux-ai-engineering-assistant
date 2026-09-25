#!/bin/bash
 
set -e
 
echo "=========================================="
echo "Embedded Linux AI Project - Python Setup"
echo "=========================================="
 
echo
echo "[1/6] Checking Ubuntu version..."
cat /etc/os-release | grep -E '^(NAME|VERSION)='
 
echo
echo "[2/6] Updating package information..."
sudo apt update
 
echo
echo "[3/6] Installing prerequisites..."
sudo apt install -y software-properties-common
 
echo
echo "[4/6] Adding Deadsnakes PPA..."
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
 
echo
echo "[5/6] Installing Python 3.10..."
sudo apt install -y python3.10 python3.10-venv python3.10-dev
 
echo
echo "[6/6] Verifying Python..."
python3.10 --version
 
echo
echo "=========================================="
echo "Python installation completed."
echo "System Python has NOT been replaced."
echo "=========================================="

