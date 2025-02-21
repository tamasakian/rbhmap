# rbhmap

**RBHMAP**: A Reciprocal Best Hit Mapping Tool.

## Version
Current version: `v1.2.0`

## Install

```
pip3 install git+https://github.com/tamasakian/rbhmap.git
```

If you want to install in editable mode,

```
pip3 install -e git+https://github.com/tamasakian/rbhmap.git#egg=rbhmap
```

## Usage

Create a gene mapping file using all-to-all BLAST results.

```
python3 -m rbhmap blast [BLAST filename] [MAP filename]
```

Split a gene mapping file into foreground and background RBH pairs.

```
python3 -m rbhmap map2split [MAP filename] [seq filename] [output basename]
```


