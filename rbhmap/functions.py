#!/usr/bin/env python3

from rbhmap import utils

"""
Function Library for RBHMAP.

Functions:
    blast: Map the Reciprocal Best Hit (RBH) from BLAST results.
"""

def blast(blast_file: str, map_file:str) -> None:
    """
    Map the Reciprocal Best Hit (RBH) from BLAST results.

    Args:
        blast_file: Path to the input BLAST file.
        map_file:   Path to the output TSV file containing RBH pairs.
    """
    blast_results = utils.parse_blast_file(blast_file=blast_file)
    rbh_pairs = utils.extract_rbh_pairs(results=blast_results)
    utils.write_map_file(map_file=map_file, rbh_pairs=rbh_pairs)
