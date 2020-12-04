#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse


pd.set_option("display.max_rows", None, "display.max_columns", None)


def get_args():
    parser = argparse.ArgumentParser(description="jScope file creator.")
    parser.add_argument('files', nargs='+', help="files")
    return parser.parse_args()


def main():
    args = get_args()
    df = pd.read_csv(args.files[0])
    df = df[-1000*48*26:]
    # print(df.loc[df['total_edges'] != 0])
    # c0de_fails = len(df.loc[df['total_edges'] == 1])
    # other_fails = len(df.loc[df['total_edges'] > 1])
    # print("c0de  fails: {}".format(c0de_fails))
    # print("other fails: {}".format(other_fails))
    # print(df['total_edges'].value_counts())
    # print(df.loc[df['total_edges'] > 0.0][['uut', 'shot', 'chan', 'total_edges']])#.drop_duplicates(subset = ['uut', 'shot']))
    ch01_fails(df)
    too_many_edges(df)
    std_large_fails(df)


def ch01_fails(df):
    """
    Catch fails where CH01 has no signal.
    """
    CH01s = df.loc[df['chan'] == 1]
    CH01s = CH01s.loc[(CH01s['min'] > -0.9) & (CH01s['max'] < 0.9) & (CH01s['total_edges'] != 24)]
    CH01s.drop_duplicates(subset=['shot', 'uut'])
    # ch01_fails = len(df.loc[df['total_edges'] == 1])
    print("CH01 fails (where there were no detected edges):")
    # print(len(CH01s))
    nshots = df['shot'].nunique()
    print("{} out of {}".format(len(CH01s), 26 * nshots))
    #print(CH01s)
    return None


def too_many_edges(df):
    """
    Catch fails where there were one or two edges.
    """
    # print(nshots)
    c0de_fails = df.loc[(df['total_edges'] == 1) | (df['total_edges'] == 2)]
    c0de_fails.drop_duplicates(subset=['shot', 'uut'])
    print("Single edge (c0de) fails:")
    nshots = df['shot'].nunique()
    print("{} out of {}".format(len(c0de_fails), 26 * nshots))
    #print(c0de_fails)
    return None


def std_large_fails(df):
    """
    Catch fails where the standard deviation is too high on channels > 1.
    """
    std_fails = df.loc[(df['std'] > 0.001) & (df['chan'] != 1)]
    std_fails.drop_duplicates(subset=['shot', 'uut'])
    print("Standard deviation (too large) fails:")
    # print(len(std_fails))
    nshots = df['shot'].nunique()
    print("{} out of {}".format(len(std_fails), 26 * nshots))
    print(std_fails)

    return None


if __name__ == '__main__':
    main()
