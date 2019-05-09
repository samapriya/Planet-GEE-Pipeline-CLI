__copyright__ = """

    Copyright 2019 Samapriya Roy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

import argparse
import logging
import os
import ee
import subprocess
import getpass
import time
import clipboard
import sys
import platform
from collections import Counter
from metadata_ingest import selupload
from config import setup_logging
from acl_changer import access
from ee_ls import lst
from assetsizes import assetsize
from cli_metadata import metadata
from async_download import ddownload
from planet.api.utils import write_planet_json
os.chdir(os.path.dirname(os.path.realpath(__file__)))
lpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(lpath)


def update():
    if str(platform.system()) =="Windows":
        os.system("python sel-latest-win.py")
        print("Updated selenium driver for Windows64")
    elif str(platform.system()) =="Linux":
        os.system("python sel-latest-linux.py")
        print("Updated selenium driver for Linux64")
    else:
        print("Architecture not recognized")
def update_from_parser(args):
    update()


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

def planet_key_entry(args):
    if args.type=="quiet":
        write_planet_json({'key': args.key})
    elif args.type==None and args.key==None:
        try:
            subprocess.call('planet init',shell=True)
        except Exception as e:
            print('Failed to Initialize')

def planet_quota():
    try:
        subprocess.call('python planet_quota.py',shell=True)
    except Exception as e:
        print(e)
def planet_quota_from_parser(args):
    planet_quota()

def dasync_from_parser(args):
    ddownload(infile=args.infile,
           item=args.item,
           asset=args.asset,
           start=args.start,
           end=args.end,
           cmin=args.cmin,
           cmax=args.cmax,
           dirc=args.local)

def savedsearch_from_parser(args):
    if args.limit==None:
        subprocess.call("python saved_search_download.py "+args.name+' '+args.asset+' '+args.local,shell=True)
    else:
        subprocess.call("python saved_search_download.py "+args.name+' '+args.asset+' '+args.local+' '+args.limit,shell=True)

def metadata_from_parser(args):
    metadata(asset=args.asset,mf=args.mf,mfile=args.mfile,errorlog=args.errorlog,directory=args.dir)

##Earth Engine Tools
def ee_auth_entry():
    auth_url = ee.oauth.get_authorization_url()
    clipboard.copy(auth_url)
    print("Authentication link copied: Go to browser and click paste")
    time.sleep(10)
    print("Enter your GEE API Token")
    password=str(getpass.getpass())
    auth_code=str(password)
    token = ee.oauth.request_token(auth_code)
    ee.oauth.write_token(token)
    print('\nSuccessfully saved authorization token.')
def ee_user_from_parser(args):
    ee_auth_entry()

def quota():
    quota=ee.data.getAssetRootQuota(ee.data.getAssetRoots()[0]['id'])
    print('')
    print("Total Quota: "+str(humansize(quota['asset_size']['limit'])))
    print("Used Quota: "+str(humansize(quota['asset_size']['usage'])))

def quota_from_parser(args):
    quota()

def create_from_parser(args):
    typ=str(args.typ)
    ee_path=str(args.path)
    os.system("earthengine create "+typ+" "+ee_path)

def ee_user_from_parser(args):
    ee_authorization()

def assetsize_from_parser(args):
    assetsize(asset=args.asset)
def lst_from_parser(args):
    lst(location=args.location,typ=args.typ,items=args.items,output=args.output)
def cancel_all_running_tasks():
    logging.info('Attempting to cancel all running tasks')
    running_tasks = [task for task in ee.data.getTaskList() if task['state'] == 'RUNNING']
    for task in running_tasks:
        ee.data.cancelTask(task['id'])
    logging.info('Cancel all request completed')

def cancel_all_running_tasks_from_parser(args):
    cancel_all_running_tasks()

def selupload_from_parser(args):
    selupload(user=args.user,
           source_path=args.source,
           destination_path=args.dest,
           metadata_path=args.metadata,
           nodata_value=args.nodata,
           bucket_name=args.bucket,
           manifest=args.manifest)

def access_from_parser(args):
    access(collection_path=args.asset,user=args.user,role=args.role)
def tasks():
    statuses=ee.data.getTaskList()
    st=[]
    for status in statuses:
        st.append(status['state'])
    print("Tasks Running: "+str(st.count('RUNNING')))
    print("Tasks Ready: "+str(st.count('READY')))
    print("Tasks Completed: "+str(st.count('COMPLETED')))
    print("Tasks Failed: "+str(st.count('FAILED')))
    print("Tasks Cancelled: "+str(st.count('CANCELLED')))

def tasks_from_parser(args):
    tasks()
spacing="                               "
def main(args=None):
    setup_logging()
    parser = argparse.ArgumentParser(description='Planet Pipeline with Google Earth Engine Batch Addons')

    subparsers = parser.add_subparsers()
    parser_pp1 = subparsers.add_parser(' ', help='---------------------------------------')
    parser_P = subparsers.add_parser(' ', help='-----Choose from Planet Tools Below-----')
    parser_pp2 = subparsers.add_parser(' ', help='---------------------------------------')

    parser_planet_key = subparsers.add_parser('planetkey', help='Enter your planet API Key')
    optional_named = parser_planet_key.add_argument_group('Optional named arguments')
    optional_named.add_argument('--type', help='For direct key entry type --type quiet')
    optional_named.add_argument('--key', help='Your Planet API Key')
    parser_planet_key.set_defaults(func=planet_key_entry)

    parser_planet_quota = subparsers.add_parser('pquota', help='Prints your Planet Quota Details')
    parser_planet_quota.set_defaults(func=planet_quota_from_parser)

    parser_dasync=subparsers.add_parser('dasync',help='Uses the Planet Client Async Downloader to download Planet Assets: Does not require activation')
    parser_dasync.add_argument('--infile',help='Choose a geojson from geojson.io or the aoi-json you created earlier using ppipe aoijson', required=True)
    parser_dasync.add_argument('--item',help='Choose from Planet Item types Example: PSScene4Band, PSOrthoTile, REOrthoTile etc', required=True)
    parser_dasync.add_argument('--asset',help='Choose an asset type example: anlaytic, analytic_dn,analytic_sr,analytic_xml etc', required=True)
    parser_dasync.add_argument('--local',help='Local Path where Planet Item and asset types are saved', required=True)
    parser_dasync.add_argument('--start', help='Start date filter format YYYY-MM-DD', required=True)
    parser_dasync.add_argument('--end', help='End date filter format YYYY-MM-DD', required=True)
    optional_named = parser_dasync.add_argument_group('Optional named arguments')
    optional_named.add_argument('--cmin', help='Cloud cover minimum between 0-1',default=None)
    optional_named.add_argument('--cmax', help='Cloud cover maximum between 0-1',default=None)
    parser_dasync.set_defaults(func=dasync_from_parser)

    parser_savedsearch=subparsers.add_parser('savedsearch',help='Tool to download saved searches from Planet Explorer')
    parser_savedsearch.add_argument('--name',help='Name of your saved search(It is case sensitive)')
    parser_savedsearch.add_argument('--asset',help='Choose asset type analytic, analytic_xml, analytic_sr, analytic_dn etc')
    parser_savedsearch.add_argument('--local',help='Local Path (full path address) where PlanetAssets are saved')
    optional_named = parser_savedsearch.add_argument_group('Optional named arguments')
    optional_named.add_argument('--limit', help='Choose number of assets you want to download')
    parser_savedsearch.set_defaults(func=savedsearch_from_parser)

    parser_metadata=subparsers.add_parser('metadata',help='Tool to tabulate and convert all metadata files from Planet or Digital Globe Assets')
    parser_metadata.add_argument('--asset', help='Choose PS OrthoTile(PSO)|PS OrthoTile DN(PSO_DN)|PS OrthoTile Visual(PSO_V)|PS4Band Analytic(PS4B)|PS4Band DN(PS4B_DN)|PS4Band SR(PS4B_SR)|PS3Band Analytic(PS3B)|PS3Band DN(PS3B_DN)|PS3Band Visual(PS3B_V)|RE OrthoTile (REO)|RE OrthoTile Visual(REO_V)|DigitalGlobe MultiSpectral(DGMS)|DigitalGlobe Panchromatic(DGP)|PolarGeospatial CenterDEM Strip(PGCDEM)?')
    parser_metadata.add_argument('--mf', help='Metadata folder?')
    parser_metadata.add_argument('--mfile',help='Metadata filename to be exported along with Path.csv')
    parser_metadata.add_argument('--errorlog',default='./errorlog.csv',help='Errorlog to be exported along with Path.csv')
    optional_named = parser_metadata.add_argument_group('Optional named arguments')
    optional_named.add_argument('--dir', help='Path to Image Directory to be used to get ImageTags with metadata. use only with PS4B_SR')
    parser_metadata.set_defaults(func=metadata_from_parser)

    parser_EE1 = subparsers.add_parser(' ', help='-------------------------------------------')
    parser_EE = subparsers.add_parser(' ', help='----Choose from Earth Engine Tools Below----')
    parser_EE2 = subparsers.add_parser(' ', help='-------------------------------------------')

    parser_update=subparsers.add_parser('update',help='Updates Selenium drivers for firefox [windows or linux systems]')
    parser_update.set_defaults(func=update_from_parser)

    parser_ee_user = subparsers.add_parser('ee_user', help='Get Earth Engine API Key & Paste it back to Command line/shell to change user')
    parser_ee_user.set_defaults(func=ee_user_from_parser)

    parser_quota = subparsers.add_parser('quota', help='Print Earth Engine total quota and used quota')
    parser_quota.set_defaults(func=quota_from_parser)

    parser_create = subparsers.add_parser('create',help='Allows the user to create an asset collection or folder in Google Earth Engine')
    parser_create.add_argument('--typ', help='Specify type: collection or folder', required=True)
    parser_create.add_argument('--path', help='This is the path for the earth engine asset to be created full path is needsed eg: users/johndoe/collection', required=True)
    parser_create.set_defaults(func=create_from_parser)

    parser_selupload = subparsers.add_parser('selupload', help='Batch Asset Uploader for Planet Items & Assets using Selenium')
    required_named = parser_selupload.add_argument_group('Required named arguments.')
    required_named.add_argument('--source', help='Path to the directory with images for upload.', required=True)
    required_named.add_argument('--dest', help='Destination. Full path for upload to Google Earth Engine, e.g. users/pinkiepie/myponycollection', required=True)
    required_named.add_argument('-m', '--metadata', help='Path to CSV with metadata.')
    required_named.add_argument('-mf','--manifest',help='Manifest type to be used,Choose PS OrthoTile(PSO)|PS OrthoTile DN(PSO_DN)|PS OrthoTile Visual(PSO_V)|PS4Band Analytic(PS4B)|PS4Band DN(PS4B_DN)|PS4Band SR(PS4B_SR)|PS3Band Analytic(PS3B)|PS3Band DN(PS3B_DN)|PS3Band Visual(PS3B_V)|RE OrthoTile (REO)|RE OrthoTile Visual(REO_V)')
    optional_named = parser_selupload.add_argument_group('Optional named arguments')
    optional_named.add_argument('--nodata', type=int, help='The value to burn into the raster as NoData (missing data)')
    required_named.add_argument('-u', '--user', help='Google account name (gmail address).')
    optional_named.add_argument('-b', '--bucket', help='Google Cloud Storage bucket name.')

    parser_selupload.set_defaults(func=selupload_from_parser)

    parser_lst = subparsers.add_parser('lst',help='List assets in a folder/collection or write as text file')
    required_named = parser_lst.add_argument_group('Required named arguments.')
    required_named.add_argument('--location', help='This it the location of your folder/collection', required=True)
    required_named.add_argument('--typ', help='Whether you want the list to be printed or output as text[print/report]', required=True)
    optional_named = parser_lst.add_argument_group('Optional named arguments')
    optional_named.add_argument('--items', help="Number of items to list")
    optional_named.add_argument('--output',help="Folder location for report to be exported")
    parser_lst.set_defaults(func=lst_from_parser)

    parser_assetsize = subparsers.add_parser('assetsize',help='Prints collection size in Human Readable form & Number of assets')
    parser_assetsize.add_argument('--asset', help='Earth Engine Asset for which to get size properties', required=True)
    parser_assetsize.set_defaults(func=assetsize_from_parser)

    parser_tasks=subparsers.add_parser('tasks',help='Queries current task status [completed,running,ready,failed,cancelled]')
    parser_tasks.set_defaults(func=tasks_from_parser)

    parser_access = subparsers.add_parser('access',help='Sets Permissions for items in folder')
    parser_access.add_argument('--asset', help='This is the path to the earth engine asset whose permission you are changing folder/collection/image', required=True)
    parser_access.add_argument('--user', help='Full email address of the user, try using "AllUsers" to make it public', required=True, default=False)
    parser_access.add_argument('--role', help='Choose between reader, writer or delete', required=True)
    parser_access.set_defaults(func=access_from_parser)

    parser_cancel = subparsers.add_parser('cancel', help='Cancel all running tasks')
    parser_cancel.set_defaults(func=cancel_all_running_tasks_from_parser)

    args = parser.parse_args()

    #ee.Initialize()
    args.func(args)

if __name__ == '__main__':
    main()
