#!/usr/bin/env python3
# coding=utf-8

"""A tool to find duplicate files
"""
from __future__ import unicode_literals, print_function
import os
import argparse
import logging
from collections import defaultdict
from hashlib import md5

__AUTHOR__ = 'Igor Tsarev'
__VERSION__ = '0.1'


def _flat_tree(tree):
    for _, val_list in tree.items():
        for val in val_list:
            yield val


def _collapse_lonely(tree):
    return {k: v for (k, v) in tree.items() if len(v) > 1}


class Comparator():
    def __init__(self, dirs, verbose):
        self.dirs = dirs
        debug_level = logging.ERROR
        if verbose:
            debug_level = logging.INFO
        logging.basicConfig(
            level=debug_level,
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%H:%M:%S'
        )
        self.logger = logging.getLogger()

    def compare(self):
        files = self.get_files()
        count = self.print_dupes(
            # compare files by hash. Very slow
            self.compare_by_hash(
                # compare files by slice of bytes from file. Fast
                self.by_same_chunk(
                    # compare files by their sizes. Very fast
                    self.by_same_size(files)
                )
            )
        )
        self.logger.info(
            "Total duplicates: {} (without original file)".format(count)
        )

    def get_files(self):
        """ Get all files recursively from dirs
        :param dirs: list of directories
        """
        file_tree = defaultdict(list)
        count = 0
        for directory in self.dirs:
            for path, _, files in os.walk(directory):
                for name in files:
                    file_tree[directory].append(os.path.join(path, name))
                    count += 1
        self.logger.info("Total files: {}".format(count))
        return file_tree

    def by_same_size(self, file_tree):
        size_tree = defaultdict(list)
        for file_path in _flat_tree(file_tree):
            size_tree[os.path.getsize(file_path)].append(file_path)
        filtered = _collapse_lonely(size_tree)
        self.logger.info("Files after size checking: {}".format(
            len(list(_flat_tree(filtered))))
        )
        return filtered

    def by_same_chunk(self, file_tree, chunk_size=8):
        """
        :param files:
        :return:
        """
        chunk_tree = defaultdict(list)

        for size, files in file_tree.items():
            prev_chunk = None
            for file_name in files:
                with open(file_name, 'rb') as f:
                    f.seek(int(size/2))  # Center of file
                    chunk = f.read(chunk_size)
                    if prev_chunk is None or prev_chunk == chunk:
                        chunk_tree[size].append(file_name)
                    prev_chunk = chunk
        filtered = _collapse_lonely(chunk_tree)
        self.logger.info("Files after chunk checking: {}".format(
            len(list(_flat_tree(filtered)))
        ))
        return filtered

    def compare_by_hash(self, file_tree):
        hash_tree = defaultdict(list)
        for file_path in _flat_tree(file_tree):
            with open(file_path, 'rb') as f:
                hash_tree[md5(f.read()).hexdigest()].append(file_path)
        return _collapse_lonely(hash_tree)

    def print_dupes(self, dupes):
        dupes_count = 0
        for file_hash, files in dupes.items():
            for file_name in files:
                print("{} duplicate {}".format(file_hash, file_name))
            dupes_count += len(files)-1
        return dupes_count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find duplicates of files'
    )
    parser.add_argument('dirs', metavar='D', type=str, nargs='+',
                        help='directories to search')
    parser.add_argument('-v', '--verbose', type=bool, help="Be verbose",
                        default=False)
    comparator = Comparator(**vars(parser.parse_args()))
    comparator.compare()


