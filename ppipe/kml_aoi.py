import subprocess
import os
import json
from pprint import pprint
import argparse
import sys
import time
from osgeo import ogr
import csv
import shapefile
import string
p1='{"config": [{"field_name": "geometry", "config": {"type": "Polygon","coordinates":'
p2='}, "type": "GeometryFilter"}, {"field_name": "gsd", "config": {"gte":1,"lte":9.99}, "type": "RangeFilter"}, {"field_name": "acquired", "config": {"gte":"'
p3='T04:00:00.000Z","lte":"'
p4='T03:59:59.999Z"}, "type": "DateRangeFilter"}, {"field_name": "cloud_cover", "config": {"gte":0'
p5=',"lte":'
p6='}, "type": "RangeFilter"}], "type": "AndFilter"}'
def main():
    parser = argparse.ArgumentParser('Tool to convert KML, Shapefile,WKT or GeoJSON file to AreaOfInterest.JSON file with structured query for use with Planet API 1.0')
    parser.add_argument('--start', help='Start date in YYYY-MM-DD?')
    parser.add_argument('--end', help='End date in YYYY-MM-DD?')
    parser.add_argument('--cloud', help='Maximum Cloud Cover(0-1) representing 0-100')
    parser.add_argument('--geo', default='./map.geojson',help='map.geojson/aoi.kml/aoi.shp/aoi.wkt file')
    parser.add_argument('--loc',help='Output location for kml file')
    args = parser.parse_args()
    sys.stdout.write(str(parsed(args)))
        
def parsed(args):
        kml_file=args.geo
        def kml2geojson(kml_file):
            drv = ogr.GetDriverByName('KML')
            kml_ds = drv.Open(kml_file)
            for kml_lyr in kml_ds:
                for feat in kml_lyr:
                    outfile=feat.ExportToJson()
                    geom2=str(outfile).replace(", 0.0",'')
                    with open(args.loc+'./kmlout.geojson','w') as csvfile:
                        writer=csv.writer(csvfile)
                        writer.writerow([geom2])
        kml2geojson(args.geo)
        raw= open(args.loc+'./kmlout.geojson')
        for line in raw:
            fields=line.strip().split(":")[3]
            f2=fields.strip().split("}")[0]
            filenames = p1+f2+p2+str(args.start)+p3+str(args.end)+p4+p5+str(args.cloud)+p6
        with open(args.loc+'./aoi.json', 'w') as outfile:
            outfile.write(filenames)
            outfile.close()
if __name__ == '__main__':
    main()
