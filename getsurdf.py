'''
get the df had params W M U C.'''

import pandas
import nearbygeo
import structure

pathr = r'C:\Users\sylar\Desktop\1.xlsx'
pathw = r'C:\Users\sylar\Desktop\2.xlsx'

# default param
surn = 4  # find the nearest surn trees surround goaltree
precision = 5  # geohash precision error
pre_dis = 2
pre_float = 2
col_sn = ['id']  # serial number or notation of trees
col_gps = ['lat', 'lng', 'altitude']
# col_geo = ['geocode']
col_W = ['x', 'y', 'z']  # uniform angle index
col_M = ['species']  # mingling
col_U = ['DBM']  # DBM
col_C = ['crown']  # crown
params_tree = [col_W, col_M, col_U, col_C]
params_spatial = ['uniformangle', 'mingling', 'neighborhood', 'crowding']
coordinates = ['gps', 'certesian', ' polar']
ells = [
    'WGS-84', 'GRS-80', 'Airy (1830)',
    'Intl 1924', 'Clarke (1880)', 'GRS-67']
# ellipsoids = {
#             #model             major (km)   minor (km)     flattening
#             'WGS-84':        (6378.137,    6356.7523142,  1 / 298.257223563),
#             'GRS-80':        (6378.137,    6356.7523141,  1 / 298.257222101),
#             'Airy (1830)':   (6377.563396, 6356.256909,   1 / 299.3249646),
#             'Intl 1924':     (6378.388,    6356.911946,   1 / 297.0),
#             'Clarke (1880)': (6378.249145, 6356.51486955, 1 / 293.465),
#             'GRS-67':        (6378.1600,   6356.774719,   1 / 298.25),
#             }#ELLIPSOIDS


# read data
df = pandas.read_excel(pathr, names=col_sn + col_gps + col_M + col_U + col_C)  # read data
original_types = df[col_sn[0]].dtypes

# find the nearest srun trees in around-places
id_g = list(df[col_sn[0]])

# get array surround trees id and array for each distance
arr_idsur, arr_idis = nearbygeo.near(
    df=df, id_g=id_g, id=col_sn[0], col_coord=col_gps,
    col_code=None, n_sur=surn, pre=precision,
    elld=ells[0], pre_dis=pre_dis)

# add col[id,idis]
col_idsur = []
col_idis = []
for i in range(0, surn):
    col_idsur.append('id_sur' + str(i+1))  # near points id
    col_idis.append('idis_sur' + str(i+1))  # correspondece points distance
df_add = pandas.DataFrame(columns=col_idsur + col_idis)
df = pandas.concat([df, df_add])
df[col_sn[0]] = df[col_sn[0]].astype(original_types)
del df_add

# add array id and distance to df
df.loc[df[col_sn[0]]==id_g, col_idsur] = arr_idsur
df.loc[df[col_sn[0]]==id_g, col_idis] = arr_idis

sn = col_sn[0] 
# get uniformangle
df.loc[df[sn]==id_g, 'W'] = structure.uniformangle_df(
    df=df, col_idsur=col_idsur, id_g=id_g, id=col_sn[0], col_coord=col_gps,
    coord=coordinates[0], pre_float=pre_float, elld=ells[0])

# # get mingling
df.loc[df[sn]==id_g, 'M'] =  structure.mingling_df(
  df=df, col_idsur=col_idsur, id_g=id_g, id=col_sn[0],
  col_species=col_M, pre_float=pre_float)

# get neighborhood
df.loc[df[sn]==id_g, 'U'] = structure.neighborhood_df(
    df=df, col_idsur=col_idsur, id_g=None,
    id=col_sn[0], col_DBM=col_U, pre_float=pre_float)

# #get crowding
df.loc[df[sn]==id_g, 'C'] = structure.crowding_df(
  df=df, col_idsur=col_idsur, col_idis=col_idis,
  id_g=None, id=col_sn[0], col_crown=col_C, pre_float=pre_float)

# # write df
df.to_excel(pathw)
