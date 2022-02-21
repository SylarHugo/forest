import pandas
import geohash.Geohash
pathr = ''
pathw = ''


precisionerrordata = [[1, 2, 3, 23, 23, 2500],\
    [2, 5, 5, 2.8, 5.6, 630],\
    [3, 7, 8, 0.70, 0.70, 78],\
    [4, 10, 10, 0.087, 0.18, 20],\
    [5, 12, 13, 0.022, 0.022, 2.4],\
    [6, 15, 15, 0.0027, 0.0055, 0.61],\
    [7, 17, 18, 0.00068, 0.00068, 0.076],\
    [8, 20, 20, 0.000085, 0.000172, 0.01911],\
    [9, 22, 23, 0.000021, 0.000021, 0.00478],\
    [10, 25, 25, 0.00000268, 0.00000536, 0.0005971],\
    [11, 27, 28, 0.00000067, 0.00000067, 0.0001492],\
    [12, 30, 30, 0.00000008, 0.00000017, 0.0000186],]
precisionerror = pandas.DataFrame(precisionerrordata, columns = \
    ['geolen','latbits' , 'lngbits', 'laterror', ' lngerror', 'kmerror'])

def geoup():
    pass
def geodown():
    pass
def geolift():
    pass
def georight():
    pass
def neargeo(p5geo, prej):
    p4geo = geolift(p5geo, prej)
    p2geo = geoup(p5geo, prej)
    p6geo = georight(p5geo, prej)
    p8geo = geodown(p5geo, prej)
    p1geo = geoup(p4geo, prej)
    p3geo = geoup(p6geo, prej)
    p7geo = geodown(p4geo, prej)
    p9geo = geodown(p6geo, prej)
    #neargeo = [p1geo, p2geo, p3geo, p4geo, p6geo, p7geo, p8geo, p9geo]
    areageo = [p1geo, p2geo, p3geo, p4geo, p5geo, p6geo, p7geo, p8geo, p9geo]
    return areageo
def nearpoint(areageo, df, prej):
    dfa = df.loc[:,df['geohash'].str[:prej].contains(areageo[0])]
    for stri in range(0,len(areageo) - 1):
        dfa = dfa.append(df.loc[:,df['geohash'].str[:prej].contains(areageo[stri + 1])])
    return dfa

#begin
df = pandas.read_excel(pathr)
for i in range(0, df.index):
    p = (df.loc[i]['lat'], df.loc[i]['lng'])
    for prei in range(5,10):
        prej = 10 - prei + 4
        p5geo = geohash.Geohash.encode(p)[:prej]
        areageo = neargeo(p5geo, prej)
        dfa = nearpoint(areageo, df, prej)
        #paixu
        #quchong
        if len(dfa.index) >= 4:
            r = precisionerrordata['laterror'] * 1500
            listdfp = []
            for pindex in dfa.index:
                if pindex != i:
                    pni = (df.at[pindex]['lat'],df.at[pindex]['lng'])
                    pdn = geopy.distance.distance(p,pni).m
                    if  pdn <= r:
                        listdfp = listmin4(listdfp, pindex, pdn)                
            if len(listdfp) >= 4:
                for j in range(0, 4):
                    df.at[i]['pn1id'] = listdfp[j][0]
                    df.at[i]['pn1dis'] = listdfp[j][1]  

class nearp4:
    def neardf():
        return df


if __name__ == '__main__':
    df.to_excel(pathw)