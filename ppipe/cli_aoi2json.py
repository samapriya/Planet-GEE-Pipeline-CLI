import subprocess
import os
import json
from pprint import pprint
import argparse
import sys
import time
import os
import csv
import shapefile
import string
p1='{"config": [{"field_name": "geometry", "config": {"type": "Polygon","coordinates":'
p2='}, "type": "GeometryFilter"}, {"field_name": "gsd", "config": {"gte":1,"lte":9.99}, "type": "RangeFilter"}, {"field_name": "acquired", "config": {"gte":"'
p3='T04:00:00.000Z","lte":"'
p4='T03:59:59.999Z"}, "type": "DateRangeFilter"}, {"field_name": "cloud_cover", "config": {"gte":0'
p5=',"lte":'
p6='}, "type": "RangeFilter"}], "type": "AndFilter"}'

dir_path = os.path.dirname(os.path.realpath(__file__))

def aoijson(start,end,cloud,inputfile,geo,loc):
    if inputfile == 'KML':
        os.system("python kml_aoi.py --start "+start+" --end "+end+" --cloud "+cloud+" --geo "+geo+" --loc "+loc)
    elif inputfile=='WRS':
         with open(dir_path+'./wrs_grid.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[13]== geo:
                    a=str(row[14])
                    strpd=a.split(':')[3].strip('}')
                    filenames = p1+strpd+p2+str(start)+p3+str(end)+p4+p5+str(cloud)+p6
                    with open(loc+'./aoi.json', 'w') as outfile:
                        outfile.write(filenames)
                        outfile.close()
    elif inputfile == 'GJSON':
        raw= open(geo)
        for line in raw:
            fields=line.strip().split(":")[7]
            f2=fields.strip().split("}")[0]
            filenames = p1+f2+p2+str(start)+p3+str(end)+p4+p5+str(cloud)+p6
            with open(loc+'./aoi.json', 'w') as outfile:
                outfile.write(filenames)
                outfile.close()        
    elif inputfile == 'SHP':
        reader = shapefile.Reader(geo)
        fields = reader.fields[1:]
        field_names = [field[0] for field in fields]
        buffer = []
        for sr in reader.shapeRecords():
            atr = dict(zip(field_names, sr.record))
            geom = sr.shape.__geo_interface__
            buffer.append(dict(type="Feature", \
            geometry=geom, properties=atr))
            geom2=str(geom).replace("(",'[')
            geom3=str(geom2).replace(")",']')
            geom4=str(geom3).replace(",]",']')
            #print(geom5)
        # write the GeoJSON file
        with open(loc+'./int.geojson','w') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow([str(geom4)])
        raw= open(loc+'./int.geojson')
        for line in raw:
            fields=line.strip().split(":")[2]
            f2=fields.strip().split("}")[0]
            filenames = p1+f2+p2+str(start)+p3+str(end)+p4+p5+str(cloud)+p6
        with open(loc+'./aoi.json', 'w') as outfile:
            outfile.write(filenames)
            outfile.close()
    elif inputfile == 'WKT':
        raw= open(geo)
        for line in raw:
            l1=str(line).replace("POLYGON ((","[[[")
            l2=str(l1).replace("))","]]]")
            l3=str(l2).replace(", ","],[")
            l4=str(l3).replace(" ",",")
            filenames = p1+l4+p2+str(start)+p3+str(end)+p4+p5+str(cloud)+p6
        with open(loc+'./aoi.json', 'w') as outfile:
            outfile.write(filenames)
            outfile.close()
