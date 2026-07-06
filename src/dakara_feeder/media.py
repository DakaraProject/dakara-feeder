VIDEO_EXTENSIONS = (
    ".mkv",
    ".mp4",
)
"""Known video extensions."""

AUDIO_EXTENSIONS = (
    ".ogg",
    ".mka",
    ".m4a",
)
"""Known audio extensions."""


def is_video(file):
    """Detect known video extensions.

    Args:
        file (pathlib.Path): File.

    Returns: True if the extension is known to be of a video file.
    """
    return file.suffix in VIDEO_EXTENSIONS


def is_audio(file):
    """Detect known video extensions.

    Args:
        file (pathlib.Path): File.

    Returns: True if the extension is known to be of an audio file.
    """
    return file.suffix in AUDIO_EXTENSIONS
