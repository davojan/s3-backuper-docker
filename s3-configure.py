#!/usr/bin/env python

import sys
from plumbum.cmd import mkdir, cat, ls
from plumbum import local, cli, colors


class MyApp(cli.Application):
    PROGNAME = colors.green
    VERSION = "0.0.1"

    verbose = cli.Flag(["v", "verbose"], help = "If given, I will be very talkative")

    def main(self):
        mkdir("-p", "~/.aws")
        # save aws credentials
        credentials = awsCredentials(key = local.env["AWS_ID"], secret = local.env["AWS_SECRET"])
        ((cat << credentials) > "~/.aws/credentials")()
        # save aws region config
        config = awsConfig(region = local.env["AWS_REGION"])
        ((cat << config) > "~/.aws/config")()


def awsCredentials(key, secret):
    return '''[default]
aws_access_key_id=%s
aws_secret_access_key=%s''' % (key, secret)

def awsConfig(region):
    return '''[default]
region=%s
output=json''' % region


if __name__ == "__main__":
    MyApp.run()
