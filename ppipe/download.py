#!/usr/bin/env python

import argparse
import os
import requests
import json
import sys
import logging
import datetime
import urllib3
import psutil
import csv
from retrying import retry
from os.path import expanduser
#from urllib3 import PoolManager
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings()

ASSET_URL = 'https://api.planet.com/data/v1/item-types/{}/items/{}/assets/'
SEARCH_URL = 'https://api.planet.com/data/v1/quick-search'
pkey=expanduser("~/.config/planet/pkey.csv")
f=open(pkey)
for row in csv.reader(f):
    #print(str(row).strip("[']"))
    os.environ['PLANET_API_KEY']=str(row).strip("[']")

# set up auth
SESSION = requests.Session()
SESSION.auth = (os.environ.get('PLANET_API_KEY'), '')

BASE_QUERY_STRING = '''{"config": [{"field_name": "geometry", "config": {"type": "Polygon", "coordinates": %s}, "type": "GeometryFilter"}, {"field_name": "acquired", "config": {"gte": "%s", "lte": "%s"}, "type": "DateRangeFilter"}], "type": "AndFilter"}'''
SAT_FILTER_QUERY_DICT = { "field_name": "satellite_id", "config": [], "type": "StringInFilter"}

class RateLimitException(Exception):
    pass


def handle_page(page):
    return [item['id'] for item in page['features']]


def retry_if_rate_limit_error(exception):
    """Return True if we should retry (in this case when it's a rate_limit
    error), False otherwise"""
    return isinstance(exception, RateLimitException)


def check_status(result, msg=None, text=True):

    if text:
        logging.info('Response: {} - {}'.format(result.status_code, result.text))
    else:
        # Logging option for when the result is a massive geotif
        logging.info('Response: {}'.format(result.status_code))

    if result.status_code == 429:
        error_msg = 'Error code 429: rate limit exceeded - retrying'
        print(error_msg)
        raise RateLimitException('Rate limit error')
    elif result.status_code == 401:
        error_msg = "Error code 401: the API Key you provided is invalid, or does not have the required permissions for this AOI or TOI.\n 1. Ensure your API key is stored in your *nix environment ('export PLANET_API_KEY=Your_API_Key'), or passed as an argument in the command ('--key Your_API_Key')\n 2. Check that it is correct at http://planet.com/account\n 3. Confirm you have the right permissions to access this AOI and TOI with your Account Manager"
        print(error_msg)
        sys.exit(1)
    elif result.status_code == 400:
        error_msg = 'Error code {}: {}'.format(result.status_code, result.text)
        print(error_msg)
        sys.exit(1)
    else:
        if msg:
            print(msg)
        return True


def parse_bbox_args(args):
    assert args.bbox

    def parse_date(date_str):
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').isoformat()

    if args.start_date:
        start = parse_date(args.start_date)
    else:
        raise Exception('Use of --bbox argument requires use of --start-date argument')

    if args.end_date:
        end = parase_date(args.end_date)
    else:
        end = datetime.datetime.utcnow().isoformat()

    # tack on a Z for full compliance with RFC 3339
    if not start.endswith('Z'):
        start += 'Z'
    if not end.endswith('Z'):
        end += 'Z'

    return args.bbox, start, end


def bbox_to_coords(bbox):
    xmin, ymin, xmax, ymax = [float(i) for i in bbox]
    coords = [[[xmin, ymax], [xmin, ymin], [xmax, ymin],
              [xmax, ymax], [xmin, ymax]]]
    return coords


def build_bbox_query(bbox, start, end, sat_list=None):
    coords = bbox_to_coords(bbox)
    query = BASE_QUERY_STRING % (coords, start, end)
    query = json.loads(query)

    if sat_list:
        SAT_FILTER_QUERY_DICT['config'] = sat_list
        query['config'].append(SAT_FILTER_QUERY_DICT)
    return query


def filter_ids_by_sat(id_list, sat_list):
    '''For when we can't do server-side filtering'''
    return [img_id for sat_id in sat_list for img_id in id_list
            if sat_id in img_id]


def build_query(args, sat_list=None):
    if args.query:
        # load query from json file
        try:
            with open(args.query, 'r') as fp:
                query = json.load(fp)
        except:
            print("Error: could not load JSON file " + args.query + ". Please check it exists, and that the syntax is valid at http://jsonlint.com/.")
            raise

    # build bbox query and add sat_list filter if supplied
    else:
        bbox, start, end = parse_bbox_args(args)

        if sat_list:
            query = build_bbox_query(bbox, start, end, sat_list)
        else:
            query = build_bbox_query(bbox, start, end)

    return query


@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000,
    retry_on_exception=retry_if_rate_limit_error,
    stop_max_attempt_number=5)
def run_search(search_request):
    print('Searching...')

    logging.info('Request: {} - {}'.format(SEARCH_URL, search_request))

    result = SESSION.post(SEARCH_URL, json=search_request)

    check_status(result)

    page = result.json()
    final_list = handle_page(page)

    while page['_links'].get('_next') is not None:
        page_url = page['_links'].get('_next')
        page = SESSION.get(page_url).json()
        ids = handle_page(page)
        final_list += ids

    return [fid for fid in final_list]


@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000,
    retry_on_exception=retry_if_rate_limit_error,
    stop_max_attempt_number=5)
def activate(item_id, item_type, asset_type):
    url = ASSET_URL.format(item_type, item_id)
    logging.info('Request: {}'.format(url))

    result = SESSION.get(url)

    check_status(result)

    try:
        status = result.json()[asset_type]['status']
        if status == 'active':
            print('{} {} {}: already active'.format(item_id, asset_type, item_type))
            return False
        else:
            item_activation_url = result.json()[asset_type]['_links']['activate']

            result = SESSION.post(item_activation_url)

            msg = '{} {} {}: started activation'.format(item_id, item_type, asset_type)
            return check_status(result, msg)
    except KeyError:
        print('Could not activate - asset type \'{}\' not found for {}'.format(asset_type, item_id))
        return False


@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000,
    retry_on_exception=retry_if_rate_limit_error,
    stop_max_attempt_number=5)
def check_activation(item_id, item_type, asset_type):
    url = ASSET_URL.format(item_type, item_id)
    logging.info('Request: {}'.format(url))
    result = SESSION.get(url)

    check_status(result)

    try:
        status = result.json()[asset_type]['status']
        msg = '{} {} {}: {}'.format(item_id, item_type, asset_type, status)
        print(msg)

        if status == 'active':
            return True
        else:
            return False
    except KeyError:
        print('Could not check activation status - asset type \'{}\' not found for {}'.format(asset_type, item_id))
        return False


@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000,
    retry_on_exception=retry_if_rate_limit_error,
    stop_max_attempt_number=5)
def download(url, path, item_id, asset_type, overwrite):
    fname = '{}_{}.tif'.format(item_id, asset_type)
    local_path = os.path.join(path, fname)

    if not overwrite and os.path.exists(local_path):
        print('File {} exists - skipping ...'.format(local_path))
    else:
        print('Downloading file to {}'.format(local_path))

        logging.info('Request: {}'.format(url))
        # memory-efficient download, per
        # stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
        result = requests.get(url)

        if check_status(result, text=False):
            f = open(local_path, 'wb')
            for chunk in result.iter_content(chunk_size=512 * 1024):
                # filter out keep-alive new chunks
                if chunk:
                    f.write(chunk)
            f.close()

    return True

def size(url, path, item_id, asset_type, overwrite):
    fname = '{}_{}.tif'.format(item_id, asset_type)
    logging.info('Request: {}'.format(url))
    result = requests.get(url)
    print path
    return True


def process_activation(func, id_list, item_type, asset_type, activate_or_check):
    results = []

    for item_id in id_list:
        result = func(item_id, item_type, asset_type)
        results.append(result)

    if activate_or_check == 'activate':
        msg = 'Requested activation for {} of {} items'
        print(msg.format(results.count(True), len(results)))

    if activate_or_check == 'check':
        msg = '{} of {} items are active'
        print(msg.format(results.count(True), len(results)))

    return results

