# Windows-Like Alt-Tab 3-Finger Gesture

A lightweight Python script that enables Windows-like Alt+Tab functionality using 3-finger touchpad gestures on Linux systems.

## Overview

This tool monitors your touchpad for 3-finger swipes and translates them into Alt+Tab actions:
- Swipe right → Alt+Tab (switch to next window)
- Swipe left → Alt+Shift+Tab (switch to previous window)

**Note:** Consider this script as a fallback option if [Fusuma](https://github.com/iberianpig/fusuma) doesn't work for your setup.

## Prerequisites

- Python 3.6+
- `ydotool` (for simulating keyboard input)
- `libinput` (for touchpad gesture detection)
- `pexpect` Python package

## Installation

1. Install the required system packages:

```bash
sudo apt install ydotool libinput-tools python3-pip
```

2. Install Python dependencies:

```bash
pip install pexpect
```

3. Clone the repository:

```bash
git clone https://github.com/yourusername/Windows-Like-Alt-Tab-3-finger-gesture.git
cd Windows-Like-Alt-Tab-3-finger-gesture
```

4. Make the script executable:

```bash
chmod +x alt-tab-gesture-cmdline.py
```

## Usage

Run the script with:

```bash
python alt-tab-gesture-cmdline.py -p root_password
```

You'll be prompted for your root password (needed for ydotool).

### Command-line Arguments

```
python alt-tab-gesture-cmdline.py [options]

Options:
  -p, --password PASSWORD  Root password for ydotoold (if not provided, will prompt securely)
  -f, --factor FACTOR      Initial sensitivity factor (default: 0.8)
  -t, --threshold THRESHOLD  Swipe threshold distance (default: 30)
  -d, --debug              Enable debug output
```

### Examples

Basic usage:
```bash
python alt-tab-gesture-cmdline.py -p root_password
```

Adjust sensitivity:
```bash
python alt-tab-gesture-cmdline.py --factor 0.6 --threshold 25
```

Enable debug output:
```bash
python alt-tab-gesture-cmdline.py --debug
```

## Auto-start with Ignition

Auto-start it using any software you prefer.

## How It Works

The script:
1. Starts ydotoold for keyboard simulation
2. Monitors touchpad events using libinput
3. Detects 3-finger swipe gestures
4. Translates the gesture direction into Alt+Tab or Alt+Shift+Tab
5. Uses adaptive sensitivity to prevent accidental triggering

## Troubleshooting

- **Error: "No touchpad found"**: Ensure your touchpad is recognized by the system: `libinput list-devices`
- **Permission issues**: Make sure you're providing correct root password for ydotool
- **Script doesn't detect gestures**: Check if your touchpad supports multi-touch gestures: `libinput debug-events`
- **Too sensitive/not sensitive enough**: Adjust the `--factor` and `--threshold` parameters

## Limitations

- Requires root password for ydotool
- May not work with all touchpad hardware
- Performance depends on your system specifications
