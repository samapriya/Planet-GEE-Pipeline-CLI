#! /usr/bin/env python

import argparse
import logging
import os
import ee
import subprocess

from batch_copy import copy
from batch_remover import delete
from batch_uploader import upload
from config import setup_logging
from query import taskquery
from batch_mover import mover
from cleanup import cleanout
from collectionprop import collprop
from taskreport import genreport
from acl_changer import access
from cli_aoi2json import aoijson
from cli_metadata import metadata

def planet_key_entry():
    os.system("planet_key.py") 
def planet_key_from_parser(args):
    planet_key_entry()
def ee_auth_entry():
    os.system("python ee_auth.py")
    print("Paste authorization link already copied to your clipboard & paste back key")
def ee_user_from_parser(args):
    ee_auth_entry()
def aoijson_from_parser(args):
    aoijson(start=args.start,end=args.end,cloud=args.cloud,inputfile=args.inputfile,geo=args.geo)
def metadata_from_parser(args):
    metadata(asset=args.asset,mf=args.mf,mfile=args.mfile,errorlog=args.errorlog)

def activatepl_from_parser(args):
    aoi_json=str(args.aoi)
    action_planet=str(args.action)
    asset_type=str(args.asst)
    try:
        os.system("download.py --query "+args.aoi+" --"+args.action+" "+asset_type)
    except Exception:
        print(' ')
def downloadpl_from_parser(args):
    aoi_json=str(args.aoi)
    action_planet=str(args.action)
    planet_pathway=str(args.pathway)
    asset_type=str(args.asst)
    try:
        os.system("download.py --query "+args.aoi+" --"+args.action+" "+args.pathway+" "+asset_type)
    except Exception:
        print(' ')
        
def cancel_all_running_tasks():
    logging.info('Attempting to cancel all running tasks')
    running_tasks = [task for task in ee.data.getTaskList() if task['state'] == 'RUNNING']
    for task in running_tasks:
        ee.data.cancelTask(task['id'])
    logging.info('Cancel all request completed')

def cancel_all_running_tasks_from_parser(args):
    cancel_all_running_tasks()
	
def delete_collection_from_parser(args):
    delete(args.id)

def upload_from_parser(args):
    upload(user=args.user,
           source_path=args.source,
           destination_path=args.dest,
           metadata_path=args.metadata,
           multipart_upload=args.large,
           nodata_value=args.nodata)
def ft_from_parser(args):
    input_file=str(args.i)
    output_ft=str(args.o)
    os.system("ogr2ft.py -i "+input_file+" -o "+output_ft)
def taskquery_from_parser(args):
    taskquery(destination=args.destination)
def mover_from_parser(args):
	mover(assetpath=args.assetpath,destinationpath=args.finalpath)
def copy_from_parser(args):
	copy(initial=args.initial,final=args.final)
def access_from_parser(args):
	copy(mode=args.mode,asset=args.asset,user=args.user)
def cleanout_from_parser(args):
    cleanout(args.dirpath)
def tasks():
    tasklist=subprocess.check_output("earthengine task list")
    taskready=tasklist.count("READY")
    taskrunning=tasklist.count("RUNNING")
    taskfailed=tasklist.count("FAILED")
    print("Running Tasks:",taskrunning)
    print("Ready Tasks:",taskready)
    print("Failed Tasks:",taskfailed)
def tasks_from_parser(args):
    tasks()
def genreport_from_parser(args):
    genreport(report=args.r)
def collprop_from_parser(args):
    collprop(imcoll=args.coll,prop=args.p)
