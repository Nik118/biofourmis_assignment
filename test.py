import os
import random
import time
import pandas as pd
import json


def process_sensor_data_func(sensor_data, dataframe , count, heart_rate_sum,
                             respiration_rate_sum, segment_count,
                             each_segment_duration):

    if segment_count == 0: #first time entry for each segment of 15 minutes
        new_segment_row = {
            'user_id': sensor_data['user_id'],
            'seg_start': sensor_data['timestamp'],
            'seg_end': '',
            'avg_hr': sensor_data['heart_rate'],
            'max_hr': sensor_data['heart_rate'],
            'min_hr': sensor_data['heart_rate'],
            'avg_rr': sensor_data['respiration_rate']
            }
        dataframe = dataframe.append(new_segment_row, ignore_index=True)

    else: # update average, max, min details for each simulation entry
        index = count // each_segment_duration # index is row number of segment
        if segment_count == each_segment_duration - 1:
            dataframe.at[index, 'seg_end'] = sensor_data['timestamp']

        dataframe.at[index, 'avg_hr'] = round(
                heart_rate_sum / (segment_count + 1), 2
            )
        dataframe.at[index, 'max_hr'] = max(
                dataframe.at[index, 'max_hr'], sensor_data['heart_rate']
            )
        dataframe.at[index,'min_hr'] = min(
                dataframe.at[index, 'min_hr'], sensor_data['heart_rate']
            )
        dataframe.at[index, 'avg_rr'] = round(
                respiration_rate_sum / (segment_count + 1), 2
            )

    return dataframe


def derive_hourly_average_func(dataframe):
    hourly_dataframe = pd.DataFrame(columns=dataframe.columns)
    heart_rate_sum = 0
    respiration_rate_sum = 0
    heart_rate_max = 0
    heart_rate_min = 10000

    for index, row in dataframe.iterrows():
        heart_rate_sum += row['avg_hr']
        respiration_rate_sum += row['avg_rr']
        heart_rate_max = max(heart_rate_max, row['max_hr'])
        heart_rate_min = min(heart_rate_min, row['min_hr'])

        if index % 4 == 0:
            segment_start = row['seg_start']

        elif index % 4 == 3:
            new_hourly_row = {
                'user_id': row['user_id'],
                'seg_start': segment_start,
                'seg_end': row['seg_end'],
                'avg_hr': round(heart_rate_sum / 4, 2),
                'max_hr': heart_rate_max,
                'min_hr': heart_rate_min,
                'avg_rr': round(respiration_rate_sum / 4, 2)
            }

            hourly_dataframe = hourly_dataframe.append(new_hourly_row,
                                                       ignore_index=True)
            heart_rate_sum = 0
            respiration_rate_sum = 0
            heart_rate_max = 0
            heart_rate_min = 10000

    hourly_dataframe.to_csv(os.getcwd() + '/' + 'output_hourly.csv')


def simulate_sensor_data_func():
    start_time = current_time = 1624275000 # 21-06-2021 17:00:00 
    sensor_data_list = []
    count = 0
    total_simulation_duration = 7200 # 2 hours
    each_segment_duration = 900 # 15 minutes
    columns = ['user_id', 'seg_start', 'seg_end', 'avg_hr', 'min_hr',
               'max_hr', 'avg_rr'
               ]
    dataframe = pd.DataFrame(columns=columns)

    while current_time - start_time < total_simulation_duration:
        segment_count = count % each_segment_duration
        sensor_data = {
            'user_id': 'abc',
            'timestamp': str(int(current_time)),
            'heart_rate': random.randint(40, 100),
            'respiration_rate': random.randint(10, 30),
            'activity': random.randint(1, 4)
        }

        if segment_count == 0:
            heart_rate_sum = sensor_data['heart_rate']
            respiration_rate_sum = sensor_data['respiration_rate']
        else:
            heart_rate_sum += sensor_data['heart_rate']
            respiration_rate_sum += sensor_data['respiration_rate']

        sensor_data_list.append(sensor_data)
        dataframe = process_sensor_data_func(sensor_data, dataframe, count,
                                            heart_rate_sum,
                                            respiration_rate_sum,
                                            segment_count,
                                            each_segment_duration
                                            )
        current_time += 1
        count += 1

    dataframe.to_csv(os.getcwd() + '/' + 'output_segment.csv')
    with open(os.getcwd() + '/' + 'input.json', 'w') as f:
        json.dump(sensor_data_list, f, indent=2)

    derive_hourly_average_func(dataframe)


if __name__ == "__main__":
    simulate_sensor_data_func()
