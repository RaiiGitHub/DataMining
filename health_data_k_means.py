import kmeans.kmeans as ks
import numpy as np
import time
from sys import version_info
from pymining import itemmining

def date_to_timestamp(date_str):
    # noinspection PyBroadException
    try:
        tm = time.strptime(date_str, '%d-%b-%Y %H:%M')
        time_array = time.strptime(date_str, "%d-%b-%Y %H:%M")
        time_stamp = int(time.mktime(time_array))
        return time_stamp
    except:
        return None

def get_health_data_2d(x,y, file):
    # Load data
    D = np.loadtxt(open(file, "rb"), delimiter=",", skiprows=0, usecols=(x,y), dtype="str")
    data_2d = []
    for d in D[1:]:
        _d = []
        _t = date_to_timestamp(d[0])
        if _t is None:
            _d.append(float(d[0]))
        else:
            _d.append(_t)
        _d.append(float(d[1]))
        data_2d.append(_d)

    data_2d_with_label = (D[0],data_2d)
    return data_2d_with_label

def draw():
    d2wl = get_health_data_2d(0, 2, "mining-data/Health Data.csv")
    # frequent
    transactions = [round(x[1]*1)/1 for x in d2wl[1]]
    transactions = zip(transactions)
    relim_input = itemmining.get_relim_input(transactions)
    report = itemmining.relim(relim_input, min_support=2)
    report_keys = report.keys()
    report_values = report.values()
    joint_sort_report = zip(report_values,report_keys)
    joint_sort_report.sort(reverse=True)
    print('Health analyse - walk&run:relim frequence:')
    f = open('result/Health analyse - walk&run - frequent(relim method).txt', 'w')
    print >> f, joint_sort_report
    f.close()
    ks.draw_2d(d2wl[1], 5,'Health analyse - walk&run', d2wl[0][0], d2wl[0][1], is_time_sequence=True, marker='x',save_path='result/walk&run')

    d2wl = get_health_data_2d(0, 2, "mining-data/Sleep Analysis.csv")
    # frequent
    transactions = [round(x[1]*1)/1 for x in d2wl[1]]
    transactions = zip(transactions)
    relim_input = itemmining.get_relim_input(transactions)
    report = itemmining.relim(relim_input, min_support=2)

    report_keys = report.keys()
    a = []
    for x in report_keys:
        for i in x:
            a.append(i)
    a.sort()
    report_keys = [frozenset([x]) for x in a]
    report_sort = [{k: report[k]} for k in report_keys]

    print('Health analyse - sleep:relim frequence:')
    f = open('result/Health analyse - sleep - frequent(relim method).txt', 'w')
    print >> f, report_sort
    f.close()
    ks.draw_2d(d2wl[1], 5, 'Health analyse - sleep', d2wl[0][0], d2wl[0][1], is_time_sequence=True, marker='x',save_path='result/sleep')


draw()