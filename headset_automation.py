import subprocess  # Module for calling external programs (pactl, headsetcontrol)
import time        # Module for time.sleep() in the loop

# The sink ID of the headset - this is how PipeWire/PulseAudio uniquely identifies the device
ID = "alsa_output.usb-Turtle_Beach_Elo_7.1_Air_3802FFFF3402-01.analog-stereo"

# Flag: was the headset already active on the last check?
# Prevents headsetcontrol from being called on every loop iteration
headset_was_active = False

print("Monitoring running...")

# Infinite loop - runs until Ctrl+C is pressed
while True:
    try:
        # Query the current default sink from pactl
        # - List instead of string: no shell, safer and more robust
        # - capture_output=True: capture stdout/stderr instead of printing to terminal
        # - text=True: return result as string (not bytes)
        # - check=True: raises an exception if return code != 0
        result = subprocess.run(
            ["pactl", "get-default-sink"],
            capture_output=True,
            text=True,
            check=True,
        )

        # .stdout contains the output, .strip() removes the trailing newline
        current = result.stdout.strip()

        # Check: is the headset currently the default sink?
        if current == ID:
            # Only react if the state has changed
            # (otherwise headsetcontrol would run unnecessarily every 2 seconds)
            if not headset_was_active:
                # Turn off LED via headsetcontrol
                # check=False because we don't want to abort if it fails
                subprocess.run(["headsetcontrol", "-l", "0"], check=False)
                print("Headset active: LED off.")
                headset_was_active = True  # Remember state

        else:
            # A different device is active
            # Only log if the headset was active before (state change)
            if headset_was_active:
                print("Other device active.")
                headset_was_active = False  # Reset state

    # pactl returned an error (e.g. PipeWire is not running)
    except subprocess.CalledProcessError as e:
        print(f"pactl error: {e}")

    # Program not found (pactl or headsetcontrol not installed)
    except FileNotFoundError as e:
        print(f"Program not found: {e}")

    # Ctrl+C: exit cleanly instead of with a traceback
    except KeyboardInterrupt:
        print("\nExiting.")
        break  # Exit loop

    # Wait 2 seconds, then next check
    time.sleep(2)