def process_download(path, id_list, item_type, asset_type, overwrite):
    results = []

    # check on directory structure
    if not os.path.exists(path):
        os.system("mkdir "+path)
        print('Directory {} does not exist - being created.'.format(path))

    # now start downloading each file
    for item_id in id_list:
        url = ASSET_URL.format(item_type, item_id)
        logging.info('Request: {}'.format(url))
        result = SESSION.get(url)

        check_status(result)

        try:
            if result.json()[asset_type]['status'] == 'active':
                download_url = result.json()[asset_type]['location']
                result = download(download_url, path, item_id, asset_type, overwrite)
            else:
                result = False
        except KeyError:
            print('Could not check activation status - asset type \'{}\' not found for {}'.format(asset_type, item_id))
            result = False


        results.append(result)

    msg = 'Successfully downloaded {} of {} files to {}. {} were not active.'
    print(msg.format(results.count(True), len(results), args.download, results.count(False)))

    return results

def process_size(path, id_list, item_type, asset_type, overwrite):
    results = []
    summation=0
    path= args.size
    spc=psutil.disk_usage(path).free
    remain=float(spc)/1073741824
    # now start downloading each file
    for item_id in id_list:
        url = ASSET_URL.format(item_type, item_id)
        logging.info('Request: {}'.format(url))
        result = SESSION.get(url)
        check_status(result)
        try:
            if result.json()[asset_type]['status'] == 'active':
                download_url = result.json()[asset_type]['location']
                #print(download_url)
                pool = PoolManager()
                response = pool.request("GET", download_url, preload_content=False)
                max_bytes = 100000000000
                content_bytes = response.headers.get("Content-Length")
                print("Item-ID: "+str(item_id))
                #print(int(content_bytes)/1048576,"MB")
                summary=float(content_bytes)/1073741824
                summation=summation+summary
                #print ("Total Size in MB",summation)
            else:
                result = False
        except KeyError:
            print('Could not check activation status - asset type \'{}\' not found for {}'.format(asset_type, item_id))
            result = False
        

        results.append(result)
    #print(remain,"MB")
    print("Remaining Space in MB",format(float(remain*1024),'.2f'))
    print("Remaining Space in GB",format(float(remain),'.2f'))
    print ("Total Size in MB",format(float(summation*1024),'.2f'))
    print ("Total Size in GB",format(float(summation),'.2f'))
    return results



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--idlist', help='Location of file containing image ids (one per line) to process')
    parser.add_argument('--query', help='Path to json file containing query')
    parser.add_argument('--search', help='Search for images', action='store_true')
    parser.add_argument('--bbox', help='Bounding box for query in geographic (latlon) coordinates',
                        metavar=('XMIN', 'YMIN', 'XMAX', 'YMAX'), nargs=4)
    parser.add_argument('--activate', help='Activate assets', action='store_true')
    parser.add_argument('--check', help='Check activation status', action='store_true')
    parser.add_argument('--size',help='Check total size of download in MB')
    parser.add_argument('--download', help='Path where downloaded files should be stored')
    parser.add_argument('--overwrite', help='Overwrite existing downloads', action='store_true')
    parser.add_argument('--start-date', help='Start date for query (e.g. 2016-01-01)')
    parser.add_argument('--end-date', help='End date for query (e.g. 2016-04-01) - optional: uses current date if not supplied along with start date')
    parser.add_argument('--satlist', help='Location of file containing satellite ids (one per line) to use for filter')
    parser.add_argument('--sats', help='Alternative to --satlist, no need for an external file. #dovecrush', nargs='*')
    parser.add_argument('--key', help='Set API key')
    parser.add_argument('--debug', help='Debug mode', action='store_true')
    parser.add_argument('item', help='Item type (e.g. REOrthoTile or PSOrthoTile)')
    parser.add_argument('asset', help='Asset type (e.g. visual, analytic, analytic_xml)')

    args = parser.parse_args()

    # override API key taken from environment (possibly missing)
    if args.key:
        SESSION.auth = (args.key, '')

    # ensure there's a way to retrieve a list of image ids
    if not args.idlist and not args.query and not args.bbox:
        parser.error('Error: please supply an --idlist, --query, or --bbox argument.')

    # set log level if --debug
    if args.debug:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    # handle list of sat ids if there is one
    if args.satlist and args.sats:
        raise Exception('Error: please specify only one of --satlist or --sats.')
    elif args.satlist:
        with open(args.satlist) as f:
            sat_list = [i.strip() for i in f.readlines()]
    elif args.sats:
        sat_list = args.sats
    else:
        sat_list = None

    # load list of image ids, filtering by sat id if appropriate
    if args.idlist:
        with open(args.idlist) as f:
            id_list = [i.strip() for i in f.readlines()]

        if sat_list:
            id_list = filter_ids_by_sat(id_list, sat_list)

    # otherwise, load query from file or build from scratch
    else:
        if sat_list:
            query = build_query(args, sat_list)
        else:
            query = build_query(args)

    # if we don't have a list of image ids already, create and run
    # the final query!
    if not args.idlist:
        # Create full search request object
        search_payload = {'item_types': [args.item], 'filter': query}

        id_list = run_search(search_payload)

        # Special case to do sat id filtering for a "standard" user-supplied
        # JSON query. This is needed because we don't want to try to parse/modify
        # the user's original query.
        if args.query and sat_list:
            id_list = filter_ids_by_sat(id_list, sat_list)

    # ok we've got our list of image ids, let's do some stuff
    print('%d available images' % len(id_list))

    # nothing more to be done if we're just searching
    if args.search:
        pass

    # start activation for all images in id_list
    elif args.activate:
        results = process_activation(activate, id_list, args.item,
                                     args.asset, 'activate')

    # check activation status
    elif args.check:
        results = process_activation(check_activation, id_list, args.item,
                                     args.asset, 'check')

    # download everything
    elif args.download:
        results = process_download(args.download, id_list, args.item,
                                   args.asset, args.overwrite)
    # check size
    elif args.size:
        results = process_size(args.download, id_list, args.item,
                                   args.asset, args.overwrite)

    else:
        parser.error('Error: no action supplied. Please check help (--help) or revise command.')


