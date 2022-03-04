'''
spatial point pattern or stand spatial structure
return W, M, U, C for each point by function
 'uniformangle', 'mingling', 'neighborhood', 'crowding'.
 or return df by function
 'uniformangle_df', 'mingling_df', 'neighborhood_df', 'crowding_df'.
the renturn df will add columns W, M, U, C.'''

__all__ = [
    'uniformangle',
    'mingling',
    'neighborhood',
    'crowding',
    'uniformangle_df',
    'mingling_df',
    'neighborhood_df',
    'crowding_df'
]


import math
import pandas
import numpy
import geopy.distance

# default param
surn = 4  # find the nearest surn trees surround goaltree
pre_dis = 2
pre_float = 2
col_sn = ['id']  # serial number or notation of trees
col_gps = ['lat', 'lng', 'altitude']
col_geo = ['geocode']
col_W = ['x', 'y', 'z']  # uniform angle index
col_M = ['species']  # mingling
col_U = ['DBM']  # DBM
col_C = ['crown']  # crown
params_tree = [col_W, col_M, col_U, col_C]
params_spatial = ['uniformangle', 'mingling', 'neighborhood', 'crowding']
coordinates = ['gps', 'certesian', ' polar']
ells = [
    'WGS-84', 'GRS-80', 'Airy (1830)', 'Intl 1924', 'Clarke (1880)', 'GRS-67']
# ellipsoids = {
#             #model             major (km)   minor (km)     flattening
#             'WGS-84':        (6378.137,    6356.7523142,  1 / 298.257223563),
#             'GRS-80':        (6378.137,    6356.7523141,  1 / 298.257222101),
#             'Airy (1830)':   (6377.563396, 6356.256909,   1 / 299.3249646),
#             'Intl 1924':     (6378.388,    6356.911946,   1 / 297.0),
#             'Clarke (1880)': (6378.249145, 6356.51486955, 1 / 293.465),
#             'GRS-67':        (6378.1600,   6356.774719,   1 / 298.25),
#             }#ELLIPSOIDS


def re_col(df, id, col_idsur, col_params, func, col_idis=None):
    '''
    df:
    id:column_name of trees index. default 'id'
    col_param:columns name of  param
    module:which specific module,
    ['uniformangle', 'mingling', 'neighborhood', 'crowding']'''
    df1 = pandas.DataFrame()

    # rename(id)
    if isinstance(id, str):
        df1[col_sn[0]] = df[id]
    elif isinstance(id, int):
        df1[col_sn[0]] = df.iloc[:, id]

    # rename(col_idsur)
    l_idsur = []
    n = len(col_idsur)
    for i in range(0, n):
        col_i = col_idsur[i]
        l_idsur.append('idsur' + str(i+1))
        if isinstance(col_i, str):
            df1[l_idsur[0]] = df[col_i]
        elif isinstance(col_i, int):
            df1[l_idsur[0]] = df.iloc[:, id]

    # rename(col_params)
    re_param = params_tree[params_spatial.index(func)]
    n = len(col_params)
    if len(re_param) == n:
        for i in range(0, n):
            col_i = col_params[i]
            if isinstance(col_i, str):
                df1[re_param[i]] = df[col_i]
            elif isinstance(col_i, int):
                df1[re_param[i]] = df.iloc[:, col_i]
    else:
        print('len(param of module) != len(param of columns)')

    # rename col_idis
    l_idis = []
    if func == params_spatial[3]:
        n = len(col_idis)
        if len(col_idsur) == n:
            for i in range(0, n):
                col_i = col_idis[i]
                l_idis.append('idis_sur' + str(i+1))
                if isinstance(col_i, str):
                    df1[l_idis[i]] = df[col_i]
                elif isinstance(col_i, int):
                    df1[l_idis[i]] = df.iloc[:, col_i]
        else:
            print('len(col_idis) != len(col_id)')
    else:
        l_idis = ['None']
    return df1, l_idsur, l_idis


