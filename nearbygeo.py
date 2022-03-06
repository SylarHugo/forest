'''
function near return two arrays arr_idsur and arr_idis.
param:
df : pd.DataFrame
id : columns where the tree number or notation resides
id_g : list[goaltrees id]
lat : gps lat
lng : gps lng
altitude : gps altitude
surn : how many trees surround goaltree
pre : correct to pre geohash code places.(percision)
return:
arr_idsur : serial number or notation of trees surround goaltree
arr_idis : each distance between trees and goaltree
'''
__all__ = [
    # def
    'near',
    'neargeo'
]

import numpy
import pandas
import geohash.Geohash as ggeo
import geopy

# default param
surn = 4  # find the nearest surn trees surround goaltree
precision = 12  # geohash precision error
pre_dis = 2  # round(distance, pre_dis)
col_sn = ['id']  # serial number or notation of trees
col_gps = ['lat', 'lng', 'altitude']
col_geo = ['geocode']
# col_W = ['x', 'y', 'z']  # uniform angle index
# col_M = ['species']  # mingling
# col_U = ['DBM']  # DBM
# col_C = ['crown']  # crown
# params_tree = [col_W, col_M, col_U, col_C]
# params_spatial = ['uniformangle', 'mingling', 'neighborhood', 'crowding']
col_preerr = [
    'geolen', 'latbits', 'lngbits', 'laterror', ' lngerror', 'kmerror']
ells = [
    'WGS-84', 'GRS-80', 'Airy (1830)', 'Intl 1924', 'Clarke (1880)', 'GRS-67']
ellipsoids = {
            # model             major (km)   minor (km)     flattening
            'WGS-84':        (6378.137,    6356.7523142,  1 / 298.257223563),
            'GRS-80':        (6378.137,    6356.7523141,  1 / 298.257222101),
            'Airy (1830)':   (6377.563396, 6356.256909,   1 / 299.3249646),
            'Intl 1924':     (6378.388,    6356.911946,   1 / 297.0),
            'Clarke (1880)': (6378.249145, 6356.51486955, 1 / 293.465),
            'GRS-67':        (6378.1600,   6356.774719,   1 / 298.25),
            }  # ELLIPSOIDS in geopy library

# creation df: geohash precision error
precisionerrordata = [
    [1, 2, 3, 23, 23, 2500],
    [2, 5, 5, 2.8, 5.6, 630],
    [3, 7, 8, 0.70, 0.70, 78],
    [4, 10, 10, 0.087, 0.18, 20],
    [5, 12, 13, 0.022, 0.022, 2.4],
    [6, 15, 15, 0.0027, 0.0055, 0.61],
    [7, 17, 18, 0.00068, 0.00068, 0.076],
    [8, 20, 20, 0.000085, 0.000172, 0.01911],
    [9, 22, 23, 0.000021, 0.000021, 0.00478],
    [10, 25, 25, 0.00000268, 0.00000536, 0.0005971],
    [11, 27, 28, 0.00000067, 0.00000067, 0.0001492],
    [12, 30, 30, 0.00000008, 0.00000017, 0.0000186]]
df_precision = pandas.DataFrame(precisionerrordata, columns=col_preerr)

# nparray:geohash code alphabet
geoalp = numpy.array([
    ['b', 'c', 'f', 'g', 'u', 'v', 'y', 'z'],
    ['8', '9', 'd', 'e', 's', 't', 'w', 'x'],
    ['2', '3', '6', '7', 'k', 'm', 'q', 'r'],
    ['0', '1', '4', '5', 'h', 'j', 'n', 'p']
])


