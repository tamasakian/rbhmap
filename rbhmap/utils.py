#!/usr/bin/env python3

import sys
from collections import defaultdict

"""
Function Library for functions.

Functions:
    parse_blast_file: Parse blast_file to generate a list of parsed rows.
    extract_rbh_pairs: Extract reciprocal best hits (RBH) from BLAST results.
    load_prefix: Load and sort unique prefixes from the RBH pairs.
    write_map_file: Write the reciprocal best hit (RBH) pairs to map_file.
    parse_seq_file: Parse seq_file to generate a set of Sequence IDs.
    split_pairs: Parse map_file and split mapping RBH pairs.
    write_map2split_files: Write two foreground and background RBH pairs to output_file.
"""

def parse_blast_file(blast_file: str) -> list:
    """
    Parse blast_file to generate a list of parsed rows.

    Args:
        blast_file: Path to the input BLAST result file.

    Returns:
        List of tuples containing parsed BLAST results.
    """
    results = []
    with open(blast_file, mode="r") as blast_handle:
        for line in blast_handle:
            if line.startswith("#"):
                continue
            li = line.strip().split("\t")
            if len(li) != 12:
                sys.stderr.write(f"Warning: Skipping malformed row (expected 12 columns, found {len(li)}): {line}\n")
                continue
            try:
                qseqid, sseqid, _, _, _, _, _, _, _, _, _, bitscore = li
                bitscore = float(bitscore)
            except ValueError:
                sys.stderr.write(f"Error: Invalid numeric value in row: {line}\n")
                continue
            results.append((qseqid, sseqid, bitscore))
    return results

def extract_rbh_pairs(results: list) -> set:
    """
    Extract reciprocal best hits (RBH) from BLAST results.

    Args:
        results: List of tuples containing parsed BLAST results.

    Returns:
        Set containing RBH pairs.
    """
    best_hits = {}
    for qseqid, sseqid, bitscore in results:
        q_prefix, s_prefix = qseqid.split("_", 1)[0], sseqid.split("_", 1)[0]
        if q_prefix == s_prefix:
            continue
        if qseqid not in best_hits or bitscore > best_hits[qseqid][1]:
            best_hits[qseqid] = (sseqid, bitscore)

    reciprocal_best_hits = defaultdict(list)
    for qseqid, (sseqid, _) in best_hits.items():
        if sseqid in best_hits and best_hits[sseqid][0] == qseqid:
            reciprocal_best_hits[qseqid].append(sseqid)

    rbh_pairs = set()
    for qseqid, sseqids in reciprocal_best_hits.items():
        for sseqid in sseqids:
            rbh_pairs.add(tuple(sorted([qseqid, sseqid])))
    return rbh_pairs


def load_prefix(rbh_pairs: set) -> list:
    """
    Load and sort unique prefixes from the RBH pairs.

    Args:
        rbh_pairs: Set of RBH pairs.

    Returns:
        A sorted list of unique prefixes.
    """
    prefixes = []
    for rbh1, rbh2 in rbh_pairs:
        rbh1_prefix = rbh1.split("_")[0]
        rbh2_prefix = rbh2.split("_")[0]
        prefixes.append(rbh1_prefix)
        prefixes.append(rbh2_prefix)

    unique_prefixes = set(prefixes)
    sorted_prefixes = sorted(unique_prefixes)
    if len(sorted_prefixes) != 2:
        sys.stderr.write("Warning: Expected exactly 2 unique prefixes.\n")
        return
    return sorted_prefixes


def write_map_file(map_file: str, rbh_pairs: set) -> None:
    """
    Write the reciprocal best hit (RBH) pairs to map_file.

    Args:
        map_file: Path to the output file.
        rbh_pairs: Set of RBH pairs.
    """
    if not rbh_pairs:
        sys.stderr.write("Warning: No reciprocal best hits found.\n")
        return

    ordered_prefixes = load_prefix(rbh_pairs)
    if len(ordered_prefixes) != 2:
        sys.stderr.write("Warning: Expected exactly 2 unique prefixes.\n")
        return

    ordered_pairs = []
    for rbh1, rbh2 in rbh_pairs:
        rbh1_prefix, rbh1_suffix = rbh1.split("_", 1)
        rbh2_prefix, rbh2_suffix = rbh2.split("_", 1)
        if rbh1_prefix < rbh2_prefix:
            ordered_pairs.append((rbh1_suffix, rbh2_suffix))
        else:
            ordered_pairs.append((rbh2_suffix, rbh1_suffix))

    with open(map_file, mode="w") as map_handle:
        map_handle.write("# Reciprocal Best Hits\n")
        map_handle.write(f"#\t{"\t".join(ordered_prefixes)}\n")
        for ordered_pair in ordered_pairs:
            map_handle.write(f"{"\t".join(ordered_pair)}\n")

def parse_seq_file(seq_file: str) -> set:
    """
    Parse seq_file to generate a set of Sequence IDs.

    Args:
        seq_file:
            Path to the input text file.

    Returns:
        set: A set of Sequence IDs parsed from seq_file.
    """
    seqs = set()
    with open(seq_file, "r") as seq_handle:
        for line in seq_handle:
            if line.startswith("#"):
                continue
            seq_name = line.strip()
            seqs.add(seq_name)
    return seqs

def split_pairs(map_file: str, seqs: set) -> list:
    """
    Parse map_file and split mapping RBH pairs.

    Args:
        map_file:
            Path to the input TSV file containing RBH pairs.
        seqs:
            A set of Sequence IDs.

    Returns:
        Two list included foreground RBH pairs and background RBH pairs.
    """
    foreground = []
    background = []
    with open(map_file, "r") as map_handle:
        for line in map_handle:
            if line.startswith("#"):
                continue
            pairs = line.strip()
            pair1, pair2 = pairs.split("\t")
            if pair1 in seqs or pair2 in seqs:
                foreground.append(pairs)
            else:
                background.append(pairs)
    return foreground, background

def write_map2split_files(output_basename: str, foreground_list: list, background_list: list) -> None:
    """
    Write two foreground and background RBH pairs to output_file.

    Args:
        output_basename:
            Path to the output TSV files without extension.
        foreground_list:
            A list of foreground RBH pairs.
        background_list:
            A list of background RBH pairs.
    """
    for group, items in zip(["foreground", "background"], [foreground_list, background_list]):
        output_file = f"{output_basename}_{group}.txt"
        with open(output_file, "w") as output_handle:
            output_handle.write("\n".join(items) + "\n")

