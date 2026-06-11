#!/data/data/com.termux/files/usr/bin/bash

echo "Updating packages..."
pkg update -y && pkg upgrade -y

echo "Installing core tools..."
pkg install -y git python openssh

echo "Python version:"
python --version

echo "Git version:"
git --version

echo "SSH client ready. Configure keys with:"
echo "  ssh-keygen -t ed25519 -C \"mvqueen_os\""
