from pathlib import Path
from unittest import TestCase

from dakara_feeder.media import is_audio, is_video


class IsVideoTestCase(TestCase):
    def test_is_video(self):
        """Test known video extensions."""
        for file in (Path("file.mkv"), Path("file.mp4")):
            self.assertTrue(is_video(file))


class IsAudioTestCase(TestCase):
    def test_is_audio(self):
        """Test known audio extensions."""
        for file in (Path("file.ogg"), Path("file.mka"), Path("file.m4a")):
            self.assertTrue(is_audio(file))
