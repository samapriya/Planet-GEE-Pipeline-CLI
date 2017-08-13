import subprocess
import os
import json
from pprint import pprint
import argparse
import sys
import time
import progressbar
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', help='Start date in YYYY-MM-DD?')
    parser.add_argument('--end', help='End date in YYYY-MM-DD?')
    parser.add_argument('--cloud', help='Maximum Cloud Cover(0-1) representing 0-100')
    parser.add_argument('--asset', type=str,help='Whether PlanetScope or RapidEye assets(PS/RE)')
    parser.add_argument('--geo', default='./map.geojson',help='map.geojson file')
    parser.add_argument('--activate',default='2000',help='Enter estimated time for activation')
    args = parser.parse_args()
    sys.stdout.write(str(parsed(args)))
        
def parsed(args):
    if args.asset == 'PS':
        subprocess.call("mkdir rexml psxml dgxml PlanetScope RapidEye dg", shell=False)
        raw= open(args.geo)
        for line in raw:
            fields=line.strip().split(":")[7]
            f2=fields.strip().split("}")
        with open('./poly.txt', 'w') as poly:
            poly.write(str(f2[0]))
        poly.close()
        with open('./st.txt', 'w') as strt:
            strt.write(args.start)
        strt.close()
        with open('./end.txt', 'w') as endr:
            endr.write(args.end)
        endr.close()
        with open('./cld.txt', 'w') as cld:
            cld.write(args.cloud)
        cld.close() 
        filenames = ['./p1.txt', './poly.txt','./p2.txt','./st.txt','./p3.txt','./end.txt','./p4.txt','./p5.txt','./cld.txt','./p6.txt']
        with open('./aoi.json', 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())        
        subprocess.call("python download.py --query aoi.json --activate PSOrthoTile analytic", shell=False)
        subprocess.call("python download.py --query aoi.json --activate PSOrthoTile analytic_xml", shell=False)
        bar=progressbar.ProgressBar()
        for i in bar(range(int(args.activate))):
            time.sleep(1)
        subprocess.call("python download.py --query aoi.json --download ""./PlanetScope/"" PSOrthoTile analytic", shell=False)
        subprocess.call("python download.py --query aoi.json --download ""./psxml/"" PSOrthoTile analytic_xml", shell=False)
    elif args.asset == 'RE':
        subprocess.call("mkdir rexml psxml dgxml PlanetScope RapidEye dg", shell=False)
        raw= open(args.geo)
        for line in raw:
            fields=line.strip().split(":")[7]
            f2=fields.strip().split("}")
        with open('./poly.txt', 'w') as poly:
            poly.write(str(f2[0]))
        poly.close()
        with open('./st.txt', 'w') as strt:
            strt.write(args.start)
        strt.close()
        with open('./end.txt', 'w') as endr:
            endr.write(args.end)
        endr.close()
        with open('./cld.txt', 'w') as cld:
            cld.write(args.cloud)
        cld.close() 
        filenames = ['./p1.txt', './poly.txt','./p2.txt','./st.txt','./p3.txt','./end.txt','./p4.txt','./p5.txt','./cld.txt','./p6.txt']
        with open('./aoi.json', 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())    
        subprocess.call("python download.py --query aoi.json --activate REOrthoTile analytic", shell=True)
        subprocess.call("python download.py --query aoi.json --activate REOrthoTile analytic_xml", shell=True)
        for i in range(int(args.activate)):
            print i,
            sys.stdout.flush()
            time.sleep(1)
        subprocess.call("python download.py --query aoi.json --download ""./RapidEye/"" REOrthoTile analytic", shell=True)
        subprocess.call("python download.py --query aoi.json --download ""./rexml/"" REOrthoTile analytic_xml", shell=True)        

if __name__ == '__main__':
    main()
