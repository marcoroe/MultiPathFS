# MultiPathFS
Map a list of dirs/drives in one mountpoint using FUSE and Python.

A predefined list of rules is applied, see Conventions below.

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

1) Mountpoint root dir operations are always routed to first path mapped in config (second row).

2) Operations inside a folder in the mountpoint will remain on the original mapped path.

3) Ranaming a folder on the mountpoit root will keep the original mapped path.
For example if you have a Folder01 inside the 5th path and you rename it in Folder01Bis, 
it will remain inside the 5th path and ignore convention number 1.

## This software uses Python and requires the following libraries

- Pyfuse
	```
	pip3 install fusepy==3.0.1
	```
	


