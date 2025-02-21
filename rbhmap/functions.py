#!/usr/bin/env python3

from rbhmap import utils

"""
Function Library for RBHMAP.

Functions:
    blast: Map the Reciprocal Best Hit (RBH) from BLAST results.
    map2split: Split a map file into foreground and background RBH pairs based a seq_file.
    map2colin: Extract RBH from a synteny file.
"""

def blast(blast_file: str, map_file: str) -> None:
    """
    Map the Reciprocal Best Hit (RBH) from BLAST results.

    Args:
        blast_file: Path to the input BLAST file.
        map_file:   Path to the output TSV file containing RBH pairs.
    """
    blast_results = utils.parse_blast_file(blast_file=blast_file)
    rbh_pairs = utils.extract_rbh_pairs(results=blast_results)
    utils.write_map_file(map_file=map_file, rbh_pairs=rbh_pairs)

def map2split(map_file: str, seq_file: str, output_basename: str) -> None:
    """
    Split a map file into foreground and background RBH pairs based a seq_file.

    Args:
        map_file:
            Path to the input TSV file containing RBH pairs.
        seq_file:
            Path to the input text file containing Sequence IDs to split.
        output_basename:
            Path to the output TSV files without extension.
    """
    sequence_set = utils.parse_seq_file(seq_file=seq_file)
    fg, bg = utils.split_pairs(map_file=map_file, seqs=sequence_set)
    utils.write_map2split_files(output_basename=output_basename, foreground_list=fg, background_list=bg)

def map2colin(map_file: str, colin_file: str, output_file: str) -> None:
    """
    Extract RBH from a synteny file.

    Args:
        map_file:
            Path to the input TSV file containing RBH pairs.
        colin_file:
            Path to the input synteny file from MCScanX.
        output_file:
            Path to the output synteny files.
    """
    rbh_list = utils.parse_map_file(map_file=map_file)
    synteny_dict = utils.parse_colin_file(colin_file=colin_file)
    utils.write_map2colin_file(pairs=rbh_list, results=synteny_dict, output_file=output_file)
