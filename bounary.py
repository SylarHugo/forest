'''
bounary correction method'''
import pandas
import geopy.distance

pathr = r'C:\Users\sylar\Desktop\1.xlsx'
pathw = r'C:\Users\sylar\Desktop\2.xlsx'

df = pandas.read_excel(pathr)

delid = set()
df=df.sort_values(by='lon')
min_lon = df['lon'].min()
max_lon = df['lon'].max()
min_lat = df['lat'].min()
max_lat = df['lat'].max()

df['x'] = None
df['y'] = None
p = (min_lat, min_lon)
for i in df.index:
    df.at[i,'x'] = round(geopy.distance.distance(p, (df.at[i, 'lat'], min_lon)).m ,2)
    df.at[i,'y'] = round(geopy.distance.distance(p, (min_lat, df.at[i, 'lon'])).m, 2)
    
df['lon'] = df['lon'] * 100000
df['lon'] = df['lon'].astype('int')
min_lon = df['lon'].min()
max_lon = df['lon'].max()
st = 12
n = int((max_lon-min_lon)//20 + 1)
for i in range(0, n):
    dfl = df.loc[(min_lon+i*st<=df['lon']) & (df['lon']<min_lon+i*st+st)]
    dmin = dfl['lat'].min()
    dmax = dfl['lat'].max()
    if pandas.isna(dmin):
        continue
    else:
        delid.add(dfl.loc[dfl['lat']==dmin, 'id'].iloc[0])
        delid.add(dfl.loc[dfl['lat']==dmax, 'id'].iloc[0])
    del dfl
writer = pandas.ExcelWriter(pathw)
df.to_excel(writer,sheet_name='all')
df.loc[delid].to_excel(writer,sheet_name='delid')
df = df.drop(delid)
df.to_excel(writer,sheet_name='save')
writer.save()
