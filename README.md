---

# Netflicks - Video Player   

## Description
This application is a custom video player integrated with Netflix-like profiles and menu navigation, built using Python and Tkinter.

## Features
- Fullscreen video playback with VLC media player integration.
- Profile selection with direct links to Netflix profiles.
- Interactive menu sidebar with navigation options.
- Thumbnail-based video selection with a scrollbar.

## Controls
- **Pause/Play**: Spacebar
- **10 Seconds Forward**: Right Arrow Key
- **10 Seconds Rewind**: Left Arrow Key
- **Exit Player**: Esc Key

## Installation
1. **Python 3**: Install Python 3.12.4 from [Python.org](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe)
2. **VLC**: Install VLC 3.0.21 from [VLC website](https://mirror.kku.ac.th/videolan/vlc/3.0.21/win64/vlc-3.0.21-win64.exe)
3. Install required Python libraries:
   ```
   pip install pillow python-vlc
   ```

## Run locally

After installing the dependencies above, run from the repository folder:

```bash
python main.py
```

Keep `Images/` and `Audio/` beside `main.py`; the application loads them using relative paths. VLC must be installed separately from the `python-vlc` Python package.

## Platform and project scope

The embedded player calls VLC's Windows-specific `set_hwnd` method, and the interface uses an ICO window icon. Linux and macOS support would require platform-specific changes.

This is a local video-player project with a Netflix-inspired interface. Playback uses the files in `Audio/`; profile-management links open Netflix in the browser rather than implementing account authentication or streaming in this application.

## Libraries Used
- Tkinter
- Webbrowser
- Datetime (timedelta)
- Vlc
- PIL (Image, ImageTk)

## Authors
- **Joyson Vadlya**
- **Shrisankhya Purandare**

## © 2024 (J.A.VA) Joyson Vadlya . All rights reserved.
---
