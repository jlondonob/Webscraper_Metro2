import pandas as pd
import numpy as np

data = {
    'Number': [1,2,3,1],
    'Characteristics': ['yellow', 'green', 'blue', 'yellow'],
    'timeMarket': [1,1,1,1]
}


df = pd.DataFrame(data)



# Groups by all columns and sums timeMarket (note that by default timeMarket in new obs is 1!)
# ---- We may change 
df.groupby(df.columns.tolist(), as_index=False).agg({'timeMarket':'sum'})
