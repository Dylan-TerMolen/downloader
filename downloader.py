#!/usr/bin/python

import sys
import os
import requests
import multiprocessing


def download_range_of_bytes(start_bytes, end_bytes, url, out_file):
    """Download a range of the contents of a file
    given a url and the range of bytes to read"""

    headers = {'Range': 'bytes=%d-%d' % (start_bytes, end_bytes)}
    req = requests.get(url, headers=headers, stream=True)
    with open(out_file, "r+b") as file:
        file.seek(start_bytes)
        file.write(req.content)


def download_file(url, nThreads):
    """Download a file concurrently given a url
    and a number of threads to use"""

    req = requests.head(url)
    file_size = int(req.headers["Content-Length"])
    size_per_thread = file_size // nThreads
    try:
        filename = url.split("/")[-1]
    except:
        filename = "outfile"

    with open(filename, "wb") as outfile:
        outfile.write(b'\0' * file_size)
    try:
        for i in range(nThreads):
            start_byte = size_per_thread * i
            end_byte = start_byte + size_per_thread
            p = multiprocessing.Process(
                    target=download_range_of_bytes,
                    args=(start_byte, end_byte, url, filename)
                )
            p.start()

        print(filename, "was downloaded successfully")

    except requests.exceptions.RequestException as e:
        # Aim for atomic downloads
        os.remove(filename)
        sys.exit(1)


def main():
    # Parse command line arguments
    # If only url provided, then use 1 process
    try:
        url = sys.argv[1]
        if len(sys.argv) > 2:
            nThreads = int(sys.argv[3])
        else:
            nThreads = 1
    except:
        print("You failed to provide the required arguments")
        print("Run as ./downloader <URL>")
        print("or run as ./downloader <URL> -c numThreads")
        sys.exit(1)

    download_file(url, nThreads)


if __name__ == "__main__":
    main()
