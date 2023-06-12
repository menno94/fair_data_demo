import os

rule all:
    input:
        path_output=os.path.join('data','4-output','output_waarden.xlsx'),
        path_bnd=os.path.join('data','4-output','D50.bnd'),
        path_fig_overview=os.path.join('reports','figures','overview.png')


rule model:
    input:
        path_data=os.path.join('data','1-external','voorbeeld_dataset.xlsx'),
    output:
        path_output=os.path.join('data','4-output','output_waarden.xlsx')
    script:
        os.path.join('src','3-model','model.py')

rule figures:
    input:
        path_data=os.path.join('data','4-output','output_waarden.xlsx'),
        path_shape=os.path.join('data','1-external','shape','NUTS_RG_01M_2021_3035.shp')
    output:
        path_fig_overview=os.path.join('reports','figures','overview.png'),
        
    params:
        path_fig=os.path.join('reports','figures'),
    script:
        os.path.join('src','5-visualize','plot_results.py')


rule create_bnd:
    input:
        path_data=os.path.join('data','4-output','output_waarden.xlsx'),
    output:
        path_bnd=os.path.join('data','4-output','D50.bnd')
    script:
        os.path.join('src','4-analyze','create_bnd.py')