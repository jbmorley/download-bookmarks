#!/usr/bin/env python3 -u

# Copyright (c) 2023 Jason Morley
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import os
import re
import subprocess
import sys
import urllib

import requests

if "DOWNLOAD_BOOKMARKS_PINBOARD_API_TOKEN" not in os.environ:
    exit("Set DOWNLOAD_BOOKMARKS_PINBOARD_API_TOKEN to your Pinboard API token.\nGet it from https://pinboard.in/settings/password.")
PINBOARD_API_TOKEN = os.environ["DOWNLOAD_BOOKMARKS_PINBOARD_API_TOKEN"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--limit", type=int)
    parser.add_argument("destination")
    options = parser.parse_args()

    print("Fetching bookmarks...")
    response = requests.get("https://api.pinboard.in/v1/posts/all",
                            params={
                                "auth_token": PINBOARD_API_TOKEN,
                                "format": "json"
                            })

    count = 0
    bookmarks = response.json()
    for index, bookmark in enumerate(bookmarks):
        url = bookmark["href"]
        url_parts = urllib.parse.urlparse(url)._replace(query='')._replace(params='')._replace(fragment='')
        pretty_url = urllib.parse.urlunparse(url_parts)
        basename = re.sub(r'^(http://|https://)', '', url, flags=re.IGNORECASE)
        basename = re.sub(r'[^a-zA-Z0-9\.]', '_', basename, flags=re.IGNORECASE)
        basename = re.sub(r'[_]*$', '', basename)
        basename = basename + ".webarchive"
        output = os.path.join(options.destination, basename)
        if not os.path.exists(output):
            count = count + 1
            print(f"[{index}/{len(bookmarks)}] {pretty_url}", end=" ")
            sys.stdout.flush()
            try:
                # Check the page exists.
                response = requests.head(url, timeout=3)
                if response.status_code == 404:
                    print("404 😭")
                    continue
                # Download the page.
                command = ["timeout", "10", "webarchiver", "-url", url, "-output", output]
                subprocess.run(command, capture_output=True, check=True)
                print("🎉")
            except (subprocess.TimeoutExpired, requests.Timeout):
                print("⏲️")
            except Exception as e:
                print("🙅‍♂️")
        if count >= options.limit:
            print("Limit reached; exiting.")
            exit()


if __name__ == "__main__":
    main()