# unify columns, return df
def col_re(df, id=col_sn[0], col_coord=col_gps, col_code=None):

    df1 = pandas.DataFrame()
    # id
    if isinstance(id, str):
        df1[col_sn[0]] = df[id]
    elif isinstance(id, int):
        df1[col_sn[0]] = df.iloc[:, id]
    else:
        print('df.columns is error.')

    # col_params:gps,certesion,polar
    for i in range(0, 3):
        col_i = col_coord[i]
        if isinstance(col_i, str):
            df1[col_gps[i]] = df[col_i]
        elif isinstance(col_i, int):
            df1[col_gps[i]] = df.iloc[:, col_i]
    if col_code is not None:
        if isinstance(col_code, str):
            df1[col_geo[0]] = df[col_code]
        elif isinstance(col_code, int):
            df1[col_geo[0]] = df.iloc[:, col_code]
        else:
            print('df.columns is error.')
    else:
        df1[col_geo[0]] = None
    return df1


def geoup(code, pre):
    # list(geohash code index in alphabet)
    for i in reversed(range(0, pre)):
        str_letter = code[i]  
        cw = numpy.argwhere(geoalp == str_letter)[0]
        if i % 2:
            if cw[1] == 7:
                code = code[:i] + geoalp[cw[0], 0] + code[i+1:]
            else:
                code = code[:i] + geoalp[cw[0], cw[1]+1] + code[i+1:]
                break
        else:
            if cw[0] == 0:
                code = code[:i] + geoalp[3, cw[1]] + code[i+1:]
            else:
                code = code[:i] + geoalp[cw[0]-1, cw[1]] + code[i+1:]
                break
    return code


def geodown(code, pre):
    # list(geohash code index in alphabet)
    for i in reversed(range(0, pre)):
        str_letter = code[i]  
        cw = numpy.argwhere(geoalp == str_letter)[0]
        if i % 2:
            if cw[1] == 0:
                code = code[:i] + geoalp[cw[0], 7] + code[i+1:]
            else:
                code = code[:i] + geoalp[cw[0], cw[1]-1] + code[i+1:]
                break              
        else:
            if cw[0] == 3:
                code = code[:i] + geoalp[0, cw[1]] + code[i+1:]
            else:
                code = code[:i] + geoalp[cw[0]+1, cw[1]] + code[i+1:]
                break
    return code


def geolift(code, pre):
    # list(geohash code index in alphabet)
    for i in reversed(range(0, pre)):
        str_letter = code[i] 
        cw = numpy.argwhere(geoalp == str_letter)[0]
        if i % 2:
            if cw[0] == 3:
                code = code[:i] + geoalp[0, cw[1]] + code[i+1:]
            else:
                code = code[:i] + geoalp[cw[0]+1, cw[1]] + code[i+1:]
                break
        else:
            if cw[1] == 0:
                code = code[:i] + geoalp[cw[0], 7] + code[i+1:]
            else:
                code = code[:i] + geoalp[cw[0], cw[1]-1] + code[i+1:]
                break
    return code


def georight(code, pre):
    # list(geohash code index in alphabet)
    for i in reversed(range(0, pre)):
        str_letter = code[i]  
        cw = numpy.argwhere(geoalp == str_letter)[0]
        if i % 2:
            if cw[0] == 0:
                code = code[:i] + geoalp[3, cw[1]] + code[i+1:]
            else:
                code = code[:i] + geoalp[cw[0]-1, cw[1]] + code[i+1:]
                break
        else:
            
            if cw[1] == 7:
                code = code[:i] + geoalp[cw[0], 0] + code[i+1:]
            else:
                code = code[:i] + geoalp[cw[0], cw[1]+1] + code[i+1:]
                break
    return code


# search area surround goal,return list(geohash code)
def neargeo(p5geo, prei):
    p4geo = geolift(p5geo, prei)
    p2geo = geoup(p5geo, prei)
    p6geo = georight(p5geo, prei)
    p8geo = geodown(p5geo, prei)
    p1geo = geoup(p4geo, prei)   
    p3geo = geoup(p6geo, prei)
    p7geo = geodown(p4geo, prei)
    p9geo = geodown(p6geo, prei)
    list_9area = [
        p1geo, p2geo, p3geo, p4geo, p5geo, p6geo, p7geo, p8geo, p9geo]
    return list_9area


