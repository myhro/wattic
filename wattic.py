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
        if self.args['<archive>'].endswith('/'):
            self.args['<archive>'] = self.args['<archive>'][:-1]

        cmd = [
            'attic',
            'create',
            '--stats',
            '{archive}::{name}'.format(
                archive=self.args['<archive>'],
                name=self.now,
            ),
            '{folder}'.format(folder=self.args['<folder>']),
        ]
        subprocess.call(cmd)

def main():
    cli = '''
    Usage:
        wattic create <archive> <folder>
    '''
    Wattic(cli)

if __name__ == '__main__':
    main()