'''Sample commands, for testing.
python download.py --query aoi.json --size "D:\Library\PlanetScope" PSOrthoTile analytic
python download.py --query redding.json --search PSScene3Band visual
python download.py --query redding.json --check PSScene3Band visual
python download.py --query redding.json --activate PSScene3Band visual
python download.py --query redding.json --download /tmp PSScene3Band visual
python download.py --idlist ids_small.txt --check PSScene3Band visual
python download.py --idlist ids_small.txt --activate PSScene3Band visual
python download.py --idlist ids_small.txt --download /tmp PSScene3Band visual
python download.py --search --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01
python download.py --check --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01
python download.py --check --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-08-01 --end-date 2016-12-31
python download.py --activate --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01
python download.py --download ~/Downloads/ --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01
python download.py --query redding.json --search PSScene3Band visual --satlist sats_redding.txt
python download.py --query redding.json --search PSScene3Band visual --sats 0c2b 0c19
python download.py --query redding.json --sats 0c2b 0c19 --search PSScene3Band visual
python download.py --search --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01 --sats 0e0e 0c38
python download.py --check --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01 --sats 0e0e 0c38
python download.py --check --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-08-01 --end-date 2016-12-31 --sats 0e0e 0c38
python download.py --search --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01 --satlist sats_miami.txt
python download.py --check --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01 --sats sats_miami.txt
python download.py --check --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-08-01 --end-date 2016-12-31 --sats 0e0e 0c38
python download.py --activate --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01 --sats sats_miami.txt
python download.py --activate --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-08-01 --end-date 2016-12-31 --sats 0e0e 0c38
python download.py --activate --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01
python download.py --download ~/Downloads/ --bbox -80.209624 25.7777338 -80 26 PSOrthoTile analytic --start-date 2016-01-01
'''
