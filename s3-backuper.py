#!/usr/bin/env python

from sys import stdout
from os import listdir
from os.path import isfile, join, getsize, getctime
import time

from plumbum.cmd import aws, ls, grep, mv, mkdir, rm
from plumbum import cli


s3 = aws["s3"]

class MyApp(cli.Application):

    VERSION = "0.0.1"

    verbose = cli.Flag(["v", "verbose"], help = "Verbose output")
    keepCount = cli.SwitchAttr(["k", "keep"], int, default = 10, help = "Max count of backup files to be kept")

    def main(self, srcDir, dstBucket, dstDir):
        # protect to prevent deleting of all backups
        if self.keepCount < 2:
            self.keepCount = 2

        s3DirPath = "s3://" + dstBucket + "/" + dstDir
        if self.verbose:
            print("Sending backups from", srcDir, "to", s3DirPath, flush = True)

        # check if bucket exists and create if not
        lines = (s3["ls"] | grep[dstBucket])().splitlines()
        if not lines:
            if self.verbose:
                print("Bucket doesn't exist. Creating...")
            (s3["mb", "s3://" + dstBucket] > stdout)()

        # create dir for processed backup files (if not exists)
        processedDir = join(srcDir, "_processed")
        mkdir("-p", processedDir)

        # process new files
        for f in listdir(srcDir):
            fullPath = join(srcDir, f)
            if isfile(fullPath) and getsize(fullPath) > 0:
                datePrefix = time.strftime("%Y-%m-%d-", time.localtime(getctime(fullPath)))
                processedFileName = datePrefix + f
                mv(fullPath, join(processedDir, processedFileName))

        # remove old backups, keep only requested count (--keep)
        for f in ls("-c", processedDir).splitlines()[self.keepCount:]:
            if self.verbose:
                print("Removing old backup", f, flush = True)
            rm(join(processedDir, f))

        # sync to s3
        (s3["sync", processedDir, s3DirPath, "--storage-class", "STANDARD_IA", "--delete"] > stdout)()


if __name__ == "__main__":
    MyApp.run()
