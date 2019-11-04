import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def genConcreteData(df):
    times = []
    counts = []
    dates = []
    start_time_hours = []
    order_total_number = df.loc[:,'count'].sum()
    workingdays = []
    seasons = []
    weathers = []
    temps = []
    atemps = []
    humiditys = []
    windspeeds = []
    #generate time & count
    for i in range(df.shape[0]):
        date_, count, workingday,season,weather,temp,atemp,humidity,windspeed = df.loc[i,['datetime','count','workingday',
        'season','weather','temp','atemp','humidity','windspeed']]
        time = date_[11:13]
        date = date_[0:10]
        times.append(int(time))
        counts.append(int(count))
        for j in range(count):
            start_time_hours.append(int(time))
            dates.append(date)
            workingdays.append(workingday)
            seasons.append(season)
            weathers.append(weather)
            temps.append(temp)
            atemps.append(atemp)
            humiditys.append(humidity)
            windspeeds.append(windspeed)
    start_time_hours = np.array(start_time_hours).reshape(order_total_number, )
    end_time_hours = []
    startTime = np.random.randint(0, 60, size=(order_total_number, 1))
    endTime = []
    for i in range(order_total_number):
        endTime.append(np.random.randint(startTime[i], 360))
    for i in range(order_total_number):
        period_hour = (endTime[i]) // 60
        end_time_hours.append(period_hour + start_time_hours[i])
    endTime = np.array(endTime).reshape(order_total_number, 1) % 60
    start_time_hours = start_time_hours.reshape((order_total_number, 1))
    end_time_hours = np.array(end_time_hours).reshape((order_total_number, 1))
    time_minutes = np.hstack((startTime, endTime))
    time_hours = np.hstack((start_time_hours, end_time_hours))

    #genrate fee & bikeid
    total_fee = (time_hours[:, 1] - time_hours[:, 0]) * 2
    bikes_id = np.random.randint(1, 2000, (order_total_number, 1))
    user_id = np.random.randint(1, 10000, (order_total_number, 1))

    #reform dataframe
    pdata = {'date': dates[:], 'start_time_hour': time_hours[:, 0], 'strat_time_minutes': time_minutes[:, 0],
             'end_time_hour': time_hours[:, 1], 'end_time_minutes': time_minutes[:, 1],
             'total_fee': total_fee[:], 'bike_id': bikes_id[:, 0], 'user_id': user_id[:, 0],
             'workingday': workingdays[:],'season': seasons[:],'weather': weathers[:],'temp': temps[:],
             'atemp': atemps[:],'humidity': humiditys[:],'windspeed': windspeeds[:]}
    order = pd.DataFrame(pdata)
    return order
