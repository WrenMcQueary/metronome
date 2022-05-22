"""Simple, decently accurate metronome to be called from the command line.  Plays beeps over an attached sound output
Command line arguments are as follows:
-t, --tempo:        tempo in bpm
-p, --pitch:        pitch of beeps as a note string (eg A4)
-d, --duration:     duration of each beep, in ms
-s, --signature:    time signature numerator (single integer)
-c, --chaos:        automatic random drift in tempo (joke option)
"""


import argparse
import musicalbeeps
from time import sleep, time
from random import uniform


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Play metronome beeps")
    parser.add_argument("--tempo", "-t", action="store", type=float, required=False, default=60, help="tempo in bpm", dest="tempo")
    parser.add_argument("--pitch", "-p", action="store", type=str, required=False, default="A4", help="pitch of emphasized beeps as a note string (eg A4)", dest="pitch")
    parser.add_argument("--duration", "-d", action="store", type=int, required=False, default=50, help="duration of each beep in ms", dest="duration")
    parser.add_argument("--signature", "-s", action="store", type=int, required=False, default=1, help="time signature numerator (single integer)", dest="signature")
    parser.add_argument("--chaos", "-c", action="store_true", required=False, default=False, help="automatic random drift in tempo (joke option)", dest="chaos")
    args = parser.parse_args()
    tempo = args.tempo
    pitch = args.pitch
    duration = args.duration
    signature = args.signature
    chaos = args.chaos

    # Handle errors
    # duration not shorter than tempo
    if duration / 1000 >= 60 / tempo:
        raise ValueError("duration must be slower than tempo")

    # Set up other relevant variables
    player = musicalbeeps.Player(volume=0.3, mute_output=True)
    period = 60 / tempo  # seconds
    duration_seconds = duration / 1000
    pause_duration = period - duration_seconds  # seconds
    pitch_unemphasized = pitch[0] + str(int(pitch[1:])-1)

    # Run
    counter = 0
    while True:
        # Play a note
        time_before = time()
        # Determine pitch to play, based on whether this is a stressed beep
        if counter == 0:
            pitch_to_play = pitch
        else:
            pitch_to_play = pitch_unemphasized
        counter = (counter + 1) % signature
        player.play_note(pitch_to_play, duration_seconds)
        # Drift period if chaos
        if chaos:
            period += uniform(-0.1, 0.1)

        # Wait until it's time to play another note
        while time() - time_before < period:
            sleep(0.001)
