import pandas as pd
import geohash
import surround

pathr = ''
pathw = ''
surn = 4 #find the nearest surn trees surround goaltree
precision = 5#geohash pricision error

#creation columns file name
col_read = ['id', 'lat', 'lng', 'altitude']
col_geo = 'geocode'
col_add = []
for i in range(0, surn):
    col_add.append('near_id' + str(i+1))  #near point id
    col_add.append('near_dis' + str(i+1)) #near point distance
df_add = pd.DataFrame(columns = col_geo + col_add)

#read data
df = pd.read_excel(pathr,columns = col_read)#, sheet_name=0, header=None, names=col_name)
df = pd.concat([df,df_add])
del df_add

# geohash.encode df
len_df = len(df.index)
for i in range(0, len_df):
    df.at[i, col_geo] = geohash.encode(df.at[i,'lat'], df.at[i, 'lng'])

#find the nearest around-places
id_goaltree = list(df.index)
arr_suridis = surround.near(goal=id_goaltree,
     df=df, col=col_read+col_geo, surn=surn, pre=precision)#surround trees
df.loc[id_goaltree, col_add] = arr_suridis
df.to_excel(pathw)