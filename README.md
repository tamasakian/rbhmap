# rbhmap

**RBHMAP**: A Reciprocal Best Hit Mapping Tool.

## Version
Current version: `v1.0.0`

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


