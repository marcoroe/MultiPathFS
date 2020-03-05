#!/usr/bin/env python

import os
import sys
import errno

# Requires: pip fusepy >= 3.0.0
from fuse import FUSE, FuseOSError, Operations
from passthrough import Passthrough


class dfs(Passthrough):
    def __init__(self, mypaths):
        self.mypaths = mypaths
        print("Loaded!")

    def _full_path(self, partial, lista=False):
        '''
        Helper function that decide the path to use
        for the requested operation from FUSE

        in: partial path requested
        out: full os path for operation
        '''
        print("Call: _full_path Inherited")
        if partial.startswith("/"):
            partial = partial[1:]

        # Pick first as write output
        # Apply filters here if needed
        valid_path = []
        print("Primary path: ", valid_path)
        for path in self.mypaths:
            full = os.path.join(path, partial)
            print("Evaluating: " + full)
            if os.path.exists(full):
                valid_path.append(full)
                print("Valid!")
            else:
                print("Not found!")

        # If no path has been found, it's a write operation
        # to the primary dir of the asked path.
        if len(valid_path) == 0:
            valid_path.append(os.path.join(self.mypaths[0], partial))

        print("Returning: ", valid_path)
        if lista is True:
            return valid_path
        else:
            return valid_path[0]

    def readdir(self, path, fh):
        '''
        Modified read directory to handle multi path search

        in: requested path
        out: ALL dir paths in requested path
        '''
        print("Call: readdir Inherited")
        dirents = ['.', '..']
        # full_paths = self._full_path(path, True)
        for dir in self._full_path(path, True):
            if os.path.isdir(dir):
                dirents.extend(os.listdir(dir))
        for r in list(set(dirents)):
            yield r


def main(mountpoint, paths):
    print("Loading FUSE package...")
    print(paths)
    FUSE(dfs(paths), mountpoint, nothreads=True,
         foreground=True, **{'allow_other': False})


# Read config files and start daemon
if __name__ == '__main__':
    with open("config", "r") as f:
        data = f.readlines()

    path_list = []
    for line in data:
        # Strip special chars from config file
        path_list.append(line.rstrip())

    print("Operating with: " + str(path_list))

# Call for main(mountpoint, paths)
main(path_list[0], path_list[1:])
