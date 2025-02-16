from importlib.resources import as_file, files
from pathlib import Path
from unittest import TestCase, skipUnless

from dakara_feeder.subtitle.extraction import FFmpegSubtitleExtractor


@skipUnless(FFmpegSubtitleExtractor.is_available(), "FFmpeg not installed")
class FFmpegSubtitleExtractorTestCase(TestCase):
    """Test the subtitle extractor based on FFmpeg in an integrated way."""

    def test_extract(self):
        """Test to extract subtitle from file."""
        with as_file(files("tests.resources.media").joinpath("dummy.mkv")) as file:
            extractor = FFmpegSubtitleExtractor.extract(file)
            subtitle = extractor.get_subtitle()

        with as_file(files("tests.resources.subtitles").joinpath("dummy.ass")) as file:
            subtitle_expected = file.read_text()

        self.assertEqual(subtitle, subtitle_expected)

    def test_extract_error(self):
        """Test error when extracting subtitle from file."""
        extractor = FFmpegSubtitleExtractor.extract(Path("nowhere"))
        subtitle = extractor.get_subtitle()

        self.assertEqual(subtitle, "")
