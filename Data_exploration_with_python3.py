import csv
import pprint
data = list(csv.DictReader(open('ds_survey_20170321.csv')))
pprint.pprint(data[0])

