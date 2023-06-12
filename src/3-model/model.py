import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


debug = False

if debug:
    path_data = os.path.join('..','..','data','1-external','voorbeeld_dataset.xlsx')
    path_output = os.path.join('..','..','data','4-output','D50_waarden.xlsx')
else: 
    path_data = snakemake.input.path_data
    path_output = snakemake.output.path_output


data = pd.read_excel(path_data,
                     sheet_name='KustlocatiesHB',
                     skiprows = range(1, 2),
                     header=0)


index_data = ~data['D50 '].isna()




data_new = data.copy()

data_new['D50 int'] = np.nan

for ii, item in enumerate(data.loc[:,'D50 ']):
    
    ## get kustvak
    kv = data['KV'][ii]

    index_data  = (~data['D50 '].isna()) & (data['KV']==kv)
    if kv==8 or kv==9:
        index_data  = (~data['D50 '].isna()) & ((data['KV']==8) | (data['KV']==9))
    elif kv==12 or kv==13:
        index_data  = (~data['D50 '].isna()) & ((data['KV']==12) | (data['KV']==13))
    elif kv==15 or kv==16:
        index_data  = (~data['D50 '].isna()) & ((data['KV']==15) | (data['KV']==16))
    
    sample_kv   = data[index_data]

    if len(sample_kv)==0:
        continue

    if np.isnan(data['D50 '][ii]):



        ## if index is lower than first index with data
        if ii < sample_kv.index[0]:
            data_new.loc[ii,['D50 int']] = data['D50 '][sample_kv.index[0]]
        elif ii > sample_kv.index[-1]:
            data_new.loc[ii,['D50 int']] = data['D50 '][sample_kv.index[-1]]
        else:
            I = np.where( ii > sample_kv.index)[0][-1]
            data_new.loc[ii,['D50 int']] = np.interp( data['Raai'][ii], sample_kv['Raai'].iloc[I:I+2],sample_kv['D50 '].iloc[I:I+2]   )


        ## exceptions (hard coded)

        ## island
        if kv==3 and data['Raai'][ii]>4600:
            data_new.loc[ii,['D50 int']] = 187
        ## Hondsbossche Duinen
        elif kv==7 and data['Raai'][ii]>=2041 and data['Raai'][ii]<=2582:
            data_new.loc[ii,['D50 int']] = np.nan
        ## Brouwers dam
        elif kv==12 and data['Raai'][ii]>=1925 and data['Raai'][ii]<=2525:
            data_new.loc[ii,['D50 int']] = np.nan
        ## Oosterscheldekering
        elif kv==14 and data['Raai'][ii]>=360 and data['Raai'][ii]<=540:
            data_new.loc[ii,['D50 int']] = np.nan
        ## Westkapelse Zeedijk
        elif kv==16 and data['Raai'][ii]>=1948 and data['Raai'][ii]<=2185:
            data_new.loc[ii,['D50 int']] = np.nan

    else:
        data_new.loc[ii,['D50 int']] = data['D50 '][ii]

    
data_new.to_excel(path_output,
                  sheet_name='KustlocatiesHB',
                  index=False)






