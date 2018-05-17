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
        subprocess.call("python kml_aoi.py --start "+'"'+start+'"'+" --end "+'"'+end+'"'+" --cloud "+'"'+cloud+'"'+" --geo "+'"'+geo+'"'+" --loc "+'"'+loc+'"',shell=True)
        print("New structured JSON has been created at "+str(os.path.join(os.path.join(os.path.splitext(loc)[0],os.path.splitext(os.path.basename(geo))[0]+"_aoi.json"))))
        os.remove(os.path.join(loc,'kmlout.geojson'))
    elif inputfile == 'GJSON':
        with open(geo) as insert,open(os.path.join(dir_path,"aoi.json")) as jbase:
            geombase=json.load(jbase)
            geomloader = json.load(insert)
            cinsert= geomloader['features'][0]['geometry']['coordinates']
            cgeom=(geombase['config'][0]['config']['coordinates'])
            geombase['config'][0]['config']['coordinates']=cinsert #coordinate insert
            geombase['config'][2]['config']['gte']=str(start)+"T04:00:00.000Z" #change start date
            geombase['config'][2]['config']['lte']=str(end)+"T03:59:59.999Z" #change end date
            geombase['config'][3]['config']['gte']=0#change cloud minima default=0
            geombase['config'][3]['config']['lte']=float(cloud)# change cloud maxima
            print(os.path.join(os.path.splitext(loc)[0],os.path.splitext(os.path.basename(geo))[0]+"_aoi.json"))
            with open(os.path.join(os.path.join(os.path.splitext(loc)[0],os.path.splitext(os.path.basename(geo))[0]+"_aoi.json")), 'w') as f:
                f.write(json.dumps(geombase))
            print("New structured JSON has been created at "+str(os.path.join(os.path.join(os.path.splitext(loc)[0],os.path.splitext(os.path.basename(geo))[0]+"_aoi.json"))))
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
        with open(os.path.join(os.path.split(geo),os.path.splitext(loc)[0]+"_aoi.json"), 'w') as outfile:
            outfile.write(filenames)
            outfile.close()
        print("New structured JSON has been created at "+str(os.path.join(os.path.join(os.path.splitext(loc)[0],os.path.splitext(os.path.basename(geo))[0]+"_aoi.json"))))
    elif inputfile == 'WKT':
        raw= open(geo)
        for line in raw:
            l1=str(line).replace("POLYGON ((","[[[")
            l2=str(l1).replace("))","]]]")
            l3=str(l2).replace(", ","],[")
            l4=str(l3).replace(" ",",")
            filenames = p1+l4+p2+str(start)+p3+str(end)+p4+p5+str(cloud)+p6
        with open(os.path.join(os.path.split(geo),os.path.splitext(loc)[0]+"_aoi.json"), 'w') as outfile:
            outfile.write(filenames)
            outfile.close()
        print("New structured JSON has been created at "+str(os.path.join(os.path.join(os.path.splitext(loc)[0],os.path.splitext(os.path.basename(geo))[0]+"_aoi.json"))))
