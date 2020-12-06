#!/usr/bin/python3


import MDSplus
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
from time import time
from functools import wraps
#from pympler.tracker import SummaryTracker
#tracker = SummaryTracker()


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('TIMING:func:%r took: %2.5f sec' % (f.__name__, te-ts))
        return result
    return wrap


def get_args():
    parser = argparse.ArgumentParser(description="jScope file creator.")
    parser.add_argument('--shot', default=0, type=int,
                        help='specify shot number')
    parser.add_argument('--start', default=0, type=int,
                        help='Which shot num to start at.')
    parser.add_argument('--stop', default=500, type=int,
                        help='Which shot num to stop at.')
    parser.add_argument('--th', default=0.09, type=float,
                        help='Transition threshold for edge detect. Default = 0.09V.')
    parser.add_argument('--dprint', default=0, type=int,
                        help='Print extended debug messages.')
    parser.add_argument('--type', type=str, default='mds', help="Which type of data offload. Default=mds, other option is blob.")
    parser.add_argument('uuts', nargs='+', help="uut list")
    return parser.parse_args()


# @timing
def load_blob_data(shot, uut):
    data = np.fromfile("/home/dt100/MR_DATA/{}.{}.dat".format(uut, shot), dtype=np.int16)
    data = data.reshape((48,-1))
    print(data.shape)
    # plt.plot(data[0])
    # plt.grid(1)
    # plt.show()
    return data


def get_blob_data(uuts, shot_start, shot_end):
    df = pd.DataFrame(index=np.arange(0,48*26*((shot_end+1) - shot_start)),
        columns=["shot", "uut", "chan", "rms", "min", "max", "std",
        "first_edge", "last_edge", "total_edges", "jog_samples",
        "run_samples", "sprint_samples"])

    print(df.shape)
    counter = 0

    for shot in range(shot_start, shot_end+1):
        for uut in uuts:
            channels = load_blob_data(shot, uut)
            file = "/home/dt100/MR_DATA/{}.{}.dec".format(uut, shot)
            # print(file)
            decims = np.fromfile(file, dtype=np.uint8)
            jrs = get_nsamples_jrs(decims)
            for chan, data in enumerate(channels):
                print(chan)
                edge_data = get_first_last_total_edges(data)
                data = analyse_open_circuit(data)
                df.loc[counter] = (shot, uut, chan, *data, *edge_data, *jrs)
                counter += 1

                if counter % 100 == 0:
                    print(counter)

    return None


def get_mdsplus_data(uuts, shot_start, shot_end):
    uuts_real = []
    uut_data = []
    oc_data = []
    total_data = []

    df = pd.DataFrame(index=np.arange(0,48*26*((shot_end+1) - shot_start)),
        columns=["shot", "uut", "chan", "rms", "min", "max", "std",
        "first_edge", "last_edge", "total_edges", "jog_samples",
        "run_samples", "sprint_samples"])

    print(df.shape)
    counter = 0

    for shot in range(shot_start, shot_end+1):
        for num, uut in enumerate(uuts):
            # try:
            tree = MDSplus.Tree(uut, shot)
            # print("Get Tree:", time.process_time() - start)
            try:
                decims = tree.TRANSIENT1.DECIMS.data()
            except Exception:
                for chan in range(1,49):
                    df.loc[counter] = (shot, uut, chan, *np.array([np.nan]*10))
                    counter += 1
                continue

            jrs = get_nsamples_jrs(decims)
            for chan in range(1,49):
                try:
                    data = load_mdsplus_data(tree, chan)
                except Exception:
                    df.loc[counter] = (shot, uut, chan, *np.array([np.nan]*10))
                    counter += 1
                    continue
                edge_data = get_first_last_total_edges(data)
                data = analyse_open_circuit(data)
                df.loc[counter] = (shot, uut, chan, *data, *edge_data, *jrs)
                if counter % 100 == 0:
                    print(counter)
                    # print(shot, uut, chan, *data, *edge_data, *jrs)
                    # print(df.head())
                counter += 1

    print(df.shape)
    df.to_csv("{}_to_{}_df.csv".format(shot_start, shot_end))
    # # uut_data = np.array(uut_data)
    return np.array(uut_data), uuts_real


# @timing
def load_mdsplus_data(tree, chan):
    data = getattr(tree.TRANSIENT1, "INPUT_{:03d}".format(chan)).CAL_INPUT.data()
    return data


def dprint(message):
    if _dprint:
        print(message)

# @timing
def analyse_open_circuit(channel):
    rms = np.sqrt(np.mean(channel**2))
    mn = np.min(channel)
    mx = np.max(channel)
    sd = np.std(channel)
    return [rms, mn, mx, sd]

# @timing
def remove_consec_incrs(array):
    non_consec = []
    for index, item in enumerate(array[0]):
        # if item != array[0][index-1]+100:
        if item > array[0][index-1]+30:
            non_consec.append(item)
    return non_consec

# @timing
def get_first_last_total_edges(channel, threshold=0.1):
    # plt.plot(channel)
    # plt.grid(1)
    # plt.show()
    diffs = np.abs(np.diff(channel))
    # plt.plot(where)
    # plt.grid(1)
    # plt.show()
    where = np.where(diffs > threshold, 1, 0)
    # remove_consec_incrs
    # plt.plot(where)
    # plt.grid(1)
    # plt.show()
    # print("DEBUGGER: ", (where == 1).sum())
    if (where == 1).sum() == 0:
        first = np.nan
        last = np.nan
        total = 0
        return [first, last, total]
    else:
        arr = np.argwhere(where == 1).T
        first = arr[0][0]
        last = arr[-1][0]
        total = remove_consec_incrs(arr)
        # print("DEBUGGER: ", total)
        total = len(total)
        return [first, last, total]

# @timing
def get_nsamples_jrs(decims):
    j = np.sum(decims == 20)
    r = np.sum(decims == 2)
    s = np.sum(decims == 1)

    return [j, r, s]


def main():
    args = get_args()
    global _dprint
    _dprint = args.dprint
    #uuts = os.walk("/home/dt100/TREES/")
    # uut_dirs = [item[0] for item in os.walk("/home/dt100/TREES/")][1:]
    # uut_list = [item.split("/")[-1] for item in uut_dirs]

    if args.type == "mds":
        data, uut_list = get_mdsplus_data(args.uuts, args.start, args.stop)
    elif args.type == "blob":
        data, uut_list = get_blob_data(args.uuts, args.start, args.stop)
    # for shot in range(args.start, args.stop + 1):
        #    shot = args.shot
        # dprint("=================================")
        # dprint(shot)
        # compare_data(data, uut_list, shot, args.th)


if __name__ == '__main__':
    main()
    # tracker.print_diff()
