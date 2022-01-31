import pandas as pd
import numpy as np
import os
from pathlib import Path

# %%
cwd = os.getcwd()
print(cwd)


# %%
def print_results(constraint: str):
    p = "./results/"
    columns = ['task', 'framework', 'constraint', 'fold', 'type', 'result', 'metric', 'duration', 'training_duration',
               'models_count']
    results = pd.read_csv(Path(p + "results.csv", usecols=columns))

    results = results[results.constraint.str.contains(constraint)]
    results['task'] = results['task'].str.lower()
    agg_model_counts_lb = results.groupby(['framework', 'type'], observed=True).agg({'models_count': [np.mean]})
    results = results.groupby(['framework', 'type', 'task', 'constraint'], observed=True).agg(
        {'result': [np.mean, np.std]})
    results.columns = ['mean', 'std']
    results = results.reset_index()
    results['mean'] = np.round(results['mean'], decimals=3)
    results['std'] = np.round(results['std'], decimals=4)
    results.to_csv(path_or_buf=Path(p + 'results_' + constraint + '.csv'), index=False)


# %%
print_results('12c_test')

# %%
print_results('1h12c')