# uniform angle index, observed angle a, standard angle a0=90
def uniformangle(p0=(0, 0), arr_s=None, pre_float=pre_float):
    '''
    p0 : a point (x, y) at goal tree
    arr_s : np.array(list[surround points coord (x, y)])
    '''
    if arr_s is None:
        print('no points surround goal')
        return None
    if isinstance(arr_s, list):
        arr_s = numpy.array(arr_s)
    if isinstance(arr_s, tuple):
        arr_s = numpy.array(arr_s)

    surn = arr_s.shape[0]
    l_angle = []
    for i in range(0, surn):
        x = arr_s[i, 0] - p0[0]
        y = arr_s[i, 1] - p0[1]
        if x > 0:
            if y > 0:
                l_angle.append(
                    round(math.atan(x / y) / math.pi * 180, pre_float))
                continue
            elif y == 0:
                l_angle.append(0)
                continue
            elif y < 0:
                l_angle.append(
                    360 + round(math.atan(x / y) / math.pi * 180, pre_float))
                continue
        if x == 0:
            if y > 0:
                l_angle.append(90)
                continue
            elif y < 0:
                l_angle.append(270)
                continue
            elif y == 0:
                l_angle.append(0)
                continue
        if x < 0:
            if y > 0:
                l_angle.append(
                    180 + round(math.atan(x / y) / math.pi * 180, pre_float))
                continue
            elif y == 0:
                l_angle.append(180)
                continue
            elif y < 0:
                l_angle.append(
                    180 + round(math.atan(x / y) / math.pi * 180, pre_float))
                continue
    l_angle.sort()
    W = 0
    for i in range(0, surn):
        if i == 0:
            angles = l_angle[surn-1] - l_angle[i]
            if angles > 180:
                angles = angles - 180
            if angles < 90:
                W = W + 1
        else:
            angles = l_angle[i] - l_angle[i-1]
            if angles > 180:
                angles = angles - 180
            if angles < 90:
                W = W + 1
    W = round(W / surn, pre_float)
    return W


# mingling degree, diffrernt tree species
def mingling(s0, l_s, pre_float=pre_float):
    '''
    s0: goaltree species
    l_s: list[surround trees species]
    '''
    M = 0
    surn = len(l_s)
    for i in range(0, surn):
        if l_s[i] != s0:
            M = M + 1
    M = round(M/surn, pre_float)
    return M


# neighborhood comparison, DBM
def neighborhood(d0, l_DBM, pre_float=pre_float):
    '''
    d0: goaltree DBM
    l_d: list[surround trees DBM]
    '''
    U = 0
    surn = len(l_DBM)
    for i in range(0, surn):
        if l_DBM[i] >= d0:
            U = U + 1
    U = round(U/surn, pre_float)
    return U


# crowding degree. basal area, crown area
def crowding(c0, l_c, l_dis, pre_float=pre_float):
    '''
    c0: goaltree crown width
    l_w: list[surround trees crown width]
    l_dis : list [distance between surround trees and goaltree],
     l_d and l_dis correspond one to one
    '''
    C = 0
    surn = len(l_c)
    for i in range(0, surn):
        if l_dis[i] < (c0 + l_c[i]) / 2:
            C = C + 1
    C = round(C/surn, pre_float)
    return C


def uniformangle_df(
    df, col_idsur, id_g=None, id=col_sn[0], col_coord=col_gps,
    coord=coordinates[0], pre_float=pre_float, elld=ells[0]
):
    '''
    pass'''
    # verifies that pass columns name

    # id_g
    if id_g is None:
        id_g = list(df.index)
    # id
    # col_idsurs
    surn = len(col_idsur)
    # len(col_idsur > 0)
    n = len(col_coord)
    if 0 < n < 3:
        for i in range(n, 3):
            df[col_W[i]] = 0
            col_coord.append(col_W[i])
    elif n == 0:
        print('col_param error')
        return None
    del n

    df, col_idsur, col_idis = re_col(
        df, id=id, col_idsur=col_idsur,
        col_params=col_coord, func=params_spatial[0])
    df['W'] = None
    del col_idis

    arr_c = numpy.zeros((len(df.index), 3))  # array certesian
    if coord == coordinates[0]:  # GPS turn cartesian
        # x_max=df.loc[:, col_W[0]].max()
        x0 = df.loc[:, col_W[0]].min()  # x_max=df.loc[:, col_W[0]].max()
        # y_max = df.loc[:, col_W[1]].max()
        y0 = df.loc[:, col_W[1]].min()
        # z_max = df.loc[:, col_W[2]].max()
        z0 = df.loc[:, col_W[2]].min()
        # get new cartesian
        for i in df.index:
            x = df.at[i, col_W[0]]
            y = df.at[i, col_W[1]]
            z = df.at[i, col_W[2]]
            arr_c[i, 0] = round(geopy.distance.geodesic(
                (x0, y), (x, y)).m, pre_float)  # x elld
            arr_c[i, 1] = round(geopy.distance.geodesic(
                (x, y0), (x, y)).m, pre_float)  # y elld
            arr_c[i, 2] = z - z0  # z
    elif coord == coordinates[1]:  # cartesian
        arr_c[:, 0] = df.loc[:, col_W[0]]
        arr_c[:, 1] = df.loc[:, col_W[1]]
        arr_c[:, 2] = df.loc[:, col_W[2]]
    elif coord == coordinates[2]:
        'polar to cartesian'
        pass

    # get each point uniformangle
    for i in id_g:
        p0_index = df.loc[df[col_sn[0]] == i].index[0]
        p0 = (arr_c[p0_index, 0], arr_c[p0_index, 1])
        l_idsur = list(df.loc[p0_index, col_idsur])
        arr_s = numpy.zeros((surn, 2))
        for j in range(0, surn):
            pn_index = df.loc[df[col_sn[0] == l_idsur[j]]].index[0]
            arr_s[j, 0] = arr_c[pn_index, 0]
            arr_s[j, 1] = arr_c[pn_index, 1]
        df.loc[df[col_sn[0]] == i, 'W'] = uniformangle(
            p0=p0, arr_s=arr_s, pre_float=pre_float)
    return df


