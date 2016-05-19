#!/usr/bin/env python

import sys
from plumbum.cmd import mkdir, cat
from plumbum import cli


class MyApp(cli.Application):

    VERSION = "0.0.1"

    verbose = cli.Flag(["v", "verbose"], help = "If given, I will be very talkative")

    def main(self, awsId, awsSecret, awsRegion):
        mkdir("-p", "~/.aws")
        # save aws credentials
        credentials = awsCredentials(id = awsId, secret = awsSecret)
        ((cat << credentials) > "~/.aws/credentials")()
        # save aws region config
        config = awsConfig(region = awsRegion)
        ((cat << config) > "~/.aws/config")()


def awsCredentials(id, secret):
    return '''[default]
aws_access_key_id=%s
aws_secret_access_key=%s''' % (id, secret)

def awsConfig(region):
    return '''[default]
region=%s
output=json''' % region


if __name__ == "__main__":
    MyApp.run()
