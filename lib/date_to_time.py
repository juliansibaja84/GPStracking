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
    scale = 'wek'
    if significance == 'yhr':
        time_list.extend(range(1, diff*48 + 1))
    elif significance == 'mon':
        if diff*4 < MIN:
            time_list.extend(range(1, 11))
        else:
            time_list.extend(range(1, diff*4 + 1))
    elif significance == 'day':
        scale = 'day'
        if diff < MIN and ini + 10 < 30:
            time_list.extend(range(ini, ini + 10))
        else:
            time_list.extend(range(ini, fin + 1))
    return scale


def timeScheme(significance, time_list, diff, ini, fin):
    time_list.extend(range(ini, fin + 1))
    return significance

if __name__ == '__main__':
    time_dict = dateToList('0002-12-10 22:15:06', '0002-12-22 22:15:16')
    print(time_dict)
