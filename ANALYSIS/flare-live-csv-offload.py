#!/usr/bin/python3


import MDSplus
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import time as time1
from functools import wraps
import struct



def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time1.time()
        result = f(*args, **kw)
        te = time1.time()
# comment out next line to stub timing report globally
#        print('TIMING:func:%r took: %2.5f sec' % (f.__name__, te-ts))
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
    parser.add_argument('--type', type=str, default='mds',
                        help="Which type of data offload. Default=mds, other option is blob.")
    parser.add_argument('uuts', nargs='+', help="uut list")
    return parser.parse_args()


@timing
def load_mdsplus_data(tree, chan):
    data = getattr(tree.TRANSIENT1, "INPUT_{:03d}".format(chan)).CAL_INPUT.data()
    return data


def dprint(message):
    if _dprint:
        print(message)


@timing
def analyse_open_circuit(channel):
    rms = np.sqrt(np.mean(channel**2))
    mn = np.min(channel)
    mx = np.max(channel)
    sd = np.std(channel)
    return [rms, mn, mx, sd]


@timing
def remove_consec_incrs(array):
    non_consec = []
    for index, item in enumerate(array[0]):
        if item > array[0][index-1]+30:
            non_consec.append(item)
    return non_consec


@timing
def get_first_last_total_edges(channel, threshold=0.3):
    diffs = np.abs(np.diff(channel))
#    if len(where) > 2000:
#        return ["too many diffs", "too many diffs", "too many diffs"]
    where = np.where(diffs > threshold, 1, 0)
    if (where == 1).sum() > 2000:
        return ["too many diffs", "too many diffs", "too many diffs"]



    if (where == 1).sum() == 0:
        first = np.nan
        last = np.nan
        total = 0
        return [first, last, total]
    else:
        arr = np.argwhere(where == 1).T
        first = arr[0][0]
        last = arr[-1][-1]
        total = remove_consec_incrs(arr)
        total = len(total)
        return [first, last, total]


@timing
def get_nsamples_jrs(decims):
    j = np.sum(decims == 20)
    r = np.sum(decims == 2)
    s = np.sum(decims == 1)

    return [j, r, s]


def get_df(uuts, shot):

    counter = 0
    df = pd.DataFrame(index=np.arange(0,26*48),
                      columns=["shot", "uut", "chan", "rms", "min", "max", "std",
                               "first_edge", "last_edge", "total_edges", "jog_samples",
                               "run_samples", "sprint_samples"])

    for num, uut in enumerate(uuts):
        try:
            tree = MDSplus.Tree(uut, shot)
        except Exception:
            for chan in range(1, 49):
                df.loc[counter] = (shot, uut, chan, *np.array([np.nan]*10))
                counter += 1
            continue
        # print("Get Tree:", time.process_time() - start)
        try:
            decims = tree.TRANSIENT1.DECIMS.data()
        except Exception:
            for chan in range(1, 49):
                df.loc[counter] = (shot, uut, chan, *np.array([np.nan]*10))
                counter += 1
            continue

        jrs = get_nsamples_jrs(decims)

        for chan in range(1, 49):
            try:
                data = load_mdsplus_data(tree, chan)
            except Exception:
                df.loc[counter] = (shot, uut, chan, *np.array([np.nan]*10))
                counter += 1
                continue

            edge_data = get_first_last_total_edges(data)
            data = analyse_open_circuit(data)
            df.loc[counter] = (shot, uut, chan, *data, *edge_data, *jrs)

            counter += 1
    return df


def offload_csv_data(csv_file, uuts, shot):

    df = get_df(uuts,shot)
    print("Got df")
    _header = False if (shot > first_shot) else True
    df.to_csv('flare_{}_mds_live.csv'.format(first_shot), mode='a', header=_header)
    return None


def get_shot():
    # shot = int(os.popen("get_shot acq2106_227").read().split("\n")[-2])-1
    # print(shot)
    for xx in range(500):
        try:
            with os.popen("get_shot acq2106_227") as pipe:
                shot = int(pipe.read().split("\n")[-2])-1
                return shot
        except Exception:
            print("Can't get shot right now...")
            #import time
            time1.sleep(0.5)
    return shot


def start_live(csv_file, uuts):
    # if os.path.isfile(csv_file)
    prev_shot_done = get_shot()
    global first_shot
    first_shot = prev_shot_done + 1
    while True:
        latest_shot_done = get_shot()
        print("Latest: {}".format(latest_shot_done))
        print("Previous: {}".format(prev_shot_done))
        if latest_shot_done > prev_shot_done:
            print("Offloading shot {}".format(latest_shot_done))
            offload_csv_data(csv_file, uuts, latest_shot_done)
            # continue
        prev_shot_done = latest_shot_done
        print("Sleeping")
#        import time
        time1.sleep(0.5)

    return None


def main():
    args = get_args()
    global _dprint
    _dprint = args.dprint

    # if args.type == "mds":
    # data, uut_list = get_mdsplus_data(args.uuts, args.start, args.stop)
    csv_file_loc = "/home/dt100/PROJECTS/ACQ400_MDSplus_TREESUPPORT/mds_live.csv"
    start_live(csv_file_loc, args.uuts)
    # elif args.type == "blob":
    # get_blob_data(args.uuts, args.start, args.stop)


if __name__ == '__main__':
    main()
