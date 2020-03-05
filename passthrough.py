#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations


class Passthrough(Operations):
    def __init__(self, root):
        self.root = root

    # Helper
    # =======

    def _full_path(self, partial):
        '''
        Used by any function to understand where to operate.
        In this case, map partial path to the only root path.

        in ex: mydocs/2020/file.doc
        out ex: rootpath/mydocs/2020/file.doc
        '''
        print("Call: _full_path")
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        print("Call: access")
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        print("Call: chmod")
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        print("Call: chown")
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        print("Call: getattr")
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid', 'st_blocks'))

    def readdir(self, path, fh):
        print("Call: readdir")
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        print("Call: readlink")
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        print("Call: mknod")
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        print("Call: rmdir")
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        print("Call: mkdir")
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        print("Call: statfs")
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        print("Call: unlink")
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        print("Call: symlink")
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        print("Call: rename")
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        print("Call: link")
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        print("Call: utimens")
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        print("Call: open")
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        print("Call: create")
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        print("Call: read")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print("Call: write")
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        print("Call: truncate")
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        print("Call: flush")
        return os.fsync(fh)

    def release(self, path, fh):
        print("Call: release")
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        print("Call: fsync")
        return self.flush(path, fh)


def main(mountpoint, root):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)


if __name__ == '__main__':
    '''
    This file can be run standalone.
    '''
    main(sys.argv[2], sys.argv[1])
