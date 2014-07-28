#!/usr/bin/env python

from datetime import datetime
import difflib
import subprocess
import docopt
import termcolor


class Wattic:
    def __init__(self, cli):
        self.args = docopt.docopt(cli.strip())
        self.now = datetime.utcnow().strftime('%Y%m%d-%H%M%S')

        if self.args['create']:
            self.create()
        elif self.args['diff']:
            self.diff()

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

    def diff(self):
        cmd = [
            'attic',
            'list',
            self.args['<repository>'],
        ]
        cmd_output = subprocess.check_output(cmd).decode('utf-8').strip()
        archives_list = [arc.split()[0] for arc in cmd_output.split('\n')]
        if self.args['<first-archive>'] and self.args['<second-archive>']:
            first_archive = self.args['<first-archive>']
            second_archive = self.args['<second-archive>']
            for archive in [first_archive, second_archive]:
                if archive not in archives_list:
                    print(
                        'Archive {archive} was not found in the repository'
                        .format(archive=archive)
                    )
                    exit(1)
        else:
            if len(archives_list) < 2:
                print('At least two archives are needed for comparison')
                exit(1)
            first_archive = archives_list[-2]
            second_archive = archives_list[-1]
        archives = [first_archive, second_archive]
        outputs = []
        for archive in archives:
            cmd = [
                'attic',
                'list',
                '{repository}::{archive}'.format(
                    archive=archive,
                    repository=self.args['<repository>'],
                ),
            ]
            output = subprocess.check_output(cmd).decode('utf-8').strip()
            file_list = output.split('\n')
            outputs.append(file_list)
        first_output, second_output = outputs
        differ = difflib.Differ()
        for line in differ.compare(first_output, second_output):
            if line.startswith('+'):
                print(termcolor.colored(line, 'green'))
            elif line.startswith('-'):
                print(termcolor.colored(line, 'red'))


def main():
    cli = '''
    A thin wrapper around the Attic Deduplicating Archiver.

    Usage:
        wattic create <repository> <folder>
        wattic diff <repository> [(<first-archive> <second-archive>)]
    '''
    Wattic(cli)

if __name__ == '__main__':
    main()
