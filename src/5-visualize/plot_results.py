import geopandas
import matplotlib.pyplot as plt
import pandas as pd
import os

debug = False

if debug:
    path_data = os.path.join('..','..','data','4-output','D50_waarden.xlsx')
    path_shape = os.path.join('..','..','data','1-external','shape','NUTS_RG_01M_2021_3035.shp')
    path_fig_overview = os.path.join('..','..','reports','figures','overview.png')
    path_fig = os.path.join('..','..','reports','figures')
else: 
    path_data = snakemake.input.path_data
    path_fig_overview = snakemake.output.path_fig_overview
    path_fig = snakemake.params.path_fig
    path_shape = snakemake.input.path_shape

data_new = pd.read_excel(path_data ,
                     sheet_name='KustlocatiesHB',
                     skiprows = range(1, 2),
                     header=0)




EU = geopandas.read_file( path_shape)
EU = EU[EU.CNTR_CODE != "FR"]

EU0 = EU.to_crs("EPSG:28992")

xlims = [[1e4, 5e4],
        [3.5e4, 9e4],
        [0.6e5, 1.1e5],
        [0.9e5, 1.35e5],
        [1.00e5, 1.4e5],
        [1.20e5, 1.60e5],
        [1.65e5, 2.2e5],
        ]
ylims = [[3.7e5, 4.2e5],
        [4.1e5, 4.5e5],
        [4.4e5, 4.9e5],
        [4.85e5, 5.4e5],
        [5.3e5, 5.8e5],
        [5.7e5, 6.2e5],
        [5.95e5, 6.2e5],
        ]
for kk, item in enumerate(xlims):
    plt.figure(figsize=[10,10])
    ax = plt.subplot(1,1,1)
    EU0.plot(color='lightsteelblue',ax=ax)


    ax.scatter(data_new['x(grd)'],data_new['y(grd)'],5,data_new['D50 int' ],cmap='turbo')
    sc= ax.scatter(data_new['x(grd)'],data_new['y(grd)'],40,data_new['D50 ' ],cmap='turbo')
    plt.colorbar(sc,format='%.0f')
    #cbar.set_label('$D_{50}$', rotation=270)
    plt.grid('on')
    ax.set_aspect('equal',adjustable='box')
    plt.xlabel('$X_{RD}$ [m]')
    plt.ylabel('$Y_{RD}$ [m]')
    plt.title('$D_{50}$ [$\mu$m]')
    ax.set_xlim(item[0],item[1])
    ax.set_ylim(ylims[kk])
    
    plt.savefig(os.path.join(path_fig,'{}'.format(kk)))


plt.figure(figsize=[10,10])
ax = plt.subplot(1,1,1)
EU0.plot(color='lightsteelblue',ax=ax)
for kk, item in enumerate(xlims):
    ax.plot([item[0], item[1], item[1], item[0], item[0]], [ylims[kk][0], ylims[kk][0], ylims[kk][1], ylims[kk][1], ylims[kk][0]],'k',linewidth=0.5)

ax.scatter(data_new['x(grd)'],data_new['y(grd)'],5,data_new['D50 int' ],cmap='turbo')
sc= ax.scatter(data_new['x(grd)'],data_new['y(grd)'],40,data_new['D50 ' ],cmap='turbo')
plt.colorbar(sc,format='%.0f')
    #cbar.set_label('$D_{50}$', rotation=270)
plt.grid('on')
ax.set_aspect('equal',adjustable='box')
plt.xlabel('$X_{RD}$ [m]')
plt.ylabel('$Y_{RD}$ [m]')
plt.title('$D_{50}$ [$\mu$m]')
ax.set_xlim([-0.5e5, 2.5e5])
ax.set_ylim([3.5e5, 6.5e5])
plt.savefig(os.path.join(path_fig_overview))










