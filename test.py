csv_sport = pd.read_csv('results/results_sportGmbH.csv', sep=',')
np.mean(csv['ho_max'])
np.mean(csv['ho_opt'])

csv_bank = pd.read_csv('results/results_bankZweiAG.csv', sep=',')
np.mean(csv_bank['ho_max'])
np.mean(csv_bank['ho_opt'])
