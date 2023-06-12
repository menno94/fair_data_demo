
import pandas as pd
import os
import numpy as np

debug = False

if debug:
    path_data = os.path.join('..','..','data','4-output','output_waarden.xlsx')
    path_bnd = os.path.join('..','..','data','4-output','D50.bnd')
else: 
    path_data = snakemake.input.path_data
    path_bnd= snakemake.output.path_bnd


data_new = pd.read_excel(path_data,
                     sheet_name='KustlocatiesHB',
                     skiprows = range(1, 2),
                     header=0)


bnd = data_new.copy()
bnd.drop(['Combi','tr','x(grd)','y(grd)','D50 ','D50','D50.1','D50.2'], axis=1, inplace=True)
bnd['D50 int'] = np.round(bnd['D50 int'])
bnd['D50 int'] = bnd['D50 int']/1000000


with open(path_bnd, 'w') as fout:
    fout.write('Kv\tNr\tD50\n')
    fout.write('*Kustvaknummer\tMetrering\tKorreldiameter\n')
    fout.write('*[-]\t[dam]\t[m]\n')

    bnd['Raai'] = bnd['Raai'].map(lambda x: '%2.1f' % x)
    bnd.to_csv(fout,sep='\t', index=False, line_terminator='\n',header=None, float_format='%.6f')