from IPython.display import Image
import pandas as pd
import numpy as np
import datetime
import warnings
import pathlib
import pygwalker as pyg

import dtale
import dtale.app as dtale_app

from IPython.display import Image
import datetime
import warnings
import pathlib

import matplotlib as mpl
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)

# company = "sportGmbH"
company = "bankZweiAG"


def load_data(comp):
    d_employees = pd.read_csv('./data/' + comp + '/employees_' + comp + '.csv', sep=',')
    d_tasks = pd.read_csv('./data/' + comp + '/tasks_' + comp + '.csv', sep=',')
    d_employee_input = pd.read_csv('./data/' + comp + '/employee_input_' + comp + '.csv', sep=',')
    return d_employees, d_tasks, d_employee_input


# calculate diff between today and the start date at the company
def tenure(start_date):
    date_now = datetime.datetime.utcnow()
    date_diff = int((date_now - start_date).days)
    return date_diff


def ho_prob(days):
    if days < 180:
        home_office_prob = 0
    else:
        home_office_prob = 100
    return home_office_prob


# calculate the home office level based on the age (gen-preference)
def ho_generation(year):
    if 1946 <= year <= 1964:
        return 48
    elif 1965 <= year <= 1980:
        return 50
    elif 1981 <= year <= 1994:
        return 44
    else:
        return 28


# calculate the home office level based on the education
def ho_degree(abschluss):
    if abschluss == 'Hochschule':
        return 48
    elif abschluss == 'mittlere Reife':
        return 17
    else:
        return 8


# calculate the home office level based on the commute time
def ho_commute(time):
    if time > 40:
        return 46
    elif 20 <= time <= 40:
        return 2.3 * time - 46  # linear decline
    else:
        return 0


# calculate the home office proportion based on caring responsibility
def ho_gender_resp(employees):
    if employees['Caring Responsibility'] and employees['Gender'] == 'female':
        return 56.1
    elif employees['Caring Responsibility'] and employees['Gender'] == 'male':
        return 52
    else:
        return 50


# calculate the preferred proportion of home office
def ho_prefer(employee_input):
    if employee_input['ho_wish']:
        return (employee_input['desired_days'] / 5) * 100
    else:
        return 0


# calculate derivations
def deviation(ho_shares):
    ho_shares['difference_to_max'] = int(ho_shares['ho_max'] - ho_shares['ho_prefer'])
    ho_shares['difference_to_opt'] = int(ho_shares['ho_opt'] - ho_shares['ho_prefer'])
    ho_shares['difference_to_social'] = int(ho_shares['ho_social'] - ho_shares['ho_prefer'])
    return ho_shares


# calculate the preferred proportion of home office based on personality traits
# see Kawakubo, S., & Arata, S. (2022). Study on residential environment and workers’ personality traits on productivity while working from home. Building and Environment, 212, 108787.
def ho_personality_openness(employee_input):
    if 2 <= employee_input['openness'] <= 8:
        return 1.2
    else:
        return 6.1


def ho_personality_neuroticism(employee_input):
    if 2 <= employee_input['neuroticism'] <= 7:
        return 6.3
    else:
        return 2.2


def ho_personality_perseverance_and_passion(employee_input):
    if 1 <= employee_input['perseverance_and_grit'] <= 3:
        return 1.7
    else:
        return 6.5


# the other three factors are not significant, therefore, we currently avoid these
# Conscientiousness
# Extraversion
# Agreeableness


# we calculate the percentage based on the single value
def ho_personality__complete(employee_input):
    return ((ho_personality_openness(employee_input) + ho_personality_neuroticism(
        employee_input) + ho_personality_perseverance_and_passion(employee_input)) / (6.1 + 6.3 + 6.5)) * 100


employees, tasks, employee_input = load_data(company)

# make sure everything is numeric
tasks.loc[:, "T01":"Q42"] = tasks.loc[:, "T01":"Q42"].apply(pd.to_numeric)
employee_input[["desired_days", "Commute", "openness", "neuroticism", "perseverance_and_grit"]] = employee_input[
    ["desired_days", "Commute", "openness", "neuroticism", "perseverance_and_grit"]].apply(pd.to_numeric)

# make everything in these two columns to a boolean value
employee_input[["ho_wish", "Caring Responsibility"]] = employee_input[["ho_wish", "Caring Responsibility"]].replace(
    {'True': True, 'False': False})
employee_input[["ho_wish", "Caring Responsibility"]] = employee_input[["ho_wish", "Caring Responsibility"]].where(
    employee_input[["ho_wish", "Caring Responsibility"]].applymap(type) == bool)

# %%

# -------------------------
# Employer's point of view
# -------------------------

