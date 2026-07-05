"""List directoryes to extract song files."""

import logging
import mimetypes
from itertools import groupby

import filetype

from dakara_feeder.subtitle.parsing import is_subtitle

logger = logging.getLogger(__name__)


def list_directory(path):
    """List song files in given directory recursively.

    Args:
        path (pathlib.Path): Path of directory to scan.

    Returns:
        list of SongPaths: Paths of the files for each song. Paths are relative
        to the given path.
    """
    logger.debug("Listing '%s'", path)
    files_list = [p.relative_to(path) for p in path.rglob("*") if p.is_file()]
    files_list.sort(key=lambda f: (get_path_without_extension(f), f))
    logger.debug("Listed %i files", len(files_list))

    listing = [
        item
        for _, files in groupby(files_list, get_path_without_extension)
        for item in group_by_type(files, path)
    ]

    logger.debug("Found %i different videos", len(listing))

    return listing


def get_path_without_extension(path):
    """Remove extension from file path.

    Args:
        path (pathlib.Path): Path to a file.

    Returns:
        pathlib.Path: Path to the file without the extension.

    Example:

    >>> get_path_without_extension(Path("directory/file0.mkv"))
    ... Path('directory/file0')
    """
    return path.parent / path.stem


def get_main_type(file):
    """Get the type of a given file.

    Args:
        file (pathlib.Path): Absolute path to the file to extract the type.

    Returns
        str: Type if it can be extracted, `None` otherwise.
    """
    # manual detection of subtitle files
    if is_subtitle(file):
        return "subtitle"

    # detect using extension
    mimetype = get_mimetype_by_extension(file)

    # if it failed, detect with magic number
    if mimetype is None:
        mimetype = get_mimetype_by_magic_number(file)

    # abort if not found
    if mimetype is None:
        return None

    maintype, _ = mimetype.split("/")
    return maintype


def get_mimetype_by_magic_number(file):
    """Return the MIME type of a file based on its magic number.

    This strategy is more costly and should be used as a second option.

    Args:
        file (pathlib.Path): Absolute path to the file to extract the MIME type.

    Returns
        str: MIME type. `None` if teh MIME type cannot be identified.
    """
    instance = filetype.guess(str(file))

    if instance:
        return instance.mime

    return None


def get_mimetype_by_extension(file):
    """Return the MIME type of a file based on its extension.

    Args:
        file (pathlib.Path): Absolute path to the file to extract the MIME type.

    Returns
        str: MIME type. `None` if the MIME type cannot be identified.
    """
    mimetype, _ = mimetypes.guess_type(file, strict=False)
    return mimetype


def group_by_type(files, path):
    """Group files by extension.

    Args:
        files (list of pathlib.Path): List of relative path to the files to group.
        path (pathlib.Path): Path of directory to scan.

    Returns:
        list of SongPaths: Paths of the files for each song.
    """
    # sort files by their extension
    videos = []
    audios = []
    subtitles = []
    others = []
    for file in files:
        maintype = get_main_type(path / file)

        if maintype == "video":
            videos.append(file)
            continue

        if maintype == "audio":
            audios.append(file)
            continue

        if maintype == "subtitle":
            subtitles.append(file)
            continue

        others.append(file)

    # check there is at least one video
    if len(videos) == 0:
        return []

    # check there if there are only one audio file
    if len(audios) > 1:
        logger.warning("More than one audio file for video '%s'", videos[0])
        return []

    # check there if there are only one subtitle
    if len(subtitles) > 1:
        logger.warning("More than one subtitle for video '%s'", videos[0])
        return []

    # recombine the files
    return [
        SongPaths(
            video,
            audios[0] if audios else None,
            subtitles[0] if subtitles else None,
            others,
        )
        for video in videos
    ]


class SongPaths:
    """Paths of files related to a song.

    Attributes:
        video (pathlib.Path): Path to the video file.
        audio (pathlib.Path): Path to the audio file.
        subtitle (pathlib.Path): Path to the subtitle file.
        others (list of pathlib.Path): Paths of other files.
    """

    def __init__(self, video, audio=None, subtitle=None, others=None):
        self.video = video
        self.audio = audio
        self.subtitle = subtitle
        self.others = [] if others is None else others

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return "video: {}, audio: {}, subtitle: {}, others: {}".format(
            self.video, self.audio, self.subtitle, self.others
        )
