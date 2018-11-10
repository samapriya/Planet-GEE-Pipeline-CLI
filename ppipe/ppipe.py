#! /usr/bin/env python

import argparse,logging,os,ee,subprocess,getpass,csv,re,time,clipboard
import sys
from collections import Counter
from ee import oauth
from batch_copy import copy
from batch_remover import delete
from batch_uploader import upload
from config import setup_logging
from batch_mover import mover
from taskrep import genreport
from acl_changer import access
from ee_ls import lst
from assetsizes import assetsize
from ee_report import ee_report
from cli_aoi2json import aoijson
from cli_metadata import metadata
from async_download import ddownload
from idlst import idl
from os.path import expanduser
from planet.api.utils import write_planet_json
os.chdir(os.path.dirname(os.path.realpath(__file__)))
lpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(lpath)
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

def aoijson_from_parser(args):
    aoijson(start=args.start,end=args.end,cloud=args.cloud,inputfile=args.inputfile,geo=args.geo,loc=args.loc)

def idl_from_parser(args):
    idl(infile=args.aoi,item=args.item,asset=args.asset,num=int(args.number))

def activatepl_from_parser(args):
    if args.aoi==None:
        asset_type=str(args.asset)
        subprocess.call("python download.py --idlist "+'"'+"idpl.txt"+'" '+"--activate "+asset_type,shell=True)
    else:
        aoi_json=str(args.aoi)
        asset_type=str(args.asset)
        subprocess.call("python download.py --query "+'"'+aoi_json+'" '+"--activate "+asset_type,shell=True)

def space_from_parser(args):
    aoi=args.aoi
    local=str(args.local)
    asset=str(args.asset)
    try:
        subprocess.call("python download.py --query "+'"'+aoi+'"'+" --size "+'"'+local+'" '+asset.split(" ")[0]+" "+asset.split(" ")[1],shell=True)
    except Exception:
        print(' ')

def downloadpl_from_parser(args):
    if args.aoi==None:
        subprocess.call("python download.py --idlist "+'"'+"idpl.txt"+'" '+"--download "+args.local+" "+args.asset,shell=True)
    else:
        aoi_json=str(args.aoi)
        planet_pathway=str(args.local)
        asset_type=str(args.asset)
        try:
            subprocess.call("python download.py --query "+'"'+args.aoi+'" '+" --download "+'"'+args.local+'"'+" "+args.asset,shell=True)
        except Exception:
            print(' ')

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

def genreport_from_parser(args):
    genreport(report=args.r)

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

def delete_collection_from_parser(args):
    delete(args.id)

def upload_from_parser(args):
    upload(user=args.user,
           source_path=args.source,
           destination_path=args.dest,
           metadata_path=args.metadata,
           multipart_upload=args.large,
           nodata_value=args.nodata,
           bucket_name=args.bucket,
           manifest=args.manifest)
def ee_report_from_parser(args):
    ee_report(output=args.outfile)

def mover_from_parser(args):
	mover(assetpath=args.assetpath,destinationpath=args.finalpath)
def copy_from_parser(args):
	copy(initial=args.initial,final=args.final)
