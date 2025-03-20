from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeController:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

    def set_volume(self, level):
        """Set volume level (0-100)"""
        vol = max(0, min(level, 100)) / 100
        self.volume.SetMasterVolumeLevelScalar(vol, None)
        return f"Volume set to {level}%"

    def mute(self):
        self.volume.SetMute(1, None)
        return "Audio muted"

    def unmute(self):
        self.volume.SetMute(0, None)
        return "Audio unmuted"
