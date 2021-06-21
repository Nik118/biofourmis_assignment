# biofourmis_assignment

## Table of contents
* [General info](#general-info)
* [Requirements](#technologies)
* [Setup](#setup)
* [Output](#output)

## General info
This file has a simulator function to generate random values of hear_rate, resp_rate and activity every second
in increasing order of unix timestamp and it will then pass every value one by one to the
processor function. processor function code will update the pandas dataframe after every
new second value comes to it with average heart beat, minimum heartbeat, maximum heart beat and average respiration rate will be calculated for each value.

## Requirements
Python and pip should be installed before
Pandas - Install it by using below command

```
pip install pandas
```

## Setup
Run the command given below to get the simulator data for 2 hours

```
python test.py
```

## Output 
These are the files that will be cretaed once you run the above command
* input.json - Simulator data of 2 hours stored in json format
* output_segment.csv - Output of the processor function with respect to each segment of 15 minutes in a row
* output_hourly.csv - Output of the processor function with respect to each hour in a row
