# MultiPathFS
Map a list of dirs/drives in one mountpoint using FUSE and Python.

A prede

## Usage
### Configure

*config - contains all paths to be used*

Cofigure as: 

First line is mountpoint

All subsequent lines must contain only one path

Example:
```
mountpoint
directory01/myfolder
directory03/directory02
```

### Run script

*extended_multipath.py - main python script*

Run using: 
```
./extended_multipath.py

```

The script has a shebang and can be executed as is without parameters.

### Conventions

Mountpoint root dir operations are always routed to first path mapped.

Operations inside a folder in the mountpoint will remain on the original mapped path.

Ranaming/Linking a folder on the mountpoit root will keep the original path.

## This software uses Python and requires the following libraries

- Pyfuse
	```
	pip3 install fusepy==3.0.1
	```
	


