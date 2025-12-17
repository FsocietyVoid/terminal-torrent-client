#!/bin/bash
# Universal installer for Terminal Torrent Client
# Supports Ubuntu, Debian, Fedora, Arch, and more

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🚀 TERMINAL TORRENT CLIENT INSTALLER 🚀            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Please run with sudo:${NC}"
    echo -e "${YELLOW}   sudo ./install.sh${NC}"
    exit 1
fi

# Detect distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo -e "${RED}❌ Cannot detect Linux distribution${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Detected distribution: ${GREEN}$PRETTY_NAME${NC}"
echo ""

# Function to install on Debian-based systems
install_debian() {
    echo -e "${BLUE}📦 Installing dependencies for Debian/Ubuntu...${NC}"
    apt update
    apt install -y python3-libtorrent mpv curl wget
    echo -e "${GREEN}✓ Installed MPV (better for streaming)${NC}"
}

# Function to install on Fedora-based systems
install_fedora() {
    echo -e "${BLUE}📦 Installing dependencies for Fedora...${NC}"
    dnf install -y python3-libtorrent mpv curl wget
    echo -e "${GREEN}✓ Installed MPV (better for streaming)${NC}"
}

# Function to install on Arch-based systems
install_arch() {
    echo -e "${BLUE}📦 Installing dependencies for Arch Linux...${NC}"
    pacman -Sy --noconfirm python-libtorrent mpv curl wget
    echo -e "${GREEN}✓ Installed MPV (better for streaming)${NC}"
}

# Function to install on openSUSE
install_opensuse() {
    echo -e "${BLUE}📦 Installing dependencies for openSUSE...${NC}"
    zypper install -y python3-libtorrent-rasterbar mpv curl wget
    echo -e "${GREEN}✓ Installed MPV (better for streaming)${NC}"
}

# Install dependencies based on distribution
case $DISTRO in
    ubuntu|debian|kali|linuxmint|pop)
        install_debian
        ;;
    fedora|rhel|centos|rocky|almalinux)
        install_fedora
        ;;
    arch|manjaro|endeavouros)
        install_arch
        ;;
    opensuse|opensuse-leap|opensuse-tumbleweed)
        install_opensuse
        ;;
    *)
        echo -e "${YELLOW}⚠️  Unsupported distribution: $DISTRO${NC}"
        echo -e "${YELLOW}⚠️  Attempting generic installation...${NC}"
        echo -e "${YELLOW}⚠️  You may need to install python3-libtorrent manually${NC}"
        ;;
esac

echo ""
echo -e "${BLUE}📥 Downloading torrent client...${NC}"

# Download the main script
if [ -f "torrent_client.py" ]; then
    echo -e "${GREEN}✓ Found torrent_client.py in current directory${NC}"
    SCRIPT_FILE="torrent_client.py"
else
    echo -e "${YELLOW}⬇️  Downloading from GitHub...${NC}"
    curl -fsSL "https://raw.githubusercontent.com/YOUR_USERNAME/terminal-torrent-client/main/torrent_client.py" -o /tmp/torrent_client.py
    SCRIPT_FILE="/tmp/torrent_client.py"
fi

echo -e "${BLUE}📋 Installing torrent command...${NC}"

# Copy script to /usr/local/bin
cp "$SCRIPT_FILE" /usr/local/bin/torrent
chmod +x /usr/local/bin/torrent

# Create torrents directory in user's home
if [ -n "$SUDO_USER" ]; then
    USER_HOME=$(eval echo ~$SUDO_USER)
    mkdir -p "$USER_HOME/torrents"
    chown -R $SUDO_USER:$SUDO_USER "$USER_HOME/torrents"
    echo -e "${GREEN}✓ Created downloads directory: $USER_HOME/torrents${NC}"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║  ✅ Installation Complete!                                ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🚀 Usage:${NC}"
echo -e "   Just type: ${GREEN}torrent${NC}"
echo ""
echo -e "${BLUE}📁 Downloads will be saved to:${NC}"
echo -e "   $USER_HOME/torrents/"
echo ""
echo -e "${BLUE}📖 For help:${NC}"
echo -e "   ${GREEN}torrent --help${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: You may need to log out and log back in for the command to work${NC}"
echo ""
