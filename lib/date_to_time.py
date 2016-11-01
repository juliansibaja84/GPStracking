# Definitions
MIN = 10


def dataGrouper(time_dict, data_time, data_value):
    # Data list is ordered by time
    # Data time has the format YYYY-MM-DD HH:MM:SS
    # Easy case is with days, hours and minutes
    data = list()
    scale = time_dict['scale']

    ini = 8
    fin = 10
    if scale == 'yhr':
        ini = 0
        fin = 4
    elif scale == 'mon':
        ini = 5
        fin = 7
    elif scale == 'hur':
        ini = 11
        fin = 13
    elif scale == 'min':
        ini = 14
        fin = 16

    # Merge data according to scale
    data_time, data_value = mergeData(data_time, data_value, ini, fin)

    for x in time_dict['array'].split(','):
        for i in range(0, len(data_time)):
            if int(x) == int(data_time[i]):
                data.append(data_value[i])
                break
            if int(x) < int(data_time[i]) + 1:
                data.append('0')
                break

    print('***********************************')
    return data


def mergeData(d_time, d_value, ini, fin):
    f_time = list()
    f_value = list()
    for x in d_time:
        check = False
        for i in range(0, len(d_time)):
            if x[ini:fin] not in f_time:
                check = True
                f_time.append(x[ini:fin])
                f_value.append([])
            if x[ini:fin] == d_time[i][ini:fin] and check:
                f_value[-1].append(d_value[i])
    print(f_time)
    print(f_value)
    return [f_time, f_value]


def dateToList(ini, fin):
    # Final list
    time_dict = dict()

    # Init and final dates YYYY-MM-DD HH:MM:SS
    dates = [ini, fin]

    # Break the dates in its basics components and store them away
    date_low = dict()
    date_high = dict()
    dates = [x.split(' ') for x in dates]

    date_low['yhr'] = dates[0][0][0:4]
    date_low['mon'] = dates[0][0][5:7]
    date_low['day'] = dates[0][0][8:]
    date_low['hur'] = dates[0][1][0:2]
    date_low['min'] = dates[0][1][3:5]
    date_low['sec'] = dates[0][1][6:]

    date_high['yhr'] = dates[1][0][0:4]
    date_high['mon'] = dates[1][0][5:7]
    date_high['day'] = dates[1][0][8:]
    date_high['hur'] = dates[1][1][0:2]
    date_high['min'] = dates[1][1][3:5]
    date_high['sec'] = dates[1][1][6:]

    # Get most significant time difference
    significance = 'yhr'
    for x in ['yhr', 'mon', 'day', 'hur', 'min', 'sec']:
        significance = x
        if date_low[x] != date_high[x]:
            break

    # Get numeric difference (for safeness take abs)
    diff = abs(int(date_high[significance]) - int(date_low[significance]))

    # Interpret difference
    # Output values are the same as significance
    time_list = list()

    # Date scheme
    ini = int(date_low[significance])
    fin = int(date_high[significance])
    scale = dateScheme(significance, time_list, diff, ini, fin)

    # Time scheme
    if not time_list:
        scale = timeScheme(significance, time_list, diff, ini, fin)

    time_dict['scale'] = scale
    time_dict['array'] = ','.join(str(x) for x in time_list)

    return time_dict


def dateScheme(significance, time_list, diff, ini, fin):
    time_list.extend(range(ini, fin + 1))
    return significance


def timeScheme(significance, time_list, diff, ini, fin):
    time_list.extend(range(ini, fin + 1))
    return significance


if __name__ == '__main__':
    time_dict = dateToList('0001-01-01 01:01:00', '0003-01-01 01:01:00')

    print(time_dict)
    timed = ['0002-12-10 01:15:06', '0002-12-10 01:15:06', '0002-12-10 05:15:06', '0002-12-10 06:15:06', '0002-12-10 06:15:06', '0002-12-10 06:15:06', '0002-12-10 08:15:06', '0002-12-10 08:15:06', '0002-12-10 09:15:06', '0002-12-10 10:15:06', '0002-12-10 11:15:06', '0002-12-10 20:15:06', '0002-12-10 21:15:06']
    datad = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    print('***********************************')
    print(dataGrouper(time_dict, timed, datad))