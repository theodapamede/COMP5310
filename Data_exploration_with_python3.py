#EXERCISE 1: READING AND ACCESSING DATA

#Read the survey response data
import csv
import pprint
data = list(csv.DictReader(open('ds_survey_20170321.csv')))
pprint.pprint(data[0])

#Defining the constants for dictionary keys
TIMESTAMP = 'Timestamp'
GROUP_NAME = 'Group Name (use DNA if none):'
BACKGROUND_INDUSTRY = 'What main industry have you worked in?'
BACKGROUND_YEARS_PROFESSIONAL = 'How many years professional experience do you have?'
BACKGROUND_YEARS_PROGRAMMING = 'How many years programming experience do you have?'
BACKGROUND_SKILLS = 'What key experiences do you have?'
IMPORT_DATA_MANAGEMENT = 'Data management'
IMPORT_STATISTICS = 'Statistics'
IMPORT_VISUALISATION = 'Visualisation'
IMPORT_MACHINE_LEARNING = 'Machine Learning & Data Mining'
IMPORT_SOFTWARE_ENGINEERING = 'Software Engineering'
IMPORT_COMMUNICATION = 'Communication'
GOALS_DEFINITION = 'How would you define data science in one sentence?'
GOALS_SKILLS = 'What key skills do you want to develop?'
GOALS_ROLE = 'What role would you like to go into?'
GOALS_INDUSTRY = 'What industry would you like to go into?'
IMPORT_AREAS = [
    IMPORT_DATA_MANAGEMENT,
    IMPORT_STATISTICS,
    IMPORT_VISUALISATION,
    IMPORT_MACHINE_LEARNING,
    IMPORT_SOFTWARE_ENGINEERING,
    IMPORT_COMMUNICATION
    ]

#Accessing data values
row = data[0] # Row 0 corresponds to first respondent since arrays are 0-indexed
print("response:", row[BACKGROUND_YEARS_PROFESSIONAL]) # years of professional experience
print("type:", type(row[BACKGROUND_YEARS_PROFESSIONAL])) # csv 
print("type:", type(float(row[BACKGROUND_YEARS_PROFESSIONAL]))) # convert to float

#TODO 1: What is the third respondent's rating for communication?
row = data[2]
print("response:", row[IMPORT_COMMUNICATION])


#EXERCISE 2: FREQUENCY DISTRIBUTION AND MODE

#Counting Data
from collections import Counter
c = Counter([row[IMPORT_COMMUNICATION] for row in data])
print("Distribution of communication importance ratings:")
for k, v in sorted(c.items()):
    print('{}: {}'.format(k, v))
    
#TODO 2: Calculate distribution of background and goal industries
from collections import Counter
c = Counter([row[BACKGROUND_INDUSTRY] for row in data])
print("Distribution of Background Industries:")
for k, v in sorted(c.items()):
    print('{}: {}'.format(k, v))
print("\n")
c = Counter([row[GOALS_INDUSTRY] for row in data])
print("Distribution of Goals Industries:")
for k, v in sorted(c.items()):
    print("{}: {}".format(k, v))
    
#Calculating the mode
def mode(data, column_key):
    c = Counter([row[column_key] for row in data])
    return c.most_common(1)[0][0]
print("Communication mode:", mode(data, IMPORT_COMMUNICATION))

#TODO 3: Calculate the mode of background and goal industries
def mode(data, column_key):
    c = Counter([row[column_key] for row in data])
    return c.most_common(1)[0][0]
print("Background Industry mode:", mode(data, BACKGROUND_INDUSTRY))
print("Goals Industry mode:", mode(data, GOALS_INDUSTRY))

#EXERCISE 3: CALCULATING DESCRIPTIVE STATISTICS

#cleaning float data
import warnings
import numpy as np
DEFAULT_VALUE = np.nan
def iter_clean(data, column_key, convert_function, default_value):
    for row in data:
        old_value = row[column_key]
        new_value = default_value
        try:
            new_value = convert_function(old_value)
        except (ValueError, TypeError):
            warnings.warn('Replacing {} with {} in column {}'.format(
                row[column_key], new_value, column_key))
        row[column_key] = new_value
        yield row
data = list(iter_clean(data, BACKGROUND_YEARS_PROFESSIONAL, float, DEFAULT_VALUE))
data = list(iter_clean(data, BACKGROUND_YEARS_PROGRAMMING, float, DEFAULT_VALUE))

#Cleaning timestamp data
from datetime import datetime
FMT = "%Y/%m/%d %H:%M:%S %p GMT+11"
def str_to_time(s):
    return datetime.strptime(s, FMT)
data = list(iter_clean(data, TIMESTAMP, str_to_time, DEFAULT_VALUE))

#Statistics with numpy
import numpy as np
for column_key in [BACKGROUND_YEARS_PROFESSIONAL, BACKGROUND_YEARS_PROGRAMMING]:
    v = [row[column_key] for row in data] # grab values
    print(column_key.upper())
    print("* Min..Max: {}..{}".format(np.nanmin(v), np.nanmax(v)))
    print("* Range: {}".format(np.nanmax(v)-np.nanmin(v)))
    print("* Mean: {}".format(np.nanmean(v)))
    print("* Standard deviation: {}".format(np.nanstd(v)))
    print("* Median: {}".format(np.nanmedian(v)))
    q1 = np.nanpercentile(v, 25)
    print("* 25th percentile (Q1): {}".format(q1))
    q3 = np.nanpercentile(v, 75)
    print("* 75th percentile (Q3): {}".format(q3))
    iqr = q3-q1
    print("* IQR: {}".format(iqr))
    
#Binning and histograms
v = [row[BACKGROUND_YEARS_PROFESSIONAL] for row in data] # grab values
freqs, bins = np.histogram(v, bins=7, range=(0,35)) # calculate frequencies and bin start/end
for i, freq in enumerate(freqs):
    # Note that bins[i] <= bin_values < bins[i+1]
    bin_str = '[{}..{}]'.format(int(bins[i]), int(bins[i+1]))
    print(bin_str, ':', freq)
    
#TODO: Calculate histogram for programming experience
v = [row[BACKGROUND_YEARS_PROGRAMMING] for row in data] # grab values
freqs, bins = np.histogram(v, bins=7, range=(0,35)) # calculate frequencies and bin start/end
for i, freq in enumerate(freqs):
    # Note that bins[i] <= bin_values < bins[i+1]
    bin_str = '[{}..{}]'.format(int(bins[i]), int(bins[i+1]))
    print(bin_str, ':', freq)
    
 
