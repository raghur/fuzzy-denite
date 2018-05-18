#!/usr/bin/env python3
import sys
import urllib.request
import platform
dlFileName = "fuzzy-denite-linux-amd64"
if platform.system() == "Windows":
    dlFileName = "fuzzy-denite-win-amd64.exe"
version = ""
with open("relver") as f:
    version = "v" + f.read().strip()
url = "https://github.com/raghur/fuzzy-denite/releases/download/%s/%s" \
    % (version, dlFileName)
file_name = "bin/" + sys.argv[1]
print("Downloading %s to %s " % (url, file_name))
urllib.request.urlretrieve(url, file_name)
