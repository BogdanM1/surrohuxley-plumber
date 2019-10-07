import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib



commands = open("load_data.py").read()
exec(commands)

data  = data.iloc[:,feature_columns + target_columns]
corrmat = data.corr()
top_corr_features = corrmat.index
g = sns.heatmap(data[top_corr_features].corr(), annot=True, cmap="RdYlGn")
g.set_ylim(5.0, 0)
g.set_xticklabels(g.get_xticklabels(), rotation=0)
plt.savefig('corrMat.png')
plt.close()