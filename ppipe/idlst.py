#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import os
import csv
import sys
from planet.api.utils import read_planet_json
from planet.api.auth import find_api_key
os.chdir(os.path.dirname(os.path.realpath(__file__)))
pathway=os.path.dirname(os.path.realpath(__file__))

try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')


def handle_page(page,asset,num):
    if num<250:
        n=0
        for items in page['features']:
            for itm in items['_permissions']:
                if itm.split(':')[0]=="assets."+asset and n<num:
                    it=items.get('id')
                    print(it)
                    n=n+1
                    with open(os.path.join(pathway,"idpl.csv"),'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([it])
                    with open(os.path.join(pathway,"idpl.txt"), 'a') as the_file:
                        the_file.write(it+'\n')
        sys.exit()
    else:
        n=0
        for items in page['features']:
            for itm in items['_permissions']:
                if itm.split(':')[0]=="assets."+asset and n<num:
                    it=items.get('id')
                    print(it)
                    n=n+1
                    with open(os.path.join(pathway,"idpl.csv"),'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([it])
        data=csv.reader(open(os.path.join(pathway,"idpl.csv")).readlines()[1: num])

        with open(os.path.join(pathway,"idpl.csv"), "wb") as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)
        open(os.path.join(pathway,"idpl.txt"), 'w')
        dat=open(os.path.join(pathway,"idpl.csv")).readlines()
        with open(os.path.join(pathway,"idpl.txt"), 'a') as the_file:
            for row in dat:
                the_file.write(row)

def idl(infile,item,asset,num):
    with open(os.path.join(pathway,"idpl.csv"),'wb') as csvfile:
        writer=csv.DictWriter(csvfile,fieldnames=["id"], delimiter=',')
        writer.writeheader()
    open(os.path.join(pathway,"idpl.txt"), 'w')
    headers = {'Content-Type': 'application/json'}
    PL_API_KEY = read_planet_json()['key']
## Create Empty CSV File for ID List

## Null payload structure
    data = {'filter': {'type': 'AndFilter',
            'config': [{'type': 'GeometryFilter', 'field_name': 'geometry',
            'config': {'type': 'Polygon', 'coordinates': []}},
            {'type': 'OrFilter', 'config': [{'type': 'AndFilter',
            'config': [{'type': 'StringInFilter', 'field_name': 'item_type'
            , 'config': []}, {'type': 'RangeFilter',
            'field_name': 'cloud_cover', 'config': {'gte': [],
            'lte': []}}, {'type': 'RangeFilter',
            'field_name': 'sun_elevation', 'config': {'gte': 0,
            'lte': 90}}]}]}, {'type': 'OrFilter',
            'config': [{'type': 'DateRangeFilter', 'field_name': 'acquired'
            , 'config': {'gte': [],
            'lte': []}}]}]},
            'item_types': []}

## Read input json file
    with open(infile) as aoi:
        aoi_resp = json.load(aoi)
        for items in aoi_resp['config']:
            aoi_geom = aoi_resp['config'][0]['config']['coordinates']
            data['filter']['config'][0]['config']['coordinates'] = aoi_geom
            if items['field_name'] == 'acquired':
                data['filter']['config'][2]['config'][0]['config']['gte'] = \
                    str(items['config']['gte']).replace('u', '')  # Date GTE
                data['filter']['config'][2]['config'][0]['config']['lte'] = \
                    str(items['config']['lte']).replace('u', '')  # Date GTE
            if items['field_name'] == 'cloud_cover':
                data['filter']['config'][1]['config'][0]['config'
                        ][1]['config']['gte'] = items['config']['gte']  # Cloud_Cover GTE
                data['filter']['config'][1]['config'][0]['config'
                        ][1]['config']['lte'] = items['config']['lte']  # Cloud Cover LTE
            data['filter']['config'][1]['config'][0]['config'][0]['config'
                    ] = [item]
            data['item_types'] = [item]
        data = str(data).replace("'", '"')

## Send post request
    result = requests.post('https://api.planet.com/data/v1/quick-search',
                           headers=headers, data=data,
                           auth=(PL_API_KEY, ''))
    page=result.json()
    final_list = handle_page(page,asset,num)
    while page['_links'].get('_next') is not None:
        page_url = page['_links'].get('_next')
        page = SESSION.get(page_url).json()
        ids = handle_page(page,asset,num)

##idl(infile=r"C:\Users\samapriya\Box Sync\IUB\Pycodes\Applications and Tools\Earth Engine Codes\EE_Manifests\aoi\bart_aoi.json",
##    item="PSScene3Band",asset="visual",num=18)
