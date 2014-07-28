#!/usr/bin/env python

from datetime import datetime
import docopt
import subprocess


class Wattic:
    def __init__(self, cli):
        self.args = docopt.docopt(cli.strip())
        self.now = datetime.utcnow().strftime('%Y%m%d-%H%M%S')

        if self.args['create']:
            self.create()

    def create(self):
        if self.args['<repository>'].endswith('/'):
            self.args['<repository>'] = self.args['<repository>'][:-1]

        cmd = [
            'attic',
            'create',
            '--stats',
            '{repository}::{archive}'.format(
                archive=self.now,
                repository=self.args['<repository>'],
            ),
            self.args['<folder>'],
        ]
        subprocess.call(cmd)

def main():
    cli = '''
    A thin wrapper around the Attic Deduplicating Archiver.

    Usage:
        wattic create <repository> <folder>
    '''
    Wattic(cli)

if __name__ == '__main__':
    main()
