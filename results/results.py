import pandas as pd
import numpy as np
import os

# %%
cwd = os.getcwd()
print(cwd)

# %%
columns = ['task', 'framework', 'constraint', 'fold', 'type', 'result', 'metric', 'duration', 'training_duration',
           'models_count']
results = pd.read_csv("./results/results.csv", usecols=columns)
results = results[~results.constraint.str.contains("1h12c")]
results = results[results.constraint != 'test']
results['task'] = results['task'].str.lower()
agg_model_counts = results.groupby(['framework', 'type'], observed=True).agg({'models_count': [np.mean]})
results = results.groupby(['framework', 'type', 'task'], observed=True).agg({'result': [np.mean, np.std]})

results.columns = ['mean', 'std']
results = results.reset_index()
results['mean'] = np.round(results['mean'], decimals=3)
results['std'] = np.round(results['std'], decimals=4)
print(results)
