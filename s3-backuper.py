#!/usr/bin/env python

from plumbum.cmd import aws, ls
from plumbum import cli, colors
import sys


s3 = aws["s3"]

class MyApp(cli.Application):
    PROGNAME = colors.green
    VERSION = "0.0.1"

    verbose = cli.Flag(["v", "verbose"], help = "If given, I will be very talkative")

    def main(self, srcDir, dstBucket, dstPath):
        print(s3("ls"))
        if self.verbose:
            print("Yadda " * 200)


if __name__ == "__main__":
    MyApp.run()