# get point id which point in area, return set(id)
def nearid(df, id_gi, list_9area, prei=precision):
    list_id = []
    for j in list_9area:
        s = j[:prei]
        l_bool = df[col_geo[0]].str.contains(s)
        list_id = list_id + list(df.loc[l_bool, col_sn[0]])
    set_id = set(list_id)
    set_id.discard(id_gi)
    return set_id


# list the nearrest surc point list(id ,ditance) sruround_goal
def geo_part(
    df, id_gi, n_sur=surn, pre=precision, pre_dis=pre_dis, elld=ells[0]
):
    '''
    pass'''
    id = col_sn[0]
    row_g = df[df[id] == id_gi].index[0]  # index row where goaltree
    p = (df.at[row_g, col_gps[0]], df.at[row_g, col_gps[1]])  # point(goal)
    list_id = []
    list_dis = []
    list_idis = []
    set_rowp = set()
    for prei in reversed(range(1, pre+1)):
        # return list[nine area for the center id_gi]
        list_9area = neargeo(p5geo=df.at[row_g, col_geo[0]][:prei], prei=prei)
        # set point in areageo and drop duplicates
        set_id = nearid(df=df, id_gi=id_gi, list_9area=list_9area, prei=prei)
        len_setid = len(set_id)

        if len_setid >= n_sur:
            r = df_precision.at[prei-1, col_preerr[5]] * 1000
            for id_i in set_id:
                row_p = df[df[id] == id_i].index[0]
                if row_p not in set_rowp:
                    pn = (df.at[row_p, col_gps[0]], df.at[row_p, col_gps[1]])
                    dis = round(
                        geopy.distance.distance(
                            p, pn, ellipsoid=elld).m, pre_dis)
                    if dis <= r:
                        set_rowp.add(row_p)
                        sn_i = df.at[row_p, col_sn[0]]
                        list_idis.append([sn_i, dis])

            if len(set_rowp) >= n_sur:
                list_idis = sorted(list_idis, key=lambda x: x[1])
                for i in range(0, 4):
                    list_id.append(list_idis[i][0])
                    list_dis.append(list_idis[i][1])
                return list_id, list_dis


# array the nearest point id and ditance surround-goal
def near(
    df, id_g=None, id=col_sn[0], col_coord=col_gps, col_code=None,
    n_sur=surn, pre=precision, elld=ells[0], pre_dis=pre_dis
):

    '''
    df : pd.DataFrame
    id_g : list(goaltrees index)
    id : columns of trees serial number ,str or int
    col_coord : list(gps lat lng altitude) in columns.
     str or int.default[lat, lng, altitude]
    col_cood : geohash code in columns. str or int.
    surn : the number of trees surround goaltree
    pre=precision,(geohash precision).eg. pre=2; code = '00'
    coord : [wgs-84]
    pre_dis : round(geopy.distance(p,p).m, 2)
    #pre_float : round(folat,2). eg.1.02, 0.01. int.'''

    # get id_g
    if id_g is None:
        id_g = list(df[id])
    # rename columns, return df
    df = col_re(df=df, id=id, col_coord=col_coord, col_code=col_code)

    # get geohash.encode
    if col_code is None:
        # get each geohash code
        for i in df.index:  # geohash.encode df.loc[lat, lng] to geocode
            df.at[i, col_geo[0]] = ggeo.encode(
                df.at[i, col_gps[0]], df.at[i, col_gps[1]], pre)
    # df.to_excel(pathw)


    list_lid = []  # list(list(id)) surround each goal
    list_ldis = []  # list(list(idis)) surround each goal
    for i in id_g:
        # return two list for each ig_g
        list_id, list_dis = geo_part(
            df=df, id_gi=i, n_sur=surn, pre=pre, pre_dis=pre_dis, elld=ells[0])
        list_lid.append(list_id)
        list_ldis.append(list_dis)
    arr_idsur = numpy.array(list_lid)
    arr_dis = numpy.array(list_ldis)
    arr_geo = numpy.array(df[col_geo[0]])
    return arr_idsur, arr_dis, arr_geo