# mingling degree, diffrernt tree species
def mingling_df(
    df, col_idsur, id_g=None, id=col_sn[0],
    col_species=col_M[0], pre_float=pre_float
):
    '''
    pass'''
    # id_g
    if id_g is None:
        id_g = list(df.index)
    # id
    # col_idsurs
    surn = len(col_idsur)

    df, col_idsur, col_idis = re_col(
        df=df, id=id, col_idsur=col_idsur,
        col_params=col_species, func=params_spatial[1])
    df['M'] = None
    del col_idis

    for i in id_g:
        s0 = df.at[df[col_sn[0]] == i, col_M[0]]  # goaltree species
        l_s = []
        for j in range(0, surn):
            l_s.append(df.at[df[col_sn[0] == col_idsur[j]], col_M[0]])
        df.at[df[col_sn[0]] == i, 'M'] = mingling(
            s0=s0, l_s=l_s, pre_float=pre_float)
    return df


# neighborhood comparison, DBM
def neighborhood_df(
    df, col_idsur, id_g=None, id=col_sn[0],
    col_DBM=col_U[0], pre_float=pre_float
):
    # id_g
    if id_g is None:
        id_g = list(df.index)
    # id
    # col_idsurs
    surn = len(col_idsur)

    df, col_idsur, col_idis = re_col(
        df=df, id=id, col_idsur=col_idsur,
        col_params=col_DBM, func=params_spatial[2])
    df['U'] = None
    del col_idis

    for i in id_g:
        d0 = df.at[df[col_sn[0]] == i, col_U[0]]  # goaltree DBM
        l_DBM = []
        for j in range(0, surn):
            l_DBM.append(df.at[df[col_sn[0]] == col_idsur[j], col_U[0]])
        df.at[df[col_sn[0]] == i, 'U'] = neighborhood(
            d0=d0, l_DBM=l_DBM, pre_float=pre_float)
    return df


# crowding degree. basal area, crown area
def crowding_df(
    df, col_idsur, col_idis, id_g=None, id=col_sn[0],
    col_crown=col_C[0], pre_float=pre_float
):
    '''
    pass'''
    # id_g
    if id_g is None:
        id_g = list(df.index)
    # id
    # col_idsurs
    surn = len(col_idsur)

    df, col_idsur, col_idis = re_col(
        df=df, id=id, col_idsur=col_idsur, col_params=col_crown,
        col_idis=col_idis, func=params_spatial[3])
    df['C'] = None

    for i in id_g:
        c0 = df.at[df[col_sn[0]] == i, col_C[0]]  # goaltree c
        l_c = []
        l_dis = []
        for j in range(0, surn):
            l_c.append(df.at[df[col_sn[0]] == col_idsur[j], col_C[0]])
            l_dis.append(df.at[df[col_sn[0]] == col_idsur[j], col_idis[j]])
        df.at[df[col_sn[0]] == i, 'C'] = crowding(
            c0=c0, l_c=l_c, l_dis=l_dis, pre_float=pre_float)
    return df
