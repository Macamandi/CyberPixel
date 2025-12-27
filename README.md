# 🎨 CyberPixel

![Python](https://img.shields.io/badge/Made%20with-Python-blue)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%20%7C%20Linux-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**CyberPixel** is a lightweight, keyboard-centric pixel art and animation tool designed specifically for **Cyberdecks**, Raspberry Pi screens (3.5" TFT), and retro hardware enthusiasts.

It features a custom GUI optimized for 480x320 resolution, a curated DB32 color palette, and a workflow that keeps your hands on the keyboard.

---

## ✨ Features

* **Cyberdeck Ready:** Interface optimized for small screens (320x320 canvas + sidebar).
* **Animation Support:** Create, edit, and preview animations. Imports/Exports **GIFs** automatically.
* **Smart Tools:** Pencil, Eraser, Flood Fill, and Eyedropper.
* **Dynamic Resolution:** Start with 16x16 and resize to 32x32, 64x64, or 128x128 on the fly (`Ctrl+R`).
* **Professional Workflow:** Unlimited Undo/Redo (`Ctrl+Z`) and Grid toggle.
* **Native Integration:** Installs as a native Linux app with menu shortcuts.

---

## 📸 Screenshots

![CyberPixel on Linux Mint](RodaMenta.png)
*Running on Linux Mint*

![CyberPixel on Cyberdeck](RodaCyber.png)
*Running on custom Raspberry Pi Cyberdeck*

---

## 🚀 Installation

### Raspberry Pi (Bookworm) & Linux Mint

CyberPixel comes with an automated installer script that handles dependencies (pygame, pillow), compilation, and menu shortcuts.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Macamandi/CyberPixel.git](https://github.com/Macamandi/CyberPixel.git)
    cd CyberPixel
    ```

2.  **Run the installer:**
    ```bash
    chmod +x install.sh
    ./install.sh
    ```

3.  **Run it:**
    Find **CyberPixel** in your System Menu under **Graphics**, or run `CyberPixel` in the terminal.

---

## 🎹 Controls & Shortcuts

CyberPixel is designed to be used with a keyboard.

| Category | Key | Action |
| :--- | :---: | :--- |
| **Tools** | `Space` | Paint Pixel |
| | `E` | Eraser |
| | `G` | Flood Fill (Bucket) |
| | `I` | Eyedropper (Pick Color) |
| **Navigation** | `Arrows` | Move Cursor |
| | `Ctrl` + `Arrows` | Shift Canvas (Move Image) |
| **System** | `S` | Save (PNG or GIF) |
| | `L` | Load Image / Open GIF |
| | `Ctrl` + `R` | Resize Canvas (e.g., 16 to 32) |
| | `Ctrl` + `Z` | Undo |
| | `Tab` | Toggle Grid |
| **Animation** | `N` | New Frame |
| | `X` | Delete Current Frame |
| | `<` and `>` | Previous / Next Frame |
| **Palette** | `C` | Open Color Selector |

---

## 🛠️ Tech Stack

* **Language:** Python 3
* **Engine:** Pygame
* **GUI:** Custom drawn (No heavy GUI libraries)
* **Build Tool:** PyInstaller

---

Made with ❤️ and Python by **Macamandi**.
