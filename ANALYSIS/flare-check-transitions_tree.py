#!/usr/bin/python3


import MDSplus
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from sklearn.ensemble import IsolationForest
#from pympler.tracker import SummaryTracker
#tracker = SummaryTracker()


def get_args():
    parser = argparse.ArgumentParser(description="jScope file creator.")
    parser.add_argument('--shot', default=0, type=int,
                        help='specify shot number')
    parser.add_argument('--start', default=0, type=int,
                        help='Which shot num to start at.')
    parser.add_argument('--stop', default=500, type=int,
                        help='Which shot num to stop at.')
    parser.add_argument('--dprint', default=0, type=int,
                        help='Print extended debug messages.')
    parser.add_argument('uuts', nargs='+', help="uut list")
    return parser.parse_args()


def get_mdsplus_data(uuts, shot):
    uut_data = []
    for uut in uuts:
        try:
            data = MDSplus.Tree(uut, shot)
            data = data.TRANSIENT1.INPUT_001.CAL_INPUT.data()
            uut_data.append(data)
            dprint("UUT: {} in shot {}. Data length: {}".format(
                uut, shot, len(data)))
        except:
            continue
    return np.array(uut_data)


def remove_consec_incrs(array):
    non_consec = []
    # print(array[0])
    for index, item in enumerate(array[0]):
        # if item != array[0][index-1]+100:
        if item > array[0][index-1]+30:
            non_consec.append(item)
    return non_consec


def dprint(message):
    if _dprint:
        print(message)


def compare_data(data, uuts, shot):
    transition_locations = []
    try:

        for num, channel in enumerate(data):

            diffs = np.diff(channel)
            where = np.where(diffs < -0.2, 1, 0)
            # for index, num in enumerate(where):
            #    if where[index-1] == 1:
            #        where[index] = 0
            transition_locations.append(where)

        for index, array in enumerate(transition_locations[1:]):
            # if not np.array_equal(transition_locations[0], array):
            arr1 = np.transpose(np.argwhere(
                transition_locations[0] == 1))
            arr2 = np.transpose(np.argwhere(
                # transition_locations[index-1] == 1))
                array == 1))

            arr1 = remove_consec_incrs(arr1)
            arr2 = remove_consec_incrs(arr2)

            if len(arr1) != len(arr2):
                print("keep {}".format(shot))
                dprint("ERROR_CODE1: Locations of transitions not the same size.")
                dprint("{} data: {}".format(uuts[0], arr1))
                dprint("{} data: {}".format(uuts[index+1], arr2))
                return
            if not np.allclose(arr1, arr2, atol=1, rtol=0):
                print("keep {}".format(shot))
                dprint("ERROR_CODE2: Found an error comparing uut: {} to {}".format(
                    uuts[0], uuts[index+1]))
                # print(uuts)
                #print("{}\n{}".format(arr1, arr2))
                return
        if shot % 100 == 0:
            print("keep {}".format(shot))
        dprint("\nNo errors found. Transitions located at the following indices: {}".format(
            arr1))
    except:
        # raise
        print("keep {}".format(shot))
        dprint("ERROR_CODE3: Found an error. Check data sizes for shot {}".format(shot))
        dprint(sys.exc_info())
    return None


def tree_compare(data, uut_list, shot):
    ch_outliers = []
    for channel in data:

        #print(data[0])
        X = np.diff(data[0][0:20000]).reshape(-1, 1)
        clf = IsolationForest(n_estimators=100, max_samples=1000, random_state=101)
        clf.fit(X)
        #preds = clf.predict(X)
        sc_sa = clf.score_samples(X)
        #plt.plot(preds, color='red')
        outliers = np.where(sc_sa < -0.8, 1, 0)
        ch_outliers.append(outliers)
        plt.plot(outliers)
        #plt.plot(X)
        #plt.grid(True)
    plt.show()
        #print(preds)
    return None


def main():
    args = get_args()
    global _dprint
    _dprint = args.dprint
    #uuts = os.walk("/home/dt100/TREES/")
    uut_dirs = [item[0] for item in os.walk("/home/dt100/TREES/")][1:]
    uut_list = [item.split("/")[-1] for item in uut_dirs]

    for shot in range(args.start, args.stop + 1):
        #    shot = args.shot
        dprint("=================================")
        dprint(shot)
        data = get_mdsplus_data(uut_list, shot)
        #compare_data(data, uut_list, shot)
        #print(data)
        tree_compare(data, uut_list, shot)


if __name__ == '__main__':
    main()
    # tracker.print_diff()