# take sum of tasks
# 3.2.1 The Teleworkability-Index
ho_tasks = tasks['T09'] + tasks['T10'] + tasks['T11'] + tasks['T12'] + tasks['T13'] + tasks['T14'] + tasks['T15'] + \
           tasks['T16']

# add new column to df
tasks['ho_max'] = ho_tasks

# 3.2.2 Infrastructure.
tasks.loc[tasks.it == False, ['ho_max']] = 0

# 3.2.3 Sense of Belonging to Company.
employees['Entry date'] = pd.to_datetime(employees['Entry date'])
employees['Company affiliation duration'] = employees['Entry date'].apply(tenure)
employees['ho_prob'] = employees['Company affiliation duration'].apply(ho_prob)

tasks = pd.merge(tasks, employees[['Activity', 'ho_prob']], on='Activity', how='left')
tasks.loc[tasks.ho_prob == 0, ['ho_max']] = 0
# calculate the mean
ho_max_total = int((int(tasks['ho_max'].sum())) / len(tasks.index))

# results after first 3 steps (mean)
print(
    'The maximum proportion of home office at the company after the first three points is: ' + str(ho_max_total) + '%.')

# 3.2.4 Task-Media-Fit Model
grouptasks_ho = tasks['Q01'] + tasks['Q02'] + tasks['Q42']
grouptasks_office = tasks['Q03'] + tasks['Q41']

tasks['grouptasks_ho'] = grouptasks_ho
tasks['grouptasks_office'] = grouptasks_office
tasks[['Activity', 'grouptasks_ho', 'grouptasks_office']]

opt_tasks = tasks['ho_max'] - tasks['grouptasks_office']
tasks['ho_opt'] = opt_tasks

# correct if mox amount of home office was already zero:
tasks.loc[tasks.ho_opt <= 0, ['ho_opt']] = 0

# calculate the mean
ho_opt_total = int((int(tasks['ho_opt'].sum())) / len(tasks.index))
print('The optimal amount of home office based on the media fit model is: ' + str(ho_opt_total) + '%.')
# %%

# -------------------------
# Social factors
# -------------------------

# 3.3.1 Different generations
employees['Birth date'] = pd.to_datetime(employees['Birth date'])
employees['birth_year'] = employees['Birth date'].dt.year
employees['ho_generation'] = employees['birth_year'].apply(ho_generation)

# 3.3.2 Education.
employees['ho_degree'] = employees['Degree'].apply(ho_degree)

# 3.3.3 Commute time
employees['ho_commute'] = employee_input['Commute'].apply(ho_commute)

# 3.3.4 Caring Responsibility
employees = employees.join(employee_input['Caring Responsibility'])
employees['ho_responsibility'] = employees.apply(ho_gender_resp, axis=1)

# 3.3.5 Personality factors
employees = employees.join(employee_input['openness'])
employees = employees.join(employee_input['neuroticism'])
employees = employees.join(employee_input['perseverance_and_grit'])

employees['personality_factor'] = employees.apply(ho_personality__complete, axis=1)

# Social factors subset
employees_subset = employees[['ho_generation', 'ho_degree', 'ho_commute', 'ho_responsibility', 'personality_factor']]

# calculate the mean
average_value_ho = np.average(employees_subset, axis=1)
employees_subset['ho_social'] = average_value_ho
ho_social_total = round((int(employees_subset['ho_social'].sum()) / len(employees.index)), 2)
print('The optimal proportion of home office based on the social factors is: ' + str(ho_social_total) + '%.')

# %%
# -------------------------
# Employee Requests
# -------------------------

# 3.4 Employee Requests
employee_input['ho_prefer'] = employee_input.apply(ho_prefer, axis=1)

# calculate the mean
ho_prefer_total = round((int(employee_input['ho_prefer'].sum()) / len(employee_input.index)), 2)
print('The mean of the employees wishes for home office is: ' + str(ho_prefer_total) + '%.')

# %%
# -------------------------
# Difference Between the Calculated proportion of Home Office and Preference
# -------------------------

employees = employees.join(employee_input['ho_prefer'])
employees = employees.join(employees_subset['ho_social'])
employees = pd.merge(employees, tasks[['Activity', 'ho_max']], on='Activity', how='left')
employees = pd.merge(employees, tasks[['Activity', 'ho_opt']], on='Activity', how='left')

ho_shares = employees[['Personal number', 'Activity', 'Employee', 'ho_social', 'ho_opt', 'ho_max', 'ho_prefer']]
ho_shares = ho_shares.drop_duplicates()
employees = employees.drop_duplicates()

ho_shares = ho_shares.apply(deviation, axis=1)

pathlib.Path('results/').mkdir(parents=True, exist_ok=True)
ho_shares.to_csv('results/results_' + company + '.csv', index=False)
