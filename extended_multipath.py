#!/usr/bin/env python

import os
import logging

# Requires: pip fusepy >= 3.0.0
from fuse import FUSE
from passthrough import Passthrough


class dfs(Passthrough):
    def __init__(self, mypaths):
        self.mypaths = mypaths
        self.verbose = False

    def _full_path(self, partial, lista=False):
        '''
        Helper function that decide the path to use
        for the requested operation from FUSE

        in: partial path requested
        out: full os path for operation
        '''
        if self.verbose:
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

        # File or Dir or Empty list
        if len(valid_path) == 0:
            if len(valid_dirs) > 0:
                full = os.path.join(valid_dirs[0], os.path.basename(partial))
                if self.verbose:
                    print("Appending valid folders: ", full)
                valid_path.append(full)

        if self.verbose:
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
        if self.verbose:
            print("Call: readdir Inherited")
        dirents = ['.', '..']
        # full_paths = self._full_path(path, True)
        for dirs in self._full_path(path, True):
            if os.path.isdir(dirs):
                dirents.extend(os.listdir(dirs))
        for r in list(set(dirents)):
            yield r

    def rename(self, old, new):
        '''
        Modified rename function to allow renaming without
        moving content between paths.

        in: requested name change tuple
        out: os mv operation
        '''
        if self.verbose:
            print("Call: rename Inherited")
        if os.path.dirname(old) != os.path.dirname(new):
            if self.verbose:
                print("Renaming:", old, " in ", new)
            Passthrough.rename(self, old, new)
        else:
            old_path = self._full_path(old)
            old_dir = os.path.dirname(old_path)
            new_path = old_dir + new
            if self.verbose:
                print("Renaming:", old_path, " in ", new_path)
            return os.rename(old_path, new_path)


def main(mountpoint, paths):
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

    print("MultiPathFS: Operating with: " + str(path_list))

    # Enable logging if needed
    logging.basicConfig(level=logging.WARN)

# Call for main(mountpoint, paths)
main(path_list[0], path_list[1:])