spacing="                               "
def main(args=None):
    setup_logging()
    parser = argparse.ArgumentParser(description='Planet Pipeline with Google Earth Engine Batch Addons')

    subparsers = parser.add_subparsers()
    parser_pp1 = subparsers.add_parser(' ', help='---------------------------------------')
    parser_P = subparsers.add_parser(' ', help='-----Choose from Planet Tools Below-----')
    parser_pp2 = subparsers.add_parser(' ', help='---------------------------------------')
    
    parser_planet_key = subparsers.add_parser('planet_key', help='Enter your planet API Key')
    parser_planet_key.set_defaults(func=planet_key_from_parser)
    
    parser_aoijson=subparsers.add_parser('aoijson',help='Tool to convert KML, Shapefile,WKT,GeoJSON or Landsat WRS PathRow file to AreaOfInterest.JSON file with structured query for use with Planet API 1.0')
    parser_aoijson.add_argument('--start', help='Start date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--end', help='End date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--cloud', help='Maximum Cloud Cover(0-1) representing 0-100')
    parser_aoijson.add_argument('--inputfile',help='Choose a kml/shapefile/geojson or WKT file for AOI(KML/SHP/GJSON/WKT) or WRS (6 digit RowPath Example: 023042)')
    parser_aoijson.add_argument('--geo', default='./map.geojson',help='map.geojson/aoi.kml/aoi.shp/aoi.wkt file')    
    parser_aoijson.set_defaults(func=aoijson_from_parser)

    parser_activatepl=subparsers.add_parser('activatepl',help='Tool to query and/or activate Planet Assets')
    parser_activatepl.add_argument('--aoi', help='Choose aoi.json file created earlier')
    parser_activatepl.add_argument('--action', help='choose between check/activate')
    parser_activatepl.add_argument('--asst',help='Choose between planet asset types (PSOrthoTile analytic/REOrthoTile analytic/PSOrthoTile analytic_xml/REOrthoTile analytic_xml')
    parser_activatepl.set_defaults(func=activatepl_from_parser)

    parser_downloadpl=subparsers.add_parser('downloadpl',help='Tool to download Planet Assets')
    parser_downloadpl.add_argument('--aoi', help='Choose aoi.json file created earlier')
    parser_downloadpl.add_argument('--action', help='choose download')
    parser_downloadpl.add_argument('--asst',help='Choose between planet asset types (PSOrthoTile analytic/REOrthoTile analytic/PSOrthoTile analytic_xml/REOrthoTile analytic_xml')
    parser_downloadpl.add_argument('--pathway',help='Folder Pathways where PlanetAssets are saved exampled ./PlanetScope ./RapidEye')
    parser_downloadpl.set_defaults(func=downloadpl_from_parser)

    parser_metadata=subparsers.add_parser('metadata',help='Tool to tabulate and convert all metadata files from Planet or Digital Globe Assets')
    parser_metadata.add_argument('--asset', help='Choose RapidEye/PlantScope/DigitalGlobe MultiSpectral/DigitalGlobe Panchromatic (RE/PS/DGMS/DGP)?')
    parser_metadata.add_argument('--mf', help='Metadata folder?')
    parser_metadata.add_argument('--mfile',help='Metadata filename to be exported along with Path.csv')
    parser_metadata.add_argument('--errorlog',default='./errorlog.csv',help='Errorlog to be exported along with Path.csv')
    parser_metadata.set_defaults(func=metadata_from_parser)

    parser_EE1 = subparsers.add_parser(' ', help='-------------------------------------------')
    parser_EE = subparsers.add_parser(' ', help='----Choose from Earth Engine Tools Below----')
    parser_EE2 = subparsers.add_parser(' ', help='-------------------------------------------')

    parser_ee_user = subparsers.add_parser('ee_user', help='Get Earth Engine API Key & Paste it back to Command line/shell to change user')
    parser_ee_user.set_defaults(func=ee_user_from_parser)
    
    parser_upload = subparsers.add_parser('upload', help='Batch Asset Uploader to Earth Engine.')
    required_named = parser_upload.add_argument_group('Required named arguments.')
    required_named.add_argument('-u', '--user', help='Google account name (gmail address).', required=True)
    required_named.add_argument('--source', help='Path to the directory with images for upload.', required=True)
    required_named.add_argument('--dest', help='Destination. Full path for upload to Google Earth Engine, e.g. users/pinkiepie/myponycollection', required=True)
    optional_named = parser_upload.add_argument_group('Optional named arguments')
    optional_named.add_argument('-m', '--metadata', help='Path to CSV with metadata.')
    optional_named.add_argument('--large', action='store_true', help='(Advanced) Use multipart upload. Might help if upload of large '
                                                                     'files is failing on some systems. Might cause other issues.')
    optional_named.add_argument('--nodata', type=int, help='The value to burn into the raster as NoData (missing data)')
    parser_upload.set_defaults(func=upload_from_parser)
    
    parser_delete = subparsers.add_parser('delete', help='Deletes collection and all items inside. Supports Unix-like wildcards.')
    parser_delete.add_argument('id', help='Full path to asset for deletion. Recursively removes all folders, collections and images.')
    parser_delete.set_defaults(func=delete_collection_from_parser)

    parser_tasks=subparsers.add_parser('tasks',help='Queries currently running, enqued,failed')
    parser_tasks.set_defaults(func=tasks_from_parser)
    
    parser_taskquery=subparsers.add_parser('taskquery',help='Queries currently running, enqued,failed ingestions and uploaded assets')
    parser_taskquery.add_argument('--destination',help='Full path to asset where you are uploading files')
    parser_taskquery.set_defaults(func=taskquery_from_parser)

    parser_genreport=subparsers.add_parser('report',help='Create a report of all tasks and exports to a CSV file')
    parser_genreport.add_argument('--r',help='Folder Path where the reports will be saved')
    parser_genreport.set_defaults(func=genreport_from_parser)

    parser_cancel = subparsers.add_parser('cancel', help='Cancel all running tasks')
    parser_cancel.set_defaults(func=cancel_all_running_tasks_from_parser)
    
    parser_mover=subparsers.add_parser('mover',help='Moves all assets from one collection to another')
    parser_mover.add_argument('--assetpath',help='Existing path of assets')
    parser_mover.add_argument('--finalpath',help='New path for assets')
    parser_mover.set_defaults(func=mover_from_parser)

    parser_copy=subparsers.add_parser('copy',help='Copies all assets from one collection to another: Including copying from other users if you have read permission to their assets')
    parser_copy.add_argument('--initial',help='Existing path of assets')
    parser_copy.add_argument('--final',help='New path for assets')
    parser_copy.set_defaults(func=copy_from_parser)

    parser_ft = subparsers.add_parser('access',help='Sets Permissions for Images, Collection or all assets in EE Folder Example: python ee_permissions.py --mode "folder" --asset "users/john/doe" --user "jimmy@doe.com:R"')
    parser_ft.add_argument('--mode', help='This lets you select if you want to change permission or folder/collection/image', required=True)
    parser_ft.add_argument('--asset', help='This is the path to the earth engine asset whose permission you are changing folder/collection/image', required=True)
    parser_ft.add_argument('--user', help="""This is the email address to whom you want to give read or write permission Usage: "john@doe.com:R" or "john@doe.com:W" R/W refers to read or write permission""", required=True, default=False)
    parser_ft.set_defaults(func=access_from_parser)

    parser_collprop=subparsers.add_parser('collprop',help='Sets Overall Properties for Image Collection')
    parser_collprop.add_argument('--coll',help='Path of Image Collection')
    parser_collprop.add_argument('--p',help='"system:description=Description"/"system:provider_url=url"/"system:tags=tags"/"system:title=title')
    parser_collprop.set_defaults(func=collprop_from_parser)
    
    parser_ft = subparsers.add_parser('convert2ft',help='Uploads a given feature collection to Google Fusion Table.')
    parser_ft.add_argument('--i', help='input feature source (KML, SHP, SpatiLite, etc.)', required=True)
    parser_ft.add_argument('--o', help='output Fusion Table name', required=True)
    parser_ft.add_argument('--add_missing', help='add missing features from the last inserted feature index', action='store_true', required=False, default=False)
    parser_ft.set_defaults(func=ft_from_parser)

    parser_cleanout=subparsers.add_parser('cleanout',help='Clear folders with datasets from earlier downloaded')
    parser_cleanout.add_argument('--dirpath',help='Folder you want to delete after all processes have been completed')
    parser_cleanout.set_defaults(func=cleanout_from_parser)

    args = parser.parse_args()

    ee.Initialize()
    args.func(args)

if __name__ == '__main__':
    main()
