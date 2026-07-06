# Changelog

<!---
## 0.0.1 - 1970-01-01

### Added

- New stuff.

### Changed

- Changed stuff.

### Deprecated

- Deprecated stuff.

### Removed

- Removed stuff.

### Fixed

- Fixed stuff.

### Security

- Security related fix.
-->

## Unreleased

### Changed

- The metadata parser can now be specified with the configuration key `metadata_parser`. Accepted values are `ffprobe` (default), `mediainfo`, or `null` (for testing only).
- Songs with instrumental version are specified either with the `instrumental_file` field, if there is an audio file of the same name in the same directory as the video file, or with the `instrumental_track` field, if the video file has a second audio track. Both fields are sent to the server, instead of the `has_instrumental` field (see removed sub-section).

### Removed

- Dropped Python 3.9.
- Removed the `has_instrumental` field of songs, in favor of `instrumental_file` and `instrumental_track`.

### Fixed

- Matroshka files containing only an audio track and having the `.mka` extension are correctly detected as adio files.

## 1.9.0 - 2025-03-06

### Added

- Added Python 3.13 support.
- MacOS support.
- Added Python 3.12 support.

### Removed

- Dropped Python 3.8 support.
- Dropped Python 3.7 support.

## 1.8.0 - 2022-11-23

### Update notes

The project uses now a library to manage user directories on the different operating systems, the location was modified for Windows:

```cmd
# cmd
mkdir %APPDATA%\DakaraProject
move %APPDATA%\Dakara %APPDATA%\DakaraProject\dakara
# powershell
mkdir $env:APPDATA\DakaraProject
mv $env:APPDATA\Dakara $env:APPDATA\DakaraProject\dakara
```

### Added

- Automatically prune artists and works without songs on server.
- Feed tags with command `dakara-feeder feed tags`.
- Feed work types with command `dakara-feeder feed work-types`.
- Feed works with command `dakara-feeder feed works`.
- Support Python 3.10 and 3.11.

### Changed

- Name of the command changed from `dakara-feed` to `dakara-feeder`.
- Feed command for songs changed from `dakara-feed` to `dakara-feeder feed songs`.
- Custom song class can be indicated in configuration file with a file name: `custom_song_class: path/to/file.py::MySong`.

## 1.7.0 - 2021-06-20

### Removed

- Dropped support of Python 3.5 and 3.6.

## 1.6.0 - 2020-09-05

### Added

- Detect instrumental tracks.

## 1.5.1 - 2019-12-06

### Fixed

- A subtitle file from which lyrics can't be parsed no longer halts the feed process but only logs an error.
- A video file from which duration can't be extracted no longer halts the feed process but only logs an error.

## 1.5.0 - 2019-12-05

### Added

- First version.
