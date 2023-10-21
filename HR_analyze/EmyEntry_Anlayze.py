import pandas as pd
from datetime import datetime


# read data from csv
file_path = "2023MCH_EmpEntry.csv"
# must check file name !!!!!!!!!!!
df = pd.read_csv(file_path)

# transfer DateTime to datetime (former is string and latter is datetime)
df['DateTime'] = pd.to_datetime(df['DateTime'])

# diagnose if is late
def is_late(row):
    emp_shift_time = datetime.strptime(row['EmpShift'], '%H:%M').time()
    actual_time = row['DateTime'].time()
    return actual_time > emp_shift_time

# use apply to call and recognize the late employees
df['Late'] = df.apply(is_late, axis=1)

# find the late employees
late_employees = df[df['Late'] == True].drop(columns=['Late'])

# sort by datetime
late_employees_sorted = late_employees.sort_values(by='DateTime')

# save into a csv file
late_employees_sorted.to_csv("late_employees_sorted.csv", index=False)