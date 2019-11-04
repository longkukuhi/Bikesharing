import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def transform_to_order(df):
    times = []
    counts = []
    dates = []
    start_time_hours = []
    order_total_number = df.sum()[1]
    for i in range(df.shape[0]):
        date_, count = df.loc[i]
        time = date_[11:13]
        date = date_[0:10]
        times.append(int(time))
        counts.append(int(count))
        for j in range(count):
            start_time_hours.append(int(time))
            dates.append(date)

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
    total_fee = (time_hours[:, 1] - time_hours[:, 0]) * 2
    bikes_id = np.random.randint(1, 2000, (order_total_number, 1))
    user_id = np.random.randint(1, 10000, (order_total_number, 1))
    pdata = {'date': dates[:], 'start_time_hour': time_hours[:, 0], 'strat_time_minutes': time_minutes[:, 0],
             'end_time_hour': time_hours[:, 1], 'end_time_minutes': time_minutes[:, 1],
             'total_fee': total_fee[:], 'bike_id': bikes_id[:, 0], 'user_id': user_id[:, 0]}
    order = pd.DataFrame(pdata)
    return order


# time-count
def draw_count_hours(df):
    count_all = pd.DataFrame({'Time': np.arange(0, 24, 1), 'Count': [0] * 24})
    for i in range(df.shape[0]):
        time = int(df.loc[i, 'datetime'][11:13])
        count_all.iloc[time, 1] += int(df.loc[i, 'count'])
    startDate = df.iloc[0, 0][0:10]
    endDate = df.iloc[df.shape[0] - 1, 0][0:10]
    plt.figure()
    plt.plot(np.arange(0, 24, 1), count_all['Count'], '.-')
    plt.title('Bike rent in different time ')
    plt.legend((startDate + ' to ' + endDate,), loc='best')
    plt.xlabel('Time',)
    plt.ylabel('Counts in an hour',)
    plt.tight_layout()
    plt.savefig('./draw_count_hours.jpeg', dpi=800)
    plt.show()


def draw_two_count_hours(df0, df1):
    startDate = []
    endDate = []
    count_all0 = pd.DataFrame({'Time': np.arange(0, 24, 1), 'Count': [0] * 24})
    count_all1 = pd.DataFrame({'Time': np.arange(0, 24, 1), 'Count': [0] * 24})
    for i in range(df0.shape[0]):
        time = int(df0.loc[i, 'datetime'][11:13])
        count_all0.iloc[time, 1] += int(df0.loc[i, 'count'])

    for i in range(df1.shape[0]):
        time = int(df1.loc[i, 'datetime'][11:13])
        count_all1.iloc[time, 1] += int(df1.loc[i, 'count'])

    startDate.append(df0.iloc[0, 0][0:10])
    endDate.append(df0.iloc[df0.shape[0] - 1, 0][0:10])

    startDate.append(df1.iloc[0, 0][0:10])
    endDate.append(df1.iloc[df1.shape[0] - 1, 0][0:10])
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('Bike rent in different time ')
    ax.set_xlabel('Time')
    ax.set_ylabel('Counts in an hour')
    ax.set_xticks(np.arange(0, 24, 1))

    l1 = ax.plot(count_all0['Count'], 'b.-', label=(startDate[0] + ' to ' + endDate[0]))
    # lt.legend(l1,(startdate[0]+' to '+enddate[0],), color='red',loc='best')
    l2 = ax.plot(count_all1['Count'], 'r.-', label=(startDate[1] + ' to ' + endDate[1]))
    # lt.legend(l2,(startdate[1]+' to '+enddate[1],),color='blue', loc='best')
    ax.legend()
    fig.tight_layout()
    plt.savefig('./draw_two_count_hours.jpeg', dpi=800)
    plt.show()

def draw_week_weekend_count(df):
    count_all = pd.DataFrame({'workingday':0,'weekend':0},index=[0])
    for i in range(df.shape[0]):
        if(int(df.loc[i,'workingday'])==1):
            count_all.iloc[0,0] += int(df.loc[i,'count'])
        else:
            count_all.iloc[0,1] += int(df.loc[i,'count'])

    fig = plt.figure()
    width = 0.2
    labels = ['Day']
    x = [0,1]
    ax = fig.add_subplot(1,1,1)
    ax.set_title('Bike rent in Workingday & holiday')
    ax.set_xticks = x
    ax.set_xticklabels(labels)
    ax.set_ylabel('Count')
    ax.set_xlabel('Time period')
    rects1 = ax.bar(width,count_all.iloc[0,0]/5,width,label='Workingday')
    rects2 = ax.bar(width*2,count_all.iloc[0,1]/2,width,label='Weeken')
    ax.legend()
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    plt.savefig('./draw_week_weekend.jpeg', dpi=800)
    plt.show()


