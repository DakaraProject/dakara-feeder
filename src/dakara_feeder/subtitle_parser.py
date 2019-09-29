import re
from abc import ABC, abstractmethod
from collections import OrderedDict

import pysubs2
from dakara_base.exceptions import DakaraError


class SubtitleParser(ABC):
    """Abstract class for subtitle parser

    Args:
        content (anything): object containing the lyrics. Can be a complete
            object or the full text of the lyrics.
    """

    def __init__(self, content={}):
        self.content = content

    @classmethod
    @abstractmethod
    def parse(cls, filepath):
        """Read a subtitle file and store the lyrics

        Args:
            filepath (path.Path): path of the file to extract lyrics from.

        Returns:
            SubtitleParser: instance of the class for the given file.
        """

    @abstractmethod
    def get_lyrics(self):
        """Extract lyrics

        Returns:
            str: text of the lyrics.
        """


class TXTSubtitleParser(SubtitleParser):
    """Subtitle parser for txt files

    >>> from Path import path
    >>> file_path = Path("path/to/file")
    >>> subtitle = TXTSubtitleParser.parse(file_path)
    >>> subtitle.get_lyrics()
    "Mary had a little lamb…"

    Args:
        content (text): Full text of the lyrics.
    """

    @classmethod
    def parse(cls, filepath):
        """Read a subtitle file and store the lyrics

        Args:
            filepath (path.Path): path of the file to extract lyrics from.

        Returns:
            TXTSubtitleParser: instance of the class for the given file.
        """
        return cls(filepath.text())

    def get_lyrics(self):
        """Extract lyrics

        Returns:
            str: text of the lyrics.
        """
        return self.content


class Pysubs2SubtitleParser(SubtitleParser):
    """Subtitle parser for ass, ssa and srt files

    This parser extracts cleaned lyrics from the provided subtitle file.

    It uses the `pysubs2` package to parse the ASS file.

    It can be used with:

    >>> from Path import path
    >>> file_path = Path("path/to/file")
    >>> subtitle = Pysubs2SubtitleParser.parse(file_path)
    >>> subtitle.get_lyrics()
    "Mary had a little lamb…"

    Attributes:
        content (pysubs2.SSAFile): parsed subtitle.
        override_sequence (re.Pattern): regex that matches any tag and any
            drawing area.

    Args:
        content (pysubs2.SSAFile): parsed subtitle.
    """

    override_sequence = re.compile(
        r"""
                \{.*?\\p\d.*?\}     # look for drawing area start tag
                .*?                 # select draw instructions
                (?:                 # until...
                    \{.*?\\p0.*?\}  # draw area end tag
                    |
                    $               # or end of line
                )
                |
                \{.*?\}             # or simply select tags
            """,
        re.UNICODE | re.VERBOSE,
    )

    @classmethod
    def parse(cls, filepath):
        """Read a subtitle file and store the lyrics

        Args:
            filepath (path.Path): path of the file to extract lyrics from.

        Returns:
            Pysubs2SubtitleParser: instance of the class for the given file.
        """
        try:
            instance = cls(pysubs2.load(filepath))

        except FileNotFoundError as error:
            raise SubtitleNotFoundError(
                "Subtitle file {} not found".format(filepath)
            ) from error

        except BaseException as error:
            raise SubtitleParseError(
                "Error when parsing subtitle file {}: {}".format(filepath, error)
            ) from error

        return instance

    def get_lyrics(self):
        """Gives the cleaned text of the Event block

        The text is cleaned in two ways:
            - All tags are removed;
            - Consecutive lines with the same content, the same start and end
                time are merged. This prevents from getting "extra effect
                lines" in the file.

        Returns:
            str: Cleaned lyrics.
        """
        lyrics = []

        # previous line object
        event_previous = None

        # loop over each dialog line
        for event in self.content:

            # Ignore comments
            if event.is_comment:
                continue

            # alter the cleaning regex
            event.OVERRIDE_SEQUENCE = self.override_sequence

            # clean the line
            line = event.plaintext.strip()

            # Ignore empty lines
            if not line:
                continue

            # append the cleaned line conditionnaly
            # Don't append if the line is a duplicate of previous line
            if not (
                event_previous
                and event_previous.plaintext.strip() == line
                and event_previous.start == event.start
                and event_previous.end == event.end
            ):
                lyrics.append(line)

            # update previous line handles
            event_previous = event

        return "\n".join(lyrics)


PARSER_BY_EXTENSION = OrderedDict(
    (
        (".ass", Pysubs2SubtitleParser),
        (".ssa", Pysubs2SubtitleParser),
        (".srt", Pysubs2SubtitleParser),
        (".txt", TXTSubtitleParser),
    )
)


class SubtitleParseError(DakaraError):
    """Error when the subtitle file cannot be parsed
    """


class SubtitleNotFoundError(DakaraError):
    """Error when the subtitle file cannot be found
    """