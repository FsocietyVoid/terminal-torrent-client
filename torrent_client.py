#!/usr/bin/env python3
"""
Terminal-based Torrent Client with Streaming Support
Interactive mode for easy use
"""

import libtorrent as lt
import time
import sys
import os
import subprocess
from pathlib import Path

class TorrentClient:
    def __init__(self, download_path="./torrents"):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        self.session = lt.session()
        self.session.listen_on(6881, 6891)
        
    def add_magnet(self, magnet_link):
        """Add a magnet link to the session"""
        params = lt.parse_magnet_uri(magnet_link)
        params.save_path = str(self.download_path)
        return self.session.add_torrent(params)
    
    def get_progress(self, handle):
        """Get download progress information"""
        status = handle.status()
        return {
            'progress': status.progress * 100,
            'download_rate': status.download_rate / 1000,
            'upload_rate': status.upload_rate / 1000,
            'num_peers': status.num_peers,
            'state': str(status.state),
            'total_size': status.total_wanted,
            'downloaded': status.total_done
        }
    
    def download_mode(self, magnet_link):
        """Download torrent completely"""
        print(f"\n{'='*60}")
        print("📥 DOWNLOAD MODE")
        print(f"{'='*60}\n")
        
        handle = self.add_magnet(magnet_link)
        print("🔍 Fetching metadata...")
        
        while not handle.has_metadata():
            time.sleep(0.1)
        
        torrent_info = handle.get_torrent_info()
        print(f"\n📦 Torrent: {torrent_info.name()}")
        print(f"📊 Size: {torrent_info.total_size() / (1024**3):.2f} GB")
        print(f"📁 Files: {torrent_info.num_files()}")
        print(f"💾 Saving to: {self.download_path}\n")
        
        while not handle.is_seed():
            info = self.get_progress(handle)
            
            bar_length = 40
            filled = int(bar_length * info['progress'] / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            print(f"\r[{bar}] {info['progress']:.1f}% | "
                  f"↓ {info['download_rate']:.1f} KB/s | "
                  f"↑ {info['upload_rate']:.1f} KB/s | "
                  f"👥 {info['num_peers']}", end='', flush=True)
            
            time.sleep(1)
        
        print("\n\n✅ Download complete!")
        print(f"📂 Location: {self.download_path / torrent_info.name()}")
    
    def stream_mode(self, magnet_link):
        """Stream torrent with sequential download"""
        print(f"\n{'='*60}")
        print("🎬 STREAM MODE")
        print(f"{'='*60}\n")
        
        handle = self.add_magnet(magnet_link)
        handle.set_sequential_download(True)
        
        print("🔍 Fetching metadata...")
        
        while not handle.has_metadata():
            time.sleep(0.1)
        
        torrent_info = handle.get_torrent_info()
        print(f"\n📦 Torrent: {torrent_info.name()}")
        print(f"📊 Size: {torrent_info.total_size() / (1024**3):.2f} GB")
        
        # Find the largest file (usually the video)
        files = torrent_info.files()
        largest_file = max(range(files.num_files()), 
                          key=lambda i: files.file_size(i))
        
        # Construct proper file path
        file_relative_path = files.file_path(largest_file)
        file_path = self.download_path / file_relative_path
        print(f"🎥 Main file: {file_relative_path}")
        print(f"📁 Full path: {file_path}")
        print(f"\n⏳ Buffering for streaming...\n")
        
        # Prioritize the largest file only
        file_priorities = [0] * files.num_files()
        file_priorities[largest_file] = 7
        handle.prioritize_files(file_priorities)
        
        # Prioritize first pieces more aggressively
        num_pieces = torrent_info.num_pieces()
        for i in range(min(20, num_pieces)):
            handle.piece_priority(i, 7)
        
        # Wait for initial buffer (10% or 100MB, whichever is smaller)
        buffer_threshold = min(0.10, 100 * 1024 * 1024 / torrent_info.total_size())
        
        while True:
            info = self.get_progress(handle)
            
            bar_length = 40
            filled = int(bar_length * info['progress'] / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            print(f"\r[{bar}] {info['progress']:.1f}% | "
                  f"↓ {info['download_rate']:.1f} KB/s | "
                  f"👥 {info['num_peers']}", end='', flush=True)
            
            # Check if file exists and has minimum size
            if file_path.exists() and file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB minimum
                if info['progress'] / 100 >= buffer_threshold or handle.is_seed():
                    break
            
            time.sleep(1)
        
        print("\n\n✅ Ready to stream!")
        print(f"\n📂 File location: {file_path}")
        
        # Wait a bit for file to be accessible
        time.sleep(2)
        
        # Verify file exists and is readable
        if not file_path.exists():
            print(f"\n⚠️  Warning: File not yet created. Waiting...")
            # Wait for file to be created
            for _ in range(30):
                if file_path.exists() and file_path.stat().st_size > 1024 * 1024:
                    break
                time.sleep(1)
        
        if not file_path.exists():
            print(f"\n❌ Error: File not accessible yet. Try downloading more first.")
            return
        
        print("\n🎬 Opening media player...")
        
        # Try to open with available media players
        player_opened = False
        file_str = str(file_path.absolute())
        
        try:
            if os.path.exists('/usr/bin/mpv'):
                # MPV is better for streaming incomplete files
                subprocess.Popen(['mpv', '--force-seekable=yes', file_str], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
                player_opened = True
                print("✓ Opened with MPV")
            elif os.path.exists('/usr/bin/vlc'):
                subprocess.Popen(['vlc', '--file-caching=10000', file_str], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
                player_opened = True
                print("✓ Opened with VLC")
            elif os.path.exists('/snap/bin/vlc'):
                subprocess.Popen(['vlc', '--file-caching=10000', file_str],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                player_opened = True
                print("✓ Opened with VLC")
            else:
                print("\n⚠️  No media player found.")
                print("Install MPV (recommended for streaming) or VLC:")
                print("  Ubuntu/Debian: sudo apt install mpv")
                print("  Fedora: sudo dnf install mpv")
                print("  Arch: sudo pacman -S mpv")
        except Exception as e:
            print(f"⚠️  Error opening player: {e}")
            print(f"\n💡 Try opening manually: mpv '{file_str}'")
        
        if player_opened:
            # Continue downloading in background
            print("\n⬇️  Continuing download in background...")
            print("Press Ctrl+C to stop\n")
            
            try:
                while not handle.is_seed():
                    info = self.get_progress(handle)
                    
                    bar_length = 40
                    filled = int(bar_length * info['progress'] / 100)
                    bar = '█' * filled + '░' * (bar_length - filled)
                    
                    print(f"\r[{bar}] {info['progress']:.1f}% | "
                          f"↓ {info['download_rate']:.1f} KB/s | "
                          f"↑ {info['upload_rate']:.1f} KB/s", end='', flush=True)
                    
                    time.sleep(1)
                
                print("\n\n✅ Download complete!")
            except KeyboardInterrupt:
                print("\n\n⏹️  Stopped by user")

def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🚀 TERMINAL TORRENT CLIENT 🚀                      ║
║                                                           ║
║        Stream or Download from Magnet Links              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)

def get_magnet_link():
    """Prompt user for magnet link"""
    print("\n📎 Paste your magnet link below:")
    print("   (It should start with 'magnet:?xt=...')\n")
    
    while True:
        magnet_link = input("🔗 Magnet Link: ").strip()
        
        if not magnet_link:
            print("❌ Error: Magnet link cannot be empty. Try again.\n")
            continue
        
        if not magnet_link.startswith("magnet:"):
            print("❌ Error: Invalid magnet link. Must start with 'magnet:'\n")
            continue
        
        return magnet_link

def get_mode_choice():
    """Prompt user for download or stream mode"""
    print("\n" + "="*60)
    print("Choose an option:")
    print("="*60)
    print("\n  [1] 📥 Download - Download the complete torrent")
    print("  [2] 🎬 Stream   - Stream while downloading")
    print("  [3] ❌ Exit     - Cancel and exit\n")
    
    while True:
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            return 'download'
        elif choice == '2':
            return 'stream'
        elif choice == '3':
            return 'exit'
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.\n")

def main():
    print_banner()
    
    # Get magnet link from user
    magnet_link = get_magnet_link()
    
    # Get mode choice from user
    mode = get_mode_choice()
    
    if mode == 'exit':
        print("\n👋 Goodbye!\n")
        sys.exit(0)
    
    # Initialize client
    client = TorrentClient()
    
    try:
        if mode == 'stream':
            client.stream_mode(magnet_link)
        elif mode == 'download':
            client.download_mode(magnet_link)
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user")
        print("\n👋 Goodbye!\n")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
