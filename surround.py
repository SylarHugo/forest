'''function near arg(
    columns need a list[index | str] 
    to know each col_near = ['id', 'lat', 'lng', 'altitude', 'geohash']
    in df.columns

)
'''





import numpy
import pandas
import geohash as ggeo
import geopy

#creation df: geohash precision error
precisionerrordata = [[1, 2, 3, 23, 23, 2500],
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
    [12, 30, 30, 0.00000008, 0.00000017, 0.0000186],]
df_precision = pandas.DataFrame(precisionerrordata, columns = 
    ['geolen', 'latbits' , 'lngbits', 'laterror', ' lngerror', 'kmerror'])
#nparray:geohash code alphabet 
geoalp = numpy.array([['0','1','4','5','h','j','n','p'],['2','3','6','7','k','m','q','r']\
    ,['8','9','d','e','s','t','w','x'],['b','c','f','g','u','v','y','z']])
#columns mane of data
col_point=['id', 'lat', 'lng', 'altitude', 'geohash']

def geoup(code, pre):
    #list(geohash code index in alphabet)
    for i in reversed(range(0,pre)):
        strformer = code[:i]
        str_letter = code[i]
        strrest = code[i+1:]
        cw = numpy.argwhere(geoalp == str_letter)[0]
        if cw[0] > 0:
            cw[0] = cw[0] - 1
            recode = strformer + geoalp[cw[0], cw[1]] + strrest
            return recode
        elif cw[0] == 0:
            cw[0] = 3
            code = strformer + geoalp[cw[0], cw[1]] + strrest
            
def geodown(code, pre):
    #list(geohash code index in alphabet)
    for i in reversed(range(0,pre)):
        strformer = code[:i]
        str_letter = code[i]
        strrest = code[i+1:]
        cw = numpy.argwhere(geoalp == str_letter)[0]
        if cw[0] < 3:
            cw[0] = cw[0] - 1
            recode = strformer + geoalp[cw[0], cw[1]] + strrest
            return recode
        elif cw[0] == 3:
            cw[0] = 0
            code = strformer + geoalp[cw[0], cw[1]] + strrest

def geolift(code, pre):
    #list(geohash code index in alphabet)
    for i in reversed(range(0,pre)):
        strformer = code[:i]
        str_letter = code[i]
        strrest = code[i+1:]
        cw = numpy.argwhere(geoalp == str_letter)[0]
        if cw[1] > 0:
            cw[1] = cw[1] - 1
            recode = strformer + geoalp[cw[0], cw[1]] + strrest
            return recode
        elif cw[1] == 0:
            cw[1] = 7
            code = strformer + geoalp[cw[0], cw[1]] + strrest
        
def georight(code, pre):
    #list(geohash code index in alphabet)
    for i in reversed(range(0,pre)):
        strformer = code[:i]
        str_letter = code[i]
        strrest = code[i+1:]
        cw = numpy.argwhere(geoalp == str_letter)[0]
        if cw[1] < 7:
            cw[1] = cw[1] - 1
            recode = strformer + geoalp[cw[0], cw[1]] + strrest
            return recode
        elif cw[1] == 7:
            cw[1] = 0
            code = strformer + geoalp[cw[0], cw[1]] + strrest




#search area surround goal,return list(geohash code)
def neargeo(geocode, prei):
    p4geo = geolift(geocode, prei)
    p2geo = geoup(geocode, prei)
    p6geo = georight(geocode, prei)
    p8geo = geodown(geocode, prei)
    p1geo = geoup(p4geo, prei)
    p3geo = geoup(p6geo, prei)
    p7geo = geodown(p4geo, prei)
    p9geo = geodown(p6geo, prei)
    #neargeo = [p1geo, p2geo, p3geo, p4geo, p6geo, p7geo, p8geo, p9geo]
    areageo = [p1geo, p2geo, p3geo, p4geo, geocode, p6geo, p7geo, p8geo, p9geo]
    return areageo
#get point id which point in area, return set(id)
def nearpoint(i, areageo, df, prei):
    list_area = []
    for j in areageo:
        list_area = list_area + list(df.loc[:, df['geohash'].str[:prei].contains(areageo[j])].index)
    set_areap = set(list_area)
    set_areap.discard(i)
    return set_areap

#unify columns
def col_re(col_df, df):
    for i_col in range(0,len(col_point)):
        col_rename = col_df[i_col]
        if isinstance(col_rename, str):
            df.rename(columns={col_rename : col_point[i_col]}, inplace=True)
        elif isinstance(col_rename, int):
            df.rename(columns={df.columns[col_rename] : col_point[i_col]}, inplace=True)
        else:
            print('df.columns is error.')
    return df

#list the nearrest surc point list(id ,ditance) sruround_goal
def surroundpoint(id_g, df, surn=1, pre=12):
    p = (df.at[id_g,'lat'], df.at[id_g, 'lng'])#point(goal)
    dict_idis = {}#dict(id:dis,id:dis~) surround goal p
    for prei in reversed(range(0, pre)):
        areageo = neargeo(df.at[id_g, col_point[4]], pre)#eight area surround goal point area
        set_areap = nearpoint(id_g, areageo, df, prei)#set point in areageo and drop duplicates
        len_setareap = len(set_areap)
        if len_setareap < surn:
            r = df_precision.at[prei, 'laterror'] * 1500
            if len_setareap == 0:
                continue
            for i in dict_idis.keys():
                if i in set_areap:
                    set_areap.dicsard(i)#drop point had add into dict_idis
            for i in set_areap:
                ps = (df.at[i, 'lat'], df.at[i, 'lng'])#point ps in areapoint
                dis = round(geopy.distance(p, ps).m, 2)#distance
                if dis <= r:
                    dict_idis[i] = dis#add {id:dis} tu dict_idis
            continue
        else:
            r = df_precision.at[prei, 'laterror'] * 1500
            for i in dict_idis.keys():
                if i in set_areap:
                    set_areap.dicsard(i)
            for i in set_areap:               
                dis = round(geopy.distance(p, ps).m, 2)
                if dis <= r:
                    dict_idis[i] = dis
            if len(dict_idis) < surn:
                continue
            else:
                list_tupleidis = sorted(dict_idis.items(), key=lambda x:x[1])
                list_surp = []
                l = list(list_tupleidis)
                for i in range(0,surn):
                    list_surp = list_surp + list(l[i])
                return list_surp

#array the nearest point id and ditance surround-goal
def near(goal, df, col=col_point, surn=1, pre=12):
    '''
    id: goal: goaltree id
    df: DataFrame
    surc: surround trees count,list([columns name | columns id]), 
    col: where is col_near:['id', 'lat', 'lng', 'altitude', 'geohash'] in df.columns
    pre: geohash precision error'''
    
    df = col_re(col, df)#unify columns
    
    
    if pre < 12:#add precision
        pre = pre +1
    
    for i in df.index:#geohash.encode df.loc[lat, lng] to geocode
        df.at[i, col_point[4]] = ggeo.encode(df.at[i, 'lat'], df.at[i, 'lng'], pre)
    
    #len_index = len(df.index)
    list_surl = []# list(list(id,dis,~)) surround each goal
    for i in goal:
        list_surp = surroundpoint(id_g=i, df=df, surn=surn, pre=pre)
        list_surl = list_surl.append(list_surp)
    arr_suridis = numpy.array(list_surl)
    return arr_suridis






