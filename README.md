# headset-led.py

Automatically turns off the LED on a Turtle Beach Elo 7.1 Air headset when it becomes the active audio output on Linux.

## What it does

The script polls the current default audio sink every 2 seconds using `pactl`. When the headset is selected as the active output, it calls `headsetcontrol` to turn off the LED. When a different device becomes active, the state resets so the script is ready to react again on the next switch.

## Requirements

- Linux with PipeWire or PulseAudio
- [`pactl`](https://www.freedesktop.org/wiki/Software/PulseAudio/) (usually part of `pulseaudio-utils`)
- [`headsetcontrol`](https://github.com/Sapd/HeadsetControl) installed and accessible in `$PATH`
- Python 3.6+

Install dependencies on Debian/Ubuntu:

```bash
sudo apt install pulseaudio-utils
```

### Installing headsetcontrol

[headsetcontrol](https://github.com/Sapd/HeadsetControl) is a tool to control USB headsets on Linux — sidetone, battery status, LEDs, and auto-off timer.

**Build from source (Debian/Ubuntu):**

```bash
sudo apt install build-essential git cmake libhidapi-dev
git clone https://github.com/Sapd/HeadsetControl && cd HeadsetControl
mkdir build && cd build
cmake ..
make
sudo make install
```

`sudo make install` also installs udev rules so the tool can be used without root. Reload them with:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

**Other distros:**

| Distro | Command |
|--------|---------|
| NixOS | `nix run nixpkgs#headsetcontrol` |
| Fedora | via [COPR](https://copr.fedorainfracloud.org/coprs/infiniteloop/HeadsetControl/) |
| Gentoo | `emerge -a app-misc/headsetcontrol` |
| macOS | `brew install sapd/headsetcontrol/headsetcontrol --HEAD` |

## Configuration

Open `headset-led.py` and adjust the `ID` variable to match your headset's sink name:

```python
ID = "alsa_output.usb-Turtle_Beach_Elo_7.1_Air_3802FFFF3402-01.analog-stereo"
```

To find your sink name, run:

```bash
pactl get-default-sink
```

or list all available sinks:

```bash
pactl list short sinks
```

## Usage

```bash
python3 headset-led.py
```

Stop with `Ctrl+C`.

## Autostart (systemd user service)

To run the script automatically on login, create a systemd user service:

```ini
# ~/.config/systemd/user/headset-led.service
[Unit]
Description=Headset LED controller
After=default.target

[Service]
ExecStart=/usr/bin/python3 /path/to/headset-led.py
Restart=on-failure

[Install]
WantedBy=default.target
```

Then enable it:

```bash
systemctl --user daemon-reload
systemctl --user enable --now headset-led.service
```

## Notes

- The script only calls `headsetcontrol` on state changes, not on every poll cycle.
- If `pactl` or `headsetcontrol` is not found, the script prints an error and continues rather than crashing.
