# 🚀 Terminal Torrent Client

A powerful, interactive terminal-based torrent client for Linux with streaming support. Download or stream torrents directly from magnet links with a simple command!

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-green.svg)
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)

## ✨ Features

- 📥 **Download Mode** - Download complete torrents with progress tracking
- 🎬 **Stream Mode** - Start watching while downloading (sequential download)
- 📊 **Real-time Stats** - Download/upload speeds, peer count, progress bar
- 🎯 **Interactive Interface** - Simple prompts, no complex commands needed
- 🚀 **One Command Install** - Get started in seconds
- 💻 **Works on All Linux Distros** - Ubuntu, Debian, Fedora, Arch, Kali, etc.

## 🎥 Demo

```
$ torrent

╔═══════════════════════════════════════════════════════════╗
║        🚀 TERMINAL TORRENT CLIENT 🚀                      ║
║        Stream or Download from Magnet Links              ║
╚═══════════════════════════════════════════════════════════╝

📎 Paste your magnet link below:
🔗 Magnet Link: magnet:?xt=urn:btih:...

Choose an option:
  [1] 📥 Download - Download the complete torrent
  [2] 🎬 Stream   - Stream while downloading
  [3] ❌ Exit     - Cancel and exit

Enter your choice (1/2/3): 2
```

## 🔧 Quick Install

### Automated Installation (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/terminal-torrent-client/main/install.sh | sudo bash
```

Or if you prefer `wget`:

```bash
wget -qO- https://raw.githubusercontent.com/YOUR_USERNAME/terminal-torrent-client/main/install.sh | sudo bash
```

### Manual Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/terminal-torrent-client.git
   cd terminal-torrent-client
   ```

2. **Run the installer:**
   ```bash
   chmod +x install.sh
   sudo ./install.sh
   ```

That's it! ✅

## 🚀 Usage

Simply type in your terminal:

```bash
torrent
```

Then follow the interactive prompts:
1. Paste your magnet link
2. Choose stream (2) or download (1)
3. Enjoy!

### Command Line Arguments (Optional)

You can also use it non-interactively:

```bash
# Download mode
torrent "magnet:?xt=urn:btih:..." download

# Stream mode
torrent "magnet:?xt=urn:btih:..." stream
```

## 📋 Requirements

- **Python 3.6+**
- **libtorrent** (python3-libtorrent)
- **VLC or MPV** (for streaming mode)

The installer automatically handles all dependencies!

## 🐧 Supported Distributions

- ✅ Ubuntu / Debian / Kali Linux / Linux Mint
- ✅ Fedora / CentOS / RHEL
- ✅ Arch Linux / Manjaro
- ✅ openSUSE
- ✅ Any Linux distribution with Python 3.6+

## 📁 File Locations

- **Downloads saved to:** `~/torrents/` (in your home directory)
- **Executable location:** `/usr/local/bin/torrent`
- **Config:** No configuration needed!

## 🛠️ Manual Installation (Advanced)

If you prefer to install dependencies manually:

### Ubuntu/Debian/Kali:
```bash
sudo apt update
sudo apt install python3-libtorrent vlc
sudo cp torrent_client.py /usr/local/bin/torrent
sudo chmod +x /usr/local/bin/torrent
```

### Fedora:
```bash
sudo dnf install python3-libtorrent vlc
sudo cp torrent_client.py /usr/local/bin/torrent
sudo chmod +x /usr/local/bin/torrent
```

### Arch Linux:
```bash
sudo pacman -S python-libtorrent vlc
sudo cp torrent_client.py /usr/local/bin/torrent
sudo chmod +x /usr/local/bin/torrent
```

## ❓ Troubleshooting

### "No media player found" error

Install VLC or MPV:
```bash
# Ubuntu/Debian
sudo apt install vlc

# Fedora
sudo dnf install vlc

# Arch
sudo pacman -S vlc
```

### Permission denied

Make sure you ran the installer with `sudo`:
```bash
sudo ./install.sh
```

### Command not found after installation

Log out and log back in, or run:
```bash
hash -r
```

## 🗑️ Uninstall

```bash
sudo rm /usr/local/bin/torrent
```

## 📝 License

MIT License - feel free to use, modify, and distribute!

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## ⭐ Support

If you find this useful, please star the repository!

## 🔒 Legal Notice

This tool is for downloading and streaming legal content only. Users are responsible for ensuring they have the right to download and stream the content they access. The developers are not responsible for any misuse of this software.

---

Made with ❤️ for the Linux community
