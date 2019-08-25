from unittest import TestCase
from unittest.mock import patch

from path import Path

from dakara_feeder import directory_lister


class ListDirectoryTestCase(TestCase):
    """Test the directory lister
    """

    maxDiff = None

    @patch.object(Path, "walkfiles")
    def test_list_directory(self, mocked_walkfiles):
        """Test to list a directory
        """
        # mock directory structure
        mocked_walkfiles.return_value = (
            item
            for item in [
                Path("directory/file0.mkv"),
                Path("directory/file0.ass"),
                Path("directory/file1.mkv"),
                Path("directory/file1.ass"),
                Path("directory/subdirectory/file2.mkv"),
                Path("directory/subdirectory/file3.mkv"),
                Path("directory/subdirectory/file3.ass"),
                Path("directory/subdirectory/empty"),
            ]
        )

        # call the function
        with self.assertLogs("dakara_feeder.directory_lister", "DEBUG") as logger:
            listing = directory_lister.list_directory(Path("directory"))

        # check the structure
        self.assertEqual(len(listing), 4)
        self.assertCountEqual(
            [
                {
                    "video": Path("file0.mkv"),
                    "subtitle": Path("file0.ass"),
                    "others": [],
                },
                {
                    "video": Path("file1.mkv"),
                    "subtitle": Path("file1.ass"),
                    "others": [],
                },
                {
                    "video": Path("subdirectory/file2.mkv"),
                    "subtitle": None,
                    "others": [],
                },
                {
                    "video": Path("subdirectory/file3.mkv"),
                    "subtitle": Path("subdirectory/file3.ass"),
                    "others": [],
                },
            ],
            listing,
        )

        # check the logger was called
        self.assertListEqual(
            logger.output,
            [
                "DEBUG:dakara_feeder.directory_lister:Listing directory",
                "DEBUG:dakara_feeder.directory_lister:Listed 8 files",
                "DEBUG:dakara_feeder.directory_lister:Found 4 different videos",
            ],
        )


class GroupByTypeTestCase(TestCase):
    """Test the group_by_type function
    """

    def test_one_video_one_subtitle(self):
        """Test to group one video and one subtitle
        """
        results = directory_lister.group_by_type([Path("video.mp4"), Path("video.ass")])

        self.assertEqual(len(results), 1)
        self.assertDictEqual(
            results[0],
            {"video": Path("video.mp4"), "subtitle": Path("video.ass"), "others": []},
        )

    def test_one_video_no_subtitle(self):
        """Test to group one video and no subtitle
        """
        results = directory_lister.group_by_type([Path("video.mp4")])

        self.assertEqual(len(results), 1)
        self.assertDictEqual(
            results[0], {"video": Path("video.mp4"), "subtitle": None, "others": []}
        )

    def test_one_video_one_subtitle_plus_others(self):
        """Test to group one video, one subtitle and other files
        """
        results = directory_lister.group_by_type(
            [
                Path("video.mp4"),
                Path("video.ass"),
                Path("video.other"),
                Path("video.dat"),
            ]
        )

        self.assertEqual(len(results), 1)
        self.assertDictEqual(
            results[0],
            {
                "video": Path("video.mp4"),
                "subtitle": Path("video.ass"),
                "others": [Path("video.other"), Path("video.dat")],
            },
        )

    def test_one_video_two_subtitles(self):
        """Test to group one video and two subtitles
        """
        with self.assertLogs("dakara_feeder.directory_lister") as logger:
            results = directory_lister.group_by_type(
                [Path("video.mp4"), Path("video.ass"), Path("video.ssa")]
            )

        self.assertEqual(len(results), 0)

        self.assertListEqual(
            logger.output,
            [
                "WARNING:dakara_feeder.directory_lister:"
                "More than one subtitle for video video.mp4"
            ],
        )

    def test_no_video_no_subtitle_other(self):
        """Test to group no video, no subtitle and one other file
        """
        results = directory_lister.group_by_type([Path("other.dat")])

        self.assertEqual(len(results), 0)

    def test_two_videos_one_subtitle(self):
        """Test to group two videos and one subtitle
        """
        results = directory_lister.group_by_type(
            [Path("video.mp4"), Path("video.mkv"), Path("video.ass")]
        )

        self.assertEqual(len(results), 2)
        self.assertCountEqual(
            results,
            [
                {
                    "video": Path("video.mp4"),
                    "subtitle": Path("video.ass"),
                    "others": [],
                },
                {
                    "video": Path("video.mkv"),
                    "subtitle": Path("video.ass"),
                    "others": [],
                },
            ],
        )

    def test_one_video_upper_case_one_subtitle(self):
        """Test to group one video with uppercase extension and one subtitle
        """
        results = directory_lister.group_by_type([Path("video.MP4"), Path("video.ass")])

        self.assertEqual(len(results), 1)
        self.assertDictEqual(
            results[0],
            {"video": Path("video.MP4"), "subtitle": Path("video.ass"), "others": []},
        )
