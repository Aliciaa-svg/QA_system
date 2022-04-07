import pandas as pd
import numpy as np

f = 'data.csv'
data = pd.read_csv(f, header=None)
data_list = np.array(data).tolist()

dst = 'train.txt'
with open(dst, 'w') as file:
    for i in data_list:
        file.write(str(i[0])+'\n')
        file.write(str(i[1])+'\n')
        file.write('\n')

    
    