def access_from_parser(args):
	access(mode=args.mode,asset=args.asset,user=args.user)
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

    parser_aoijson=subparsers.add_parser('aoijson',help='Tool to convert KML, Shapefile,WKT,GeoJSON or Landsat WRS PathRow file to AreaOfInterest.JSON file with structured query for use with Planet API 1.0')
    parser_aoijson.add_argument('--start', help='Start date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--end', help='End date in YYYY-MM-DD?')
    parser_aoijson.add_argument('--cloud', help='Maximum Cloud Cover(0-1) representing 0-100')
    parser_aoijson.add_argument('--inputfile',help='Choose a kml/shapefile/geojson or WKT file for AOI(KML/SHP/GJSON/WKT) or WRS (6 digit RowPath Example: 023042)')
    parser_aoijson.add_argument('--geo', default='./map.geojson',help='map.geojson/aoi.kml/aoi.shp/aoi.wkt file')
    parser_aoijson.add_argument('--loc', help='Location where aoi.json file is to be stored')
    parser_aoijson.set_defaults(func=aoijson_from_parser)

    parser_idl=subparsers.add_parser('idlist',help='Creates an IDLIST that intersects AOI JSON')
    parser_idl.add_argument('--aoi', help='Choose aoi.json file created earlier')
    parser_idl.add_argument('--item', help='choose between Planet Item types PSOrthoTile|PSScene4Band|PSScene3Band|REOrthoTile')
    parser_idl.add_argument('--asset',help='Choose between Planet asset types analytic|analytic_dn|visual')
    parser_idl.add_argument('--number',help='Maximum number of assets for the idlist')
    parser_idl.set_defaults(func=idl_from_parser)

    parser_activatepl=subparsers.add_parser('activatepl',help='Tool to activate Planet Assets')
    parser_activatepl.add_argument('--asset',help='Choose between planet asset types (PSOrthoTile analytic/PSOrthoTile analytic_dn/PSOrthoTile visual/PSScene4Band analytic/PSScene4Band analytic_dn/PSScene3Band analytic/PSScene3Band analytic_dn/PSScene3Band visual/REOrthoTile analytic/REOrthoTile visual')
    optional_named = parser_activatepl.add_argument_group('Optional named arguments')
    optional_named.add_argument('--aoi', help='Choose aoi.json file created earlier')
    parser_activatepl.set_defaults(func=activatepl_from_parser)

    parser_space=subparsers.add_parser('space',help='Tool to query total download size of activated assets & local space left for download')
    parser_space.add_argument('--aoi', help='Choose aoi.json file created earlier')
    parser_space.add_argument('--local', help='local path where you are downloading assets')
    parser_space.add_argument('--asset',help='Choose between planet asset types (PSOrthoTile analytic/PSOrthoTile analytic_dn/PSOrthoTile visual/PSScene4Band analytic/PSScene4Band analytic_dn/PSScene3Band analytic/PSScene3Band analytic_dn/PSScene3Band visual/REOrthoTile analytic/REOrthoTile visual')
    parser_space.set_defaults(func=space_from_parser)

    parser_downloadpl=subparsers.add_parser('downloadpl',help='Tool to download Planet Assets')
    parser_downloadpl.add_argument('--asset',help='Choose between planet asset types or for Metadata follow by _xml Eg: PSOrthoTile analytic_xml--->Assets Include:(PSOrthoTile analytic/PSOrthoTile analytic_dn/PSOrthoTile visual/PSScene4Band analytic/PSScene4Band analytic_dn/PSScene3Band analytic/PSScene3Band analytic_dn/PSScene3Band visual/REOrthoTile analytic/REOrthoTile visual')
    parser_downloadpl.add_argument('--local',help='Local Pathways where PlanetAssets are saved exampled ./PlanetScope ./RapidEye')
    optional_named = parser_downloadpl.add_argument_group('Optional named arguments')
    optional_named.add_argument('--aoi', help='Choose aoi.json file created earlier')
    parser_downloadpl.set_defaults(func=downloadpl_from_parser)

    parser_dasync=subparsers.add_parser('dasync',help='Uses the Planet Client Async Downloader to download Planet Assets: Does not require activation')
    parser_dasync.add_argument('--infile',help='Choose a geojson from geojson.io or the aoi-json you created earlier using ppipe aoijson')
    parser_dasync.add_argument('--item',help='Choose from Planet Item types Example: PSScene4Band, PSOrthoTile, REOrthoTile etc')
    parser_dasync.add_argument('--asset',help='Choose an asset type example: anlaytic, analytic_dn,analytic_sr,analytic_xml etc')
    parser_dasync.add_argument('--local',help='Local Path where Planet Item and asset types are saved')
    optional_named = parser_dasync.add_argument_group('Optional named arguments')
    optional_named.add_argument('--start', help='Start date filter format YYYY-MM-DD',default=None)
    optional_named.add_argument('--end', help='End date filter format YYYY-MM-DD',default=None)
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

    parser_ee_user = subparsers.add_parser('ee_user', help='Get Earth Engine API Key & Paste it back to Command line/shell to change user')
    parser_ee_user.set_defaults(func=ee_user_from_parser)

    parser_quota = subparsers.add_parser('quota', help='Print Earth Engine total quota and used quota')
    parser_quota.set_defaults(func=quota_from_parser)

    parser_create = subparsers.add_parser('create',help='Allows the user to create an asset collection or folder in Google Earth Engine')
    parser_create.add_argument('--typ', help='Specify type: collection or folder', required=True)
    parser_create.add_argument('--path', help='This is the path for the earth engine asset to be created full path is needsed eg: users/johndoe/collection', required=True)
    parser_create.set_defaults(func=create_from_parser)

    parser_upload = subparsers.add_parser('upload', help='Batch Asset Uploader.')
    required_named = parser_upload.add_argument_group('Required named arguments.')
    required_named.add_argument('--source', help='Path to the directory with images for upload.', required=True)
    required_named.add_argument('--dest', help='Destination. Full path for upload to Google Earth Engine, e.g. users/pinkiepie/myponycollection', required=True)
    required_named.add_argument('-m', '--metadata', help='Path to CSV with metadata.')
    required_named.add_argument('-mf','--manifest',help='Manifest type to be used,Choose PS OrthoTile(PSO)|PS OrthoTile DN(PSO_DN)|PS OrthoTile Visual(PSO_V)|PS4Band Analytic(PS4B)|PS4Band DN(PS4B_DN)|PS4Band SR(PS4B_SR)|PS3Band Analytic(PS3B)|PS3Band DN(PS3B_DN)|PS3Band Visual(PS3B_V)|RE OrthoTile (REO)|RE OrthoTile Visual(REO_V)')
    optional_named = parser_upload.add_argument_group('Optional named arguments')
    optional_named.add_argument('--large', action='store_true', help='(Advanced) Use multipart upload. Might help if upload of large '
                                                                     'files is failing on some systems. Might cause other issues.')
    optional_named.add_argument('--nodata', type=int, help='The value to burn into the raster as NoData (missing data)')

    required_named.add_argument('-u', '--user', help='Google account name (gmail address).')
    optional_named.add_argument('-s', '--service-account', help='Google Earth Engine service account.')
    optional_named.add_argument('-k', '--private-key', help='Google Earth Engine private key file.')
    optional_named.add_argument('-b', '--bucket', help='Google Cloud Storage bucket name.')
    parser_upload.set_defaults(func=upload_from_parser)

    parser_lst = subparsers.add_parser('lst',help='List assets in a folder/collection or write as text file')
    required_named = parser_lst.add_argument_group('Required named arguments.')
    required_named.add_argument('--location', help='This it the location of your folder/collection', required=True)
    required_named.add_argument('--typ', help='Whether you want the list to be printed or output as text[print/report]', required=True)
    optional_named = parser_lst.add_argument_group('Optional named arguments')
    optional_named.add_argument('--items', help="Number of items to list")
    optional_named.add_argument('--output',help="Folder location for report to be exported")
    parser_lst.set_defaults(func=lst_from_parser)

    parser_ee_report = subparsers.add_parser('ee_report',help='Prints a detailed report of all Earth Engine Assets includes Asset Type, Path,Number of Assets,size(MB),unit,owner,readers,writers')
    parser_ee_report.add_argument('--outfile', help='This it the location of your report csv file ', required=True)
    parser_ee_report.set_defaults(func=ee_report_from_parser)

    parser_assetsize = subparsers.add_parser('assetsize',help='Prints collection size in Human Readable form & Number of assets')
    parser_assetsize.add_argument('--asset', help='Earth Engine Asset for which to get size properties', required=True)
    parser_assetsize.set_defaults(func=assetsize_from_parser)

    parser_tasks=subparsers.add_parser('tasks',help='Queries current task status [completed,running,ready,failed,cancelled]')
    parser_tasks.set_defaults(func=tasks_from_parser)

    parser_genreport=subparsers.add_parser('taskreport',help='Create a report of all tasks and exports to a CSV file')
    parser_genreport.add_argument('--r',help='Path to csv report file')
    parser_genreport.set_defaults(func=genreport_from_parser)


    parser_delete = subparsers.add_parser('delete', help='Deletes collection and all items inside. Supports Unix-like wildcards.')
    parser_delete.add_argument('id', help='Full path to asset for deletion. Recursively removes all folders, collections and images.')
    parser_delete.set_defaults(func=delete_collection_from_parser)

    parser_mover=subparsers.add_parser('mover',help='Moves all assets from one collection to another')
    parser_mover.add_argument('--assetpath',help='Existing path of assets')
    parser_mover.add_argument('--finalpath',help='New path for assets')
    parser_mover.set_defaults(func=mover_from_parser)

    parser_copy=subparsers.add_parser('copy',help='Copies all assets from one collection to another: Including copying from other users if you have read permission to their assets')
    parser_copy.add_argument('--initial',help='Existing path of assets')
    parser_copy.add_argument('--final',help='New path for assets')
    parser_copy.set_defaults(func=copy_from_parser)

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
