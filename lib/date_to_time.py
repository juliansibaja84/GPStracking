# Definitions
MIN = 10


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
    # Output values are: weeks, days, hours, minutes or seconds
    time_list = list()

    # Date scheme
    scale = dateScheme(significance, time_list, diff)

    # Time scheme
    if not time_list:
        scale = timeScheme(significance, time_list, diff)

    time_dict['scale'] = scale
    time_dict['array'] = ','.join(str(x) for x in time_list)

    return time_dict


def dateScheme(significance, time_list, diff):
    scale = 'wek'
    if significance == 'yhr':
        time_list.extend(range(1, diff*12 + 1))
    elif significance == 'mon':
        if diff*4 < MIN:
            time_list.extend(range(1, 11))
        else:
            time_list.extend(range(1, diff*4 + 1))
    elif significance == 'day':
        scale = 'day'
        if diff < MIN:
            time_list.extend(range(1, 11))
        else:
            time_list.extend(range(1, diff + 1))
    return scale


def timeScheme(significance, time_list, diff):
    scale = 'hur'
    if significance == 'hur':
        if diff < 2:
            scale = 'min'
            time_list.extend(range(1, diff*60 + 1))
        else:
            if diff < MIN:
                time_list.extend(range(1, 11))
            else:
                time_list.extend(range(1, diff + 1))
    elif significance == 'min':
        scale = 'min'
        if diff < 2:
            scale = 'sec'
            time_list.extend(range(1, diff*60 + 1))
        else:
            if diff < MIN:
                time_list.extend(range(1, 11))
            else:
                time_list.extend(range(1, diff + 1))
    elif significance == 'sec':
        scale = 'sec'
        if diff < MIN:
            time_list.extend(range(1, 11))
        else:
            time_list.extend(range(1, diff + 1))
    return scale

if __name__ == '__main__':
    time_dict = dateToList('0000-00-00 22:05:06', '0000-00-00 04:15:16')
    print(time_dict)
