import pandas as pd
import numpy as np
df = pd.DataFrame([[0, 0], [0, 0]], index=['row 1', 'row 2'], columns=['col 1', 'col 2'])

print(df)
print(df.values)
print(df.to_json(orient='split'))  ##
print(df.to_json(orient='records'))
print(df.to_json(orient='index'))
print(df.to_json(orient='columns'))  ##
print(df.to_json(orient='values'))
print(df.to_json(orient='table'))
np1 = df.values
print(np.all(np1 == 0))