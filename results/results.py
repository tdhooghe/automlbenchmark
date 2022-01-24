import pandas as pd
import numpy as np
import os

#%%
cwd = os.getcwd()
print(cwd)

# %%
columns = ['task', 'framework', 'constraint', 'fold', 'type', 'result', 'metric', 'duration', 'training_duration',
           'models_count']
results = pd.read_csv("./results/results.csv", usecols=columns)
results = results[results['constraint'].str.contains("1h12c") == False]
results = results[results.constraint != 'test']
results = results.groupby(['framework', 'task']).agg({'result': [np.mean, np.std], })

print(results)
#results = results.groupby('task')['result'].agg([np.mean, np.std])

#%%
#results_hyperboost = results_hyperboost.groupby('task').agg(lambda x: list(x))
results_hyperboost = results_hyperboost.groupby(['framework', 'task']).agg({'result': [np.mean, np.std], })

print(results_hyperboost)
