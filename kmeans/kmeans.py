from collections import defaultdict
from random import uniform
from math import sqrt
from plotcolor import *
import matplotlib.pyplot as plt
import time
import matplotlib.ticker as ticker


def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    NB. points can have more dimensions than 2
    
    Returns a new point which is the center of all the points.
    """
    dimensions = len(points[0])

    new_center = []

    for dimension in xrange(dimensions):
        dim_sum = 0  # dimension sum
        for p in points:
            dim_sum += p[dimension]

        # average of each dimension
        new_center.append(dim_sum / float(len(points)))

    return new_center


def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.

    Compute the center for each of the assigned groups.

    Return `k` centers where `k` is the number of unique assignments.
    """
    new_means = defaultdict(list)
    centers = []
    for assignment, point in zip(assignments, data_set):
        new_means[assignment].append(point)
        
    for points in new_means.itervalues():
        centers.append(point_avg(points))

    return centers


def assign_points(data_points, centers):
    """
    Given a data set and a list of points betweeen other points,
    assign each point to an index that corresponds to the index
    of the center point on it's proximity to that point. 
    Return an array of indexes of centers that correspond to
    an index in the data set; that is, if there are N points
    in `data_set` the list we return will have N elements. Also
    If there are Y points in `centers` there will be Y unique
    possible values within the returned list.
    """
    assignments = []
    for point in data_points:
        shortest = ()  # positive infinity
        shortest_index = 0
        for i in xrange(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    #not consider the first dimension.
    """
    dimensions = len(a)
    
    _sum = 0
    for dimension in xrange(dimensions):
        difference_sq = (a[dimension] - b[dimension]) ** 2
        _sum += difference_sq
    return sqrt(_sum)


def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    find the minimum and maximum for each coordinate, a range.
    Generate `k` random points between the ranges.
    Return an array of the random points within the ranges.
    """
    centers = []
    dimensions = len(data_set[0])
    min_max = defaultdict(int)

    for point in data_set:
        for i in xrange(dimensions):
            val = point[i]
            min_key = 'min_%d' % i
            max_key = 'max_%d' % i
            if min_key not in min_max or val < min_max[min_key]:
                min_max[min_key] = val
            if max_key not in min_max or val > min_max[max_key]:
                min_max[max_key] = val

    for _k in xrange(k):
        rand_point = []
        for i in xrange(dimensions):
            min_val = min_max['min_%d' % i]
            max_val = min_max['max_%d' % i]
            
            rand_point.append(uniform(min_val, max_val))

        centers.append(rand_point)
    centers.sort()
    return centers


def k_means(dataset, k):
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
        k_points = new_centers

    return (zip(assignments, dataset), k_points)

def max_min_mean_of_dimenstion(dataset):
    dimension_turple = zip(*dataset)
    min_max_mean_set = []
    for d in dimension_turple:
        _min = min(d)
        _max = max(d)
        _mean = np.mean(d)
        min_max_mean_set.append(dict(min=_min, max=_max, mean=_mean))
    return min_max_mean_set

def normalize_dataset(dataset,min_max_mean_set):
    #x* = (x-mean)/(max-min)
    for d in dataset:
        for i in range(len(d)):
            d[i] = (d[i] - min_max_mean_set[i]['mean'])/(min_max_mean_set[i]['max'] - min_max_mean_set[i]['min'])

def reverse_normalize_point(point, mmm_point):
    #x = x* * (max-min) + mean
    return point * (mmm_point['max'] - mmm_point['min']) + mmm_point['mean']


def format_date(x, pos=None):
    #x is the approximate timestamp, in seconds
    return time.strftime('%d-%b-%Y', time.localtime(x))

def draw_2d(
        points,
        center_max_num = 3,
        title = 'clutter-figure',
        x_label ='x',
        y_label = 'y',
        marker = '*',
        point_label = 'clutter center',
        is_time_sequence = False,
        save_path = 'draw_2d_figure'
        ):

    #nomalize the datas
    mmm = max_min_mean_of_dimenstion(points)
    print('min,max,mean->',mmm)
    normalize_dataset(points,mmm)
    clutter_k_center = k_means(points, center_max_num)
    clutter = clutter_k_center[0]
    k_center = clutter_k_center[1]
    clutter.sort()
    print(len(clutter))
    print('clutter:',k_center)
    center_actual = 0
    center_last = -1
    for _d in clutter:
        if center_last != _d[0]:
            center_last = _d[0]
            center_actual += 1
    print('max center count:%d, actual center count:%d' % (center_max_num, center_actual))
    clutter_color = list()
    for c in range(0,center_actual,1):
        while True:
            _c = get_random_color()
            _e = False
            for t in clutter_color:
                if t == _c:
                    _e = True
                    break
            if _e is False:
                clutter_color.append(_c)
                break

    fig = plt.figure()
    ax = fig.add_subplot(111)
    print(clutter_color)

    #plot points.
    for d in clutter:
        plt.plot(reverse_normalize_point(d[1][0], mmm[0]), reverse_normalize_point(d[1][1], mmm[1]),
                 color=clutter_color[d[0]], marker=marker)

    #plot center
    for i in range(len(k_center)):
        if center_actual > 15 or i > 0:
            plt.plot(reverse_normalize_point(k_center[i][0], mmm[0]), reverse_normalize_point(k_center[i][1], mmm[1]),
                     color='black', marker='^')
        else:
            plt.plot(reverse_normalize_point(k_center[i][0], mmm[0]), reverse_normalize_point(k_center[i][1], mmm[1]),
                     color='black', marker='^', label='%s:%d' % (point_label,center_actual))

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    if is_time_sequence is True:
        xfmt = ticker.FuncFormatter(format_date)
        ax.xaxis.set_major_formatter(xfmt)
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)

    fig = plt.gcf()
    plt.show()
    fig.savefig(save_path + ".png")


# points = [
#     [1, 2],
#     [2, 1],
#     [3, 1],
#     [5, 4],
#     [5, 5],
#     [6, 5],
#     [10, 8],
#     [7, 9],
#     [11, 5],
#     [14, 9],
#     [14, 14],
#     ]
# center_max_num = 3
#draw_2d()