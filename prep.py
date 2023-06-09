import pandas as pd
from secciones import *

print('Booting...')

df = pd.read_csv('MEX_GUB_2023.csv', on_bad_lines='skip', encoding='latin-1')

df.rename({'TOTAL_PERSONAS_VOTARON':'TOTAL', 
           'PAN':'ALE1', 
           'PRI':'ALE2', 
           'PRD':'ALE3', 
           'NAEM':'ALE4',
           'C_PAN_PRI_PRD_NAEM':'ALE5', 
           'C_PAN_PRI_PRD':'ALE6', 
           'C_PAN_PRI_NAEM':'ALE7',
           'C_PAN_PRD_NAEM':'ALE8',
           'C_PRI_PRD_NAEM':'ALE9',
           'C_PAN_PRI':'ALE10',
           'C_PAN_PRD':'ALE11',
           'C_PAN_NAEM':'ALE12',
           'C_PRI_PRD':'ALE13',
           'C_PRI_NAEM':'ALE14',
           'C_PRD_NAEM':'ALE15',
           'CC_PVEM_PT_MORENA':'DEL', 
           }, axis=1, inplace=True)
print(df.columns)
df = df[['SECCION', 'ALE1', 'ALE2', 'ALE3', 'ALE4', 'ALE5','ALE6',
         'ALE7', 'ALE8', 'ALE9', 'ALE10', 'ALE11','ALE12', 
         'ALE13', 'ALE14', 'ALE15', 'DEL', 'TOTAL']  ]
df.dropna(axis=0, inplace=True)
df = df[df.ALE1 != 'Sin acta']

ALE = df['ALE1'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        + df['ALE2'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        +  df['ALE3'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        + df['ALE4'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        + df['ALE5'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        + df['ALE6'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        +  df['ALE7'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        +  df['ALE8'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        +  df['ALE9'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        +  df['ALE10'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        + df['ALE11'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        +  df['ALE12'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        +  df['ALE13'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        +  df['ALE14'].apply(lambda x: int(x) if str(x).isdigit() else None) \
        +  df['ALE15'].apply(lambda x: int(x) if str(x).isdigit() else None) 
df['ALE'] = ALE

ndf = df[['SECCION', 'ALE', 'DEL', 'TOTAL']]

l = []
d = mun_dict()

for label in ndf.index:
    s = ndf.loc[label]['SECCION']
    s = s.strip('\'')
    mun = mun_secc(s,d)
    l.append(mun)
ndf['CVE_MUN'] = l
ndf.drop('SECCION', axis=1, inplace=True)
DELFINA = ndf['DEL'].apply(lambda x: int(x) if str(x).isdigit() else None)  
VOT_TOTAL = ndf['TOTAL'].apply(lambda x: int(x) if str(x).isdigit() else None)  
ndf['DELFINA'] = DELFINA
ndf['VOT_TOTAL'] = VOT_TOTAL

results = ndf.groupby(['CVE_MUN'], as_index=False).sum()
POR_DELFINA = results['DELFINA']*100/results['VOT_TOTAL']  
POR_ALEJANDRA = results['ALE']*100/results['VOT_TOTAL']



results['DELFINA_PORCENTUAL'] = POR_DELFINA
results['ALEJANDRA_PORCENTUAL'] = POR_ALEJANDRA

print(ndf)
print(ndf.columns)
print(results)

results.to_excel('Resultados EDOMEX.xlsx')
print('Done!')