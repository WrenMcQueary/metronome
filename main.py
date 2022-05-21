"""Simple, decently accurate metronome to be called from the command line.  Plays beeps over an attached sound output
Command line arguments are as follows:
-t, --tempo: tempo in bpm
-p, --pitch: pitch of beeps as a note string (eg A4)
-d, --duration: duration of each beep, in ms
"""


# TODO: Play a little bit of background noise so that other systems on the user's machine don't mute the beeps for being too short
# TODO: Time signature option
# TODO: Chaos option


import argparse
import musicalbeeps
from time import sleep, time


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Play metronome beeps")
    parser.add_argument("--tempo", "-t", action="store", type=float, required=False, default=60, help="tempo in bpm", dest="tempo")
    parser.add_argument("--pitch", "-p", action="store", type=str, required=False, default="A4", help="pitch of beeps as a note string (eg A4)", dest="pitch")
    parser.add_argument("--duration", "-d", action="store", type=int, required=False, default=50, help="duration of each beep in ms", dest="duration")
    args = parser.parse_args()
    tempo = args.tempo
    pitch = args.pitch
    duration = args.duration

    # Handle errors
    # duration not shorter than tempo
    if duration / 1000 >= 60 / tempo:
        raise ValueError("duration must be slower than tempo")

    # Set up other relevant variables
    player = musicalbeeps.Player(volume=0.3, mute_output=True)
    period = 60 / tempo  # seconds
    duration_seconds = duration / 1000
    pause_duration = period - duration_seconds  # seconds

    # Run
    while True:
        time_before = time()
        player.play_note(pitch, duration_seconds)
        while time() - time_before < period:
            sleep(0.001)
