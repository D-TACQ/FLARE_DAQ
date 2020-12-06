#!/usr/bin/python3


import MDSplus
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
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
    parser.add_argument('--th', default=0.09, type=float,
                        help='Transition threshold for edge detect. Default = 0.09V.')
    parser.add_argument('--dprint', default=0, type=int,
                        help='Print extended debug messages.')
    parser.add_argument('uuts', nargs='+', help="uut list")
    return parser.parse_args()


def get_mdsplus_data(uuts, shot):
    uuts_real = []
    uut_data = []
    for uut in uuts:
        try:
            data = MDSplus.Tree(uut, shot)
            data = data.TRANSIENT1.INPUT_001.CAL_INPUT.data()
            uut_data.append(data)
            uuts_real.append(uut)
            dprint("UUT: {} in shot {}. Data length: {}".format(
                uut, shot, len(data)))
        except:
            continue
    return np.array(uut_data), uuts_real


def remove_consec_incrs(array):
    non_consec = []
    for index, item in enumerate(array[0]):
        # if item != array[0][index-1]+100:
        if item > array[0][index-1]+30:
            non_consec.append(item)
    return non_consec


def dprint(message):
    if _dprint:
        print(message)


def analyse_open_circuit(channel):
    rms = np.sqrt(np.mean(channel**2))
    mn = np.min(channel)
    mx = np.max(channel)
    sd = np.std(channel)
    return [rms, mn, mx, sd]


def check_diffs_at_indices(CH1, CH2, ind1, ind2, shot):

    y1 = CH1[ind1]
    y2 = CH2[ind2]
    # Remove offsets
    y1 = y1 - np.mean(y1)
    y2 = y2 - np.mean(y2)

    # Scale x2 to match x1
    m1 = np.mean(abs(y1))
    y2 = y2 * (m1/np.mean(abs(y2)))

    y3 = np.abs(y2-y1)
    mini = np.round(np.min(y3) * 50, 3)
    maxi = np.round(np.max(y3) * 50, 3)
    av = np.round(np.mean(y3) * 50, 3)
    std = np.round(np.std(y3) * 50, 3)
    if av > 10:
        print("Hello world")
        print("Average delta between normalised transition values is greater than 10ns. Please inspect shot {}.".format(shot))
    dprint("Min: {}ns, Max: {}ns, Mean: {}ns, STD: {}".format(mini, maxi, av, std))
    return None


def compare_data(data, uuts, shot, threshold):
    transition_locations = []
    try:

        for num, channel in enumerate(data):
            if uuts[num] != "acq2106_201" and uuts[num] != "acq2106_203" and uuts[num] != "acq2106_204":
                dprint(uuts[num])
                continue

            diffs = np.diff(channel)
            where = np.where(np.abs(diffs) > threshold, 1, 0)
            dprint("DEBUG WHERE: {}".format(sum(where)))
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
            check_diffs_at_indices(data[0], channel, arr1, arr2, shot)
            if len(arr1) != len(arr2):
                print("keep {}".format(shot))
                dprint("ERROR_CODE1: Locations of transitions not the same size.")
                dprint("{} data: {}".format(uuts[0], arr1))
                dprint("{} data: {}".format(uuts[index+1], arr2))
                print(index+1)
                return
            if not np.allclose(arr1, arr2, atol=1, rtol=0):
                print("keep {}".format(shot))
                dprint("ERROR_CODE2: Found an error comparing uut: {} to {}".format(
                    uuts[0], uuts[index+1]))
                # print(uuts)
                print("{}\n{}".format(arr1, arr2))
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
        # plt.show()
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
        data, uut_list = get_mdsplus_data(uut_list, shot)
        compare_data(data, uut_list, shot, args.th)


if __name__ == '__main__':
    main()
    # tracker.print_diff()
