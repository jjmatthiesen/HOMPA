import pandas as pd

companies = ["sportGmbH", "bankZweiAG"]

for company in companies:
    employees = pd.read_excel('data/' + company + '/' + company + '.xlsx', index_col='Personalnummer', sheet_name='AN_Infos')
    tasks = pd.read_excel('data/' + company + '/' + company + '.xlsx', index_col='Tätigkeit', sheet_name='Tätigkeit')
    employee_input = pd.read_excel('data/' + company + '/' + company + '.xlsx', index_col="Personalnummer", sheet_name='AN_Angaben')

    tasks.columns = [col[0:3] for col in tasks.columns]
    tasks = tasks.rename(columns={'IT ': 'it'})

    employee_input = employee_input.rename(columns={'Homeoffice erwünscht?':'ho_wunsch', 'Gewünschte Anzahl Tage pro Woche im Homeoffice':'wunsch_tage'})

    print(employees.columns)
    print(tasks.columns)
    print(employee_input.columns)

    employees.to_csv('./data/' + company + '/employees_' + company + '.csv')
    tasks.to_csv('./data/' + company + '/tasks_' + company + '.csv')
    employee_input.to_csv('./data/' + company + '/employee_input_' + company + '.csv')