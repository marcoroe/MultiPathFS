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

    def _full_path(self, partial, lista=False):
        '''
        Helper function that decide the path to use
        for the requested operation from FUSE

        in: partial path requested
        out: full os path for operation
        '''
        print("Call: _full_path Inherited with: ", partial)
        if partial.startswith("/"):
            partial = partial[1:]

        # Search if path exist
        valid_path = []
        valid_dirs = []
        for path in self.mypaths:
            full = os.path.join(path, partial)
            fuld = os.path.dirname(full)
            # print("Evaluating: " + full)
            if os.path.exists(full):
                valid_path.append(full)
            if os.path.exists(fuld):
                valid_dirs.append(fuld)

        # If still nothing found default to the first path.
        if len(valid_path) == 0:
            if len(valid_dirs) > 0:
                full = os.path.join(valid_dirs[0], os.path.basename(partial))
                print("Appending valid folders: ", full)
                valid_path.append(full)
            else:
                print("Appending default path: ", full)
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
        for dirs in self._full_path(path, True):
            if os.path.isdir(dirs):
                dirents.extend(os.listdir(dirs))
        for r in list(set(dirents)):
            yield r

    def rename(self, old, new):
        print("Call: rename")
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        print("Call: link")
        return os.link(self._full_path(target), self._full_path(name))


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
