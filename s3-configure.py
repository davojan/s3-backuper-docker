#!/usr/bin/env python

import sys
from plumbum.cmd import mkdir, cat
from plumbum import cli


CONFIG_DIR = "/root/.aws"

class MyApp(cli.Application):

    VERSION = "0.0.1"

    verbose = cli.Flag(["v", "verbose"], help = "If given, I will be very talkative")

    def main(self, awsId, awsSecret, awsRegion):
        mkdir("-p", CONFIG_DIR)
        # save aws credentials
        credentials = awsCredentials(id = awsId, secret = awsSecret)
        ((cat << credentials) > CONFIG_DIR + "/credentials")()
        # save aws region config
        config = awsConfig(region = awsRegion)
        ((cat << config) > CONFIG_DIR + "/config")()


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
