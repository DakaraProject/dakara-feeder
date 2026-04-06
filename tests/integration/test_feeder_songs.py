from importlib.resources import as_file, files
from shutil import copy
from tempfile import TemporaryDirectory
from unittest import TestCase, skipUnless
from unittest.mock import patch

from dakara_feeder.feeder.songs import SongsFeeder
from dakara_feeder.metadata import FFProbeMetadataParser


@skipUnless(FFProbeMetadataParser.is_available(), "FFProbe not installed")
@patch("dakara_feeder.feeder.songs.HTTPClientDakara", autospec=True)
class SongsFeederIntegrationTestCase(TestCase):
    """Integration tests for the SongsFeeder class."""

    def test_feed(self, mocked_http_client_dakara_class):
        """Test to feed."""
        # create the mocks
        mocked_http_client_dakara_class.return_value.retrieve_songs.return_value = []

        # create the object
        with TemporaryDirectory() as temp:
            # copy required files
            with as_file(files("tests.resources.media").joinpath("dummy.ass")) as file:
                copy(file, temp)

            with as_file(files("tests.resources.media").joinpath("dummy.mkv")) as file:
                copy(file, temp)

            config = {"server": {}, "kara_folder": str(temp)}
            feeder = SongsFeeder(config, progress=False)

            # call the method
            with self.assertLogs("dakara_feeder.feeder.songs", "DEBUG"):
                with self.assertLogs("dakara_base.progress_bar"):
                    feeder.feed()

        # assert the mocked calls
        mocked_http_client_dakara_class.return_value.retrieve_songs.assert_called_with()
        mocked_http_client_dakara_class.return_value.post_song.assert_called_with(
            [
                {
                    "title": "dummy",
                    "filename": "dummy.mkv",
                    "directory": "",
                    "duration": 2.023,
                    "has_instrumental": True,
                    "artists": [],
                    "works": [],
                    "tags": [],
                    "version": "",
                    "detail": "",
                    "detail_video": "",
                    "lyrics": "Piyo!",
                }
            ]
        )
