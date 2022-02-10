import time
import pandas as pd


def GetPeakValues(data):
    df=pd.DataFrame(columns=['a', 'b'])
    for p in range(1, data['ID']):
        time.sleep(1)
        print(p)

    return df