def draw_stack_three_week_weekend(df,period1_start,period1_end,period2_start,period2_end,period3_start,period3_end):
    time = []
    for i in range(6):
        time.append(period1_start)
        time.append(period1_end)
        time.append(period2_start)
        time.append(period2_end)
        time.append(period3_start)
        time.append(period3_end)
    #process part1
    count_all = pd.DataFrame({'workingday': [0]*3, 'weekend': [0]*3})

    #start1 = df[df['datetime']== time].iloc[0,0][0:11]
    start1 = df[df['datetime'] == time[0]].index.values[0]
    end1 = df[df['datetime'] == time[1]].index.values[0]
    start2 = df[df['datetime'] == time[2]].index.values[0]
    end2 = df[df['datetime'] == time[3]].index.values[0]
    start3 = df[df['datetime'] == time[4]].index.values[0]
    end3 = df[df['datetime'] == time[5]].index.values[0]
    length1 = end1 - start1
    length2 = end2 - start2
    length3 = end3 - start3

    for i in np.arange(start1,end1,1):
        if(int(df.loc[i,'workingday'])==1):
            count_all.iloc[0,0] += int(df.loc[i,'count'])
        else:
            count_all.iloc[0,1] += int(df.loc[i,'count'])

    for i in np.arange(start2,end2,1):
        if(int(df.loc[i,'workingday'])==1):
            count_all.iloc[1,0] += int(df.loc[i,'count'])
        else:
            count_all.iloc[1,1] += int(df.loc[i,'count'])

    for i in np.arange(start3,end3,1):
        if(int(df.loc[i,'workingday'])==1):
            count_all.iloc[2,0] += int(df.loc[i,'count'])
        else:
            count_all.iloc[2,1] += int(df.loc[i,'count'])
    #data
    workingday = [count_all.iloc[:,0][i] for i in range(3)]
    weekend = [count_all.iloc[:,1][i] for i in range(3)]
    #draw figure
    #pdf = PdfPages('draw_three_week_weekend.pdf')
    width = 0.35
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    labels = [period1_start[0:11] +' to '+period2_end[0:11],period1_start[0:11]+' to '+period2_end[0:11],
              period3_start[0:11]+' to '+period3_end[0:11]]
    index = np.arange(0,len(labels)*5,5)
    ax.set_title('Bike renting in different period')
    ax.set_xticks(index)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Count')
    ax.set_xlabel('Time period')

    rects1 = ax.bar(index,workingday,width,label='Workingday')
    rects2 = ax.bar(index,weekend,width,label='Weekend')
    ax.legend()


    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    plt.savefig('./draw_three_week_weekend.jpeg', dpi=800)
    plt.show()

def draw_three_week_weekend(df,period1_start,period1_end,period2_start,period2_end,period3_start,period3_end):
    time = []
    for i in range(6):
        time.append(period1_start)
        time.append(period1_end)
        time.append(period2_start)
        time.append(period2_end)
        time.append(period3_start)
        time.append(period3_end)
    #process part1
    count_all = pd.DataFrame({'workingday': [0]*3, 'weekend': [0]*3})

    #start1 = df[df['datetime']== time].iloc[0,0][0:11]
    start1 = df[df['datetime'] == time[0]].index.values[0]
    end1 = df[df['datetime'] == time[1]].index.values[0]
    start2 = df[df['datetime'] == time[2]].index.values[0]
    end2 = df[df['datetime'] == time[3]].index.values[0]
    start3 = df[df['datetime'] == time[4]].index.values[0]
    end3 = df[df['datetime'] == time[5]].index.values[0]
    length1 = end1 - start1
    length2 = end2 - start2
    length3 = end3 - start3

    for i in np.arange(start1,end1,1):
        if(int(df.loc[i,'workingday'])==1):
            count_all.iloc[0,0] += int(df.loc[i,'count'])
        else:
            count_all.iloc[0,1] += int(df.loc[i,'count'])

    for i in np.arange(start2,end2,1):
        if(int(df.loc[i,'workingday'])==1):
            count_all.iloc[1,0] += int(df.loc[i,'count'])
        else:
            count_all.iloc[1,1] += int(df.loc[i,'count'])

    for i in np.arange(start3,end3,1):
        if(int(df.loc[i,'workingday'])==1):
            count_all.iloc[2,0] += int(df.loc[i,'count'])
        else:
            count_all.iloc[2,1] += int(df.loc[i,'count'])
    #data
    workingday = [count_all.iloc[:,0][i] for i in range(3)]
    weekend = [count_all.iloc[:,1][i] for i in range(3)]
    #draw figure
    #pdf = PdfPages('draw_three_week_weekend.pdf')
    width = 0.35
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    labels = [period1_start[0:11] +' to '+period2_end[0:11],period1_start[0:11]+' to '+period2_end[0:11],
              period3_start[0:11]+' to '+period3_end[0:11]]
    x = np.arange(0,len(labels)*5,5)
    ax.set_title('Bike renting in different period')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Count')
    ax.set_xlabel('Time period')

    rects1 = ax.bar(x-width/2,workingday,width,label='Workingday')
    rects2 = ax.bar(x+width/2,weekend,width,label='Weekend')
    ax.legend()


    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    plt.savefig('./draw_stack_three_week_weekend.jpeg', dpi=800)
    plt.show()