#!/usr/bin/python

import subprocess
import sys
import typing

from alsaaudio import Mixer


def volume_up_down(way):
    if way not in "toggle|up|down":
        return
    mixer = Mixer()
    if way == "toggle":
        mixer.setmute(bool(mixer.getmute()[0] - 1))
    else:
        step = 5  # qtile.widgets_map["volume"].step
        vol = typing.cast(list[int], mixer.getvolume())[0]
        diff = vol % step
        if way == "up":
            vol += step - diff
        else:
            if diff != 0:
                vol -= diff
            else:
                vol -= step
        if vol <= 0:
            mixer.setmute(True)
        else:
            mixer.setmute(False)
        mixer.setvolume(vol)
        # volume osd using dunst
        subprocess.Popen(
            [
                "notify-send",
                "-a",
                "qtile-volume",
                "-h",
                "string:x-dunst-stack-tag:test",
                "-h",
                f"int:value:{vol}",
                f"Volume: {vol}%",
            ]
        )


volume_up_down(sys.argv[1])
