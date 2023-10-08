# download-bookmarks

Generate archives for all your Pinboard bookmarks

## Installation

- Install [webarchier]():

  ```bash
  brew install webarchiver
  ```

- Install download-bookmarks:

  ```bash
  git clone https://github.com/jbmorley/download-bookmarks.git
  cd download-bookmarks
  pipenv install
  ```

- Set the `DOWNLOAD_BOOKMARKS_PINBOARD_API_TOKEN` to your [Pinboard API key](https://pinboard.in/settings/password) in your RC file of choice (e.g., `~/.zshrc`):

  ```bash
  export DOWNLOAD_BOOKMARKS_PINBOARD_API_TOKEN=XXX
  ```

## Usage

```
usage: download-bookmarks.py [-h] [-l LIMIT] destination

positional arguments:
  destination

options:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
```
