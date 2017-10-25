# Planet GEE Pipeline CLI

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.998025.svg)](https://doi.org/10.5281/zenodo.998025)
[![JetStream](https://img.shields.io/badge/SupportedBy%3A-JetStream-brightgreen.svg)](https://jetstream-cloud.org/)
[![Planet](https://img.shields.io/badge/SupportedBy%3A-Planet%20Ambassador%20Program-brightgreen.svg)](https://www.planet.com/products/education-and-research/)

While moving between assets from Planet Inc and Google Earth Engine it was imperative to create a pipeline that allows for easy transitions between the two service end points and this tool is designed to act as a step by step process chain from Planet Assets to batch upload and modification within the Google Earth Engine environment. The ambition is apart from helping user with batch actions on assets along with interacting and extending capabilities of existing GEE CLI. It is developed case by case basis to include more features in the future as it becomes available or as need arises. tab.

![CLI](https://i.imgur.com/1H4IlW9.gif)

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
    * [Batch uploader](#batch-uploader)
    * [Parsing metadata](#parsing-metadata)
* [Usage examples](#usage-examples)
* [Planet Tools](#planet-tools)
	* [Planet Key](#planet-key)
    * [AOI JSON](#aoi-json)
    * [Activate or Check Asset](#activate-or-check-asset)
	* [Check Total size of assets](#check-total-size-of-assets)
    * [Download Asset](#download-asset)
    * [Metadata Parser](#metadata-parser)
* [Earth Engine Tools](#earth-engine-tools)
	* [EE User](#ee-user)
	* [Create](#create)
    * [Upload a directory with images and associate properties with each image:](#upload-a-directory-with-images-and-associate-properties-with-each-image)
	* [Upload a directory with images with specific NoData value to a selected destination:](#upload-a-directory-with-images-with-specific-nodata-value-to-a-selected-destination)
	* [List all assets](#list-all-assets)
	* [Collection size](#collection-size)
	* [Delete a collection with content:](#delete-a-collection-with-content)
	* [Task Query](#task-query)
	* [Task Query during ingestion](#task-query-during-ingestion)
	* [Task Report](#task-report)
	* [Cancel all tasks](#cancel-all-tasks)
	* [Assets Move](#assets-move)
	* [Assets Copy](#assets-copy)
	* [Assets Access](#assets-access)
	* [Set Collection Property](#set-collection-property)
	* [Cleanup Utility](#cleanup-utility)
* [Credits](#credits)

## Installation
We assume Earth Engine Python API is installed and EE authorised as desribed [here](https://developers.google.com/earth-engine/python_install). We also assume Planet Python API is installed you can install by simply running.
```
pip install planet
```
Further instructions can be found [here](https://www.planet.com/docs/api-quickstart-examples/cli/) 

**This toolbox also uses some functionality from GDAL**
For installing GDAL in Ubuntu
```
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get install gdal-bin
```
For Windows I found this [guide](https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows) from UCLA

To install **Planet-GEE-Pipeline-CLI:**
```
git clone https://github.com/samapriya/Planet-GEE-Pipeline-CLI.git
cd Planet-GEE-Pipeline-CLI && pip install .
```
This release also contains a windows installer which bypasses the need for you to have admin permission, it does however require you to have python in the system path meaning when you open up command prompt you should be able to type python and start it within the command prompt window. Post installation using the installer you can just call ppipe using the command prompt similar to calling python. Give it a go post installation type
```
ppipe -h
```
Installation is an optional step; the application can be also run directly by executing ppipe.py script. The advantage of having it installed is being able to execute ppipe as any command line tool. I recommend installation within virtual environment. To install run
```
python setup.py develop or python setup.py install

In a linux distribution
sudo python setup.py develop or sudo python setup.py install
```

## Getting started

As usual, to print help:
```
usage: ppipe.py [-h]
                {
                ,planetkey,aoijson,activatepl,space,downloadpl,metadata,ee_user,create,upload,lst,collsize,delete,tasks,taskquery,report,cancel,mover,copy,access,collprop,cleanout}
                ...

Planet Pipeline with Google Earth Engine Batch Addons

positional arguments:
  { ,planetkey,aoijson,activatepl,space,downloadpl,metadata,ee_user,create,upload,lst,collsize,delete,tasks,taskquery,report,cancel,mover,copy,access,collprop,cleanout}
                        ---------------------------------------
                        -----Choose from Planet Tools Below-----
                        ---------------------------------------
    planetkey           Enter your planet API Key
    aoijson             Tool to convert KML, Shapefile,WKT,GeoJSON or Landsat
                        WRS PathRow file to AreaOfInterest.JSON file with
                        structured query for use with Planet API 1.0
    activatepl          Tool to query and/or activate Planet Assets
    space               Tool to query total download size of activated assets
                        & local space left for download
    downloadpl          Tool to download Planet Assets
    metadata            Tool to tabulate and convert all metadata files from
                        Planet or Digital Globe Assets
                        -------------------------------------------
                        ----Choose from Earth Engine Tools Below----
                        -------------------------------------------
    ee_user             Get Earth Engine API Key & Paste it back to Command
                        line/shell to change user
    create              Allows the user to create an asset collection or
                        folder in Google Earth Engine
    upload              Batch Asset Uploader.
    lst                 List assets in a folder/collection or write as text
                        file
    collsize            Collects collection size in Human Readable form &
                        Number of assets
    delete              Deletes collection and all items inside. Supports
                        Unix-like wildcards.
    tasks               Queries currently running, enqued,failed
    taskquery           Queries currently running, enqued,failed ingestions
                        and uploaded assets
    report              Create a report of all tasks and exports to a CSV file
    cancel              Cancel all running tasks
    mover               Moves all assets from one collection to another
    copy                Copies all assets from one collection to another:
                        Including copying from other users if you have read
                        permission to their assets
    access              Sets Permissions for Images, Collection or all assets
                        in EE Folder Example: python ee_permissions.py --mode
                        "folder" --asset "users/john/doe" --user
                        "jimmy@doe.com:R"
    collprop            Sets Overall Properties for Image Collection
    cleanout            Clear folders with datasets from earlier downloaded

optional arguments:
  -h, --help            show this help message and exit
```

To obtain help for a specific functionality, simply call it with _help_
switch, e.g.: `ppipe upload -h`. If you didn't install ppipe, then you
can run it just by going to _ppipe_ directory and running `python
ppipe.py [arguments go here]`

## Batch uploader
The script creates an Image Collection from GeoTIFFs in your local
directory. By default, the collection name is the same as the local
directory name; with optional parameter you can provide a different
name. Another optional parameter is a path to a CSV file with metadata
for images, which is covered in the next section:
[Parsing metadata](#parsing-metadata).



```
usage: ppipe.py upload [-h] --source SOURCE --dest DEST [-m METADATA]
                       [-mf MANIFEST] [--large] [--nodata NODATA] [-u USER]
                       [-s SERVICE_ACCOUNT] [-k PRIVATE_KEY] [-b BUCKET]

optional arguments:
  -h, --help            show this help message and exit

Required named arguments.:
  --source SOURCE       Path to the directory with images for upload.
  --dest DEST           Destination. Full path for upload to Google Earth
                        Engine, e.g. users/pinkiepie/myponycollection
  -u USER, --user USER  Google account name (gmail address).

Optional named arguments:
  -m METADATA, --metadata METADATA
                        Path to CSV with metadata.
  -mf MANIFEST, --manifest MANIFEST
                        Manifest type to be used,for planetscope use
                        "planetscope"
  --large               (Advanced) Use multipart upload. Might help if upload
                        of large files is failing on some systems. Might cause
                        other issues.
  --nodata NODATA       The value to burn into the raster as NoData (missing
                        data)
  -s SERVICE_ACCOUNT, --service-account SERVICE_ACCOUNT
                        Google Earth Engine service account.
  -k PRIVATE_KEY, --private-key PRIVATE_KEY
                        Google Earth Engine private key file.
  -b BUCKET, --bucket BUCKET
                        Google Cloud Storage bucket name.
```

### Parsing metadata
By metadata we understand here the properties associated with each image. Thanks to these, GEE user can easily filter collection based on specified criteria. The file with metadata should be organised as follows:

| filename (without extension) | property1 header | property2 header |
|------------------------------|------------------|------------------|
| file1                        | value1           | value2           |
| file2                        | value3           | value4           |

Note that header can contain only letters, digits and underscores. 

Example:

| id_no     | class      | category | binomial             |system:time_start|
|-----------|------------|----------|----------------------|-----------------|
| my_file_1 | GASTROPODA | EN       | Aaadonta constricta  |1478943081000    |
| my_file_2 | GASTROPODA | CR       | Aaadonta irregularis |1478943081000    |

The corresponding files are my_file_1.tif and my_file_2.tif. With each of the files five properties are associated: id_no, class, category, binomial and system:time_start. The latter is time in Unix epoch format, in milliseconds, as documented in GEE glosary. The program will match the file names from the upload directory with ones provided in the CSV and pass the metadata in JSON format:

```
{ id_no: my_file_1, class: GASTROPODA, category: EN, binomial: Aaadonta constricta, system:time_start: 1478943081000}
```

The program will report any illegal fields, it will also complain if not all of the images passed for upload have metadata associated. User can opt to ignore it, in which case some assets will have no properties.

Having metadata helps in organising your asstets, but is not mandatory - you can skip it.


## Usage examples
Usage examples have been segmented into two parts focusing on both planet tools as well as earth engine tools, earth engine tools include additional developments in CLI which allows you to recursively interact with their python API

## Planet Tools
The Planet Toolsets consists of tools required to access control and download planet labs assets (PlanetScope and RapidEye OrthoTiles) as well as parse metadata in a tabular form which maybe required by other applications.

### Planet Key
This tool basically asks you to input your Planet API Key using a password prompt this is then used for all subsequent tools
```
usage: ppipe.py planetkey [-h]

optional arguments:
  -h, --help  show this help message and exit
```

If using on a private machine the Key is saved as a csv file for all future runs of the tool.
 
### AOI JSON
The aoijson tab within the toolset allows you to create filters and structure your existing input file to that which can be used with Planet's API. The tool requires inputs with start and end date, along with cloud cover. You can choose from multiple input files types such as KML, Zipped Shapefile, GeoJSON, WKT or even Landsat Tiles based on PathRow numbers. The geo option asks you to select existing files which will be converted into formatted JSON file called aoi.json. If using WRS as an option just type in the 6 digit PathRow combination and it will create a json file for you.
```
usage: ppipe.py aoijson [-h] [--start START] [--end END] [--cloud CLOUD]
                     [--inputfile INPUTFILE] [--geo GEO] [--loc LOC]

optional arguments:
  -h, --help            show this help message and exit
  --start START         Start date in YYYY-MM-DD?
  --end END             End date in YYYY-MM-DD?
  --cloud CLOUD         Maximum Cloud Cover(0-1) representing 0-100
  --inputfile INPUTFILE
                        Choose a kml/shapefile/geojson or WKT file for
                        AOI(KML/SHP/GJSON/WKT) or WRS (6 digit RowPath
                        Example: 023042)
  --geo GEO             map.geojson/aoi.kml/aoi.shp/aoi.wkt file
  --loc LOC             Location where aoi.json file is to be stored
```

### Activate or Check Asset
The activatepl tab allows the users to either check or activate planet assets, in this case only PSOrthoTile and REOrthoTile are supported because I was only interested in these two asset types for my work but can be easily extended to other asset types. This tool makes use of an existing json file sturctured for use within Planet API or the aoi.json file created earlier
```
usage: ppipe.py activatepl [-h] [--aoi AOI] [--action ACTION] [--asst ASST]

optional arguments:
  -h, --help       show this help message and exit
  --aoi AOI        Choose aoi.json file created earlier
  --action ACTION  choose between check/activate
  --asst ASST      Choose between planet asset types (PSOrthoTile
                   analytic/REOrthoTile analytic/PSOrthoTile
                   analytic_xml/REOrthoTile analytic_xml

```

### Check Total size of assets
It is important to sometimes estimate the overall size of download before you can actually download activated assets. This tool allows you to estimate local storage available at any location and overall size of download in MB or GB. This tool makes use of an existing url get request to look at content size and estimate overall download size of download for the activated assets.
```
usage: ppipe.py space [-h] [--aoi AOI] [--local LOCAL] [--asset ASSET]

optional arguments:
  -h, --help     show this help message and exit
  --aoi AOI      Choose aoi.json file created earlier
  --local LOCAL  local path where you are downloading assets
  --asset ASSET  Choose between planet asset types (PSOrthoTile
                 analytic/PSOrthoTile analytic_dn/PSOrthoTile
                 visual/PSScene4Band analytic/PSScene4Band
                 analytic_dn/PSScene3Band analytic/PSScene3Band
                 analytic_dn/PSScene3Band visual/REOrthoTile
                 analytic/REOrthoTile visual
```

### Download Asset
Having metadata helps in organising your asstets, but is not mandatory - you can skip it.
The downloadpl tab allows the users to download assets. The platform can download Asset or Asset_XML which is the metadata file to desired folders.One again I was only interested in these two asset types(PSOrthoTile and REOrthoTile) for my work but can be easily extended to other asset types.
```
usage: ppipe.py downloadpl [-h] [--aoi AOI] [--action ACTION] [--asst ASST]
                           [--pathway PATHWAY]

optional arguments:
  -h, --help         show this help message and exit
  --aoi AOI          Choose aoi.json file created earlier
  --action ACTION    choose download
  --asst ASST        Choose between planet asset types (PSOrthoTile
                     analytic/REOrthoTile analytic/PSOrthoTile
                     analytic_xml/REOrthoTile analytic_xml
  --pathway PATHWAY  Folder Pathways where PlanetAssets are saved exampled
                     ./PlanetScope ./RapidEye
```

### Metadata Parser
The metadata tab is a more powerful tool and consists of metadata parsing for All PlanetScope and RapiEye Assets along with Digital Globe MultiSpectral and DigitalGlobe PanChromatic datasets. This was developed as a standalone to process xml metadata files from multiple sources and is important step is the user plans to upload these assets to Google Earth Engine. 

```
usage: ppipe.py metadata [-h] [--asset ASSET] [--mf MF] [--mfile MFILE]
                      [--errorlog ERRORLOG]

optional arguments:
  -h, --help           show this help message and exit
  --asset ASSET        Choose PS OrthoTile(PSO)|PS OrthoTile DN(PSO_DN)|PS
                       OrthoTile Visual(PSO_V)|PS4Band Analytic(PS4B)|PS4Band
                       DN(PS4B_DN)|PS3Band Analytic(PS3B)|PS3Band
                       DN(PS3B_DN)|PS3Band Visual(PS3B_V)|RE OrthoTile
                       (REO)|RE OrthoTile Visual(REO_V)|DigitalGlobe
                       MultiSpectral(DGMS)|DigitalGlobe Panchromatic(DGP)?
  --mf MF              Metadata folder?
  --mfile MFILE        Metadata filename to be exported along with Path.csv
  --errorlog ERRORLOG  Errorlog to be exported along with Path.csv
```

## Earth Engine Tools
The ambition is apart from helping user with batch actions on assets along with interacting and extending capabilities of existing GEE CLI. It is developed case by case basis to include more features in the future as it becomes available or as need arises. This is also a seperate package for earth engine users to use and can be downloaded [here](https://github.com/samapriya/gee_asset_manager_addon)

### EE User
This tool is designed to allow different users to change earth engine authentication credentials. The tool invokes the authentication call and copies the authentication key verification website to the clipboard which can then be pasted onto a browser and the generated key can be pasted back

### Create
This tool allows you to create a collection or folder in your earth engine root directory. The tool uses the system cli to achieve this and this has been included so as to reduce the need to switch between multiple tools and CLI.
```
usage: ppipe.py create [-h] --typ TYP --path PATH

optional arguments:
  -h, --help   show this help message and exit
  --typ TYP    Specify type: collection or folder
  --path PATH  This is the path for the earth engine asset to be created full
               path is needsed eg: users/johndoe/collection
```			   

### Upload a directory with images to your myfolder/mycollection and associate properties with each image:
```
ppipe upload -u johndoe@gmail.com --source path_to_directory_with_tif -m path_to_metadata.csv -mf maifest_type(ex:planetscope) --dest users/johndoe/myfolder/myponycollection
```
The script will prompt the user for Google account password. The program will also check that all properties in path_to_metadata.csv do not contain any illegal characters for GEE. Don't need metadata? Simply skip this option.You can also skip manifest for RapidEye imagery or any other source that does not require metadata field type handling.

### Upload a directory with images with specific NoData value to a selected destination 
```
ppipe upload -u johndoe@gmail.com --source path_to_directory_with_tif --dest users/johndoe/myfolder/myponycollection --nodata 222
```
In this case we need to supply full path to the destination, which is helpful when we upload to a shared folder. In the provided example we also burn value 222 into all rasters for missing data (NoData).

### List all assets
This tool allows you to list assets and is a direct derivative of the Earth Engine tool including the ability to export the list of assets as a text file.
```
usage: ppipe.py lst [-h] --location LOCATION --type TYPE [--items ITEMS]
                    [--folder FOLDER]

optional arguments:
  -h, --help           show this help message and exit
  --location LOCATION  This it the location of your folder/collection
  --type TYPE          Whether you want the list to be printed or output as
                       text
  --items ITEMS        Number of items to list
  --folder FOLDER      Folder location for report to be exported
```

### Collection size
This tool allows you to iteratively calculate the size of an image collection or image in human readable format ,(MB/GB or TB). The system size is reflected and may not always match the space utilized on local drive. This is now part of the standard API but the standard API generates size in bytes.
```
usage: ppipe.py collsize [-h] --coll COLL

optional arguments:
  -h, --help   show this help message and exit
  --coll COLL  Earth Engine Collection for which to get size properties
```

### Task Query
This script counts all currently running and ready tasks along with failed tasks.
```
usage: ppipe.py tasks [-h]

optional arguments:
  -h, --help  show this help message and exit

ppipe.py tasks
```

### Task Query during ingestion
This script can be used intermittently to look at running, failed and ready(waiting) tasks during ingestion. This script is a special case using query tasks only when uploading assets to collection by providing collection pathway to see how collection size increases.
```
usage: ppipe.py taskquery [-h] [--destination DESTINATION]

optional arguments:
  -h, --help            show this help message and exit
  --destination DESTINATION
                        Full path to asset where you are uploading files

ppipe.py taskquery "users/johndoe/myfolder/myponycollection"						
```

### Task Report
Sometimes it is important to generate a report based on all tasks that is running or has finished. Generated report includes taskId, data time, task status and type
```
usage: ppipe.py report [-h] [--r R] [--e E]

optional arguments:
  -h, --help  show this help message and exit
  --r R       Path & CSV filename where the report will be saved
  --e E       Path & CSV filename where the errorlog will be saved

ppipe.py report --r "report.csv" --e "errorlog.csv"
```
### Delete a collection with content:

The delete is recursive, meaning it will delete also all children assets: images, collections and folders. Use with caution!
```
ppipe delete users/johndoe/test
```

Console output:
```
2016-07-17 16:14:09,212 :: oauth2client.client :: INFO :: Attempting refresh to obtain initial access_token
2016-07-17 16:14:09,213 :: oauth2client.client :: INFO :: Refreshing access_token
2016-07-17 16:14:10,842 :: root :: INFO :: Attempting to delete collection test
2016-07-17 16:14:16,898 :: root :: INFO :: Collection users/johndoe/test removed
```

### Delete all directories / collections based on a Unix-like pattern

```
ppipe delete users/johndoe/*weird[0-9]?name*
```

### Cancel all tasks
This is a simpler tool, can be called directly from the earthengine cli as well
```
earthengine cli command
earthengine task cancel all

usage: ppipe.py cancel [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### Assets Move
This script allows us to recursively move assets from one collection to the other.
```
usage: ppipe.py mover [-h] [--assetpath ASSETPATH] [--finalpath FINALPATH]

optional arguments:
  -h, --help            show this help message and exit
  --assetpath ASSETPATH
                        Existing path of assets
  --finalpath FINALPATH
                        New path for assets
ppipe.py mover --assetpath "users/johndoe/myfolder/myponycollection" --destination "users/johndoe/myfolder/myotherponycollection"					
```

### Assets Copy
This script allows us to recursively copy assets from one collection to the other. If you have read acess to assets from another user this will also allow you to copy assets from their collections.
```
usage: ppipe.py copy [-h] [--initial INITIAL] [--final FINAL]

optional arguments:
  -h, --help         show this help message and exit
  --initial INITIAL  Existing path of assets
  --final FINAL      New path for assets
ppipe.py mover --initial "users/johndoe/myfolder/myponycollection" --final "users/johndoe/myfolder/myotherponycollection"					
```

### Assets Access
This tool allows you to set asset acess for either folder , collection or image recursively meaning you can add collection access properties for multiple assets at the same time.
```
usage: ppipe access [-h] --mode MODE --asset ASSET --user USER

optional arguments:
  -h, --help     show this help message and exit
  --mode MODE    This lets you select if you want to change permission or
                 folder/collection/image
  --asset ASSET  This is the path to the earth engine asset whose permission
                 you are changing folder/collection/image
  --user USER    This is the email address to whom you want to give read or
                 write permission Usage: "john@doe.com:R" or "john@doe.com:W"
                 R/W refers to read or write permission
ppipe.py access --mode folder --asset "folder/collection/image" --user "john@doe.com:R"
```

### Set Collection Property
This script is derived from the ee tool to set collection properties and will set overall properties for collection. 
```
usage: ppipe.py collprop [-h] [--coll COLL] [--p P]

optional arguments:
  -h, --help   show this help message and exit
  --coll COLL  Path of Image Collection
  --p P        "system:description=Description"/"system:provider_url=url"/"sys
               tem:tags=tags"/"system:title=title
```

### Cleanup Utility
This script is used to clean folders once all processes have been completed. In short this is a function to clear folder on local machine.
```
usage: ppipe.py cleanout [-h] [--dirpath DIRPATH]

optional arguments:
  -h, --help         show this help message and exit
  --dirpath DIRPATH  Folder you want to delete after all processes have been
                     completed
ppipe.py cleanout --dirpath "./folder"
```

### Credits
[JetStream](https://jetstream-cloud.org/) A portion of the work is suported by JetStream Grant TG-GEO160014.

Also supported by [Planet Labs Ambassador Program](https://www.planet.com/markets/ambassador-signup/)

Original upload function adapted from [Lukasz's asset manager tool](https://github.com/tracek/gee_asset_manager)


# Changelog

## [0.1.8] - 2017-09-27 Compiled using Google Earth Engine API 1.1.9
### Added & Removed
- Minor fixes to parser and general improvements
- Planet Key is now stored in a configuration folder which is safer "C:\users\.config\planet"
- Earth Engine now requires you to assign a field type for metadata meaning an alphanumeric column like satID cannot also have numeric values unless specified explicitly . Manifest option has been added to handle this (just use -mf "planetscope")
- Added capability to query download size and local disk capacity before downloading planet assets.
- Added the list function to generate list of collections or folders including reports
- Added the collection size tool which allows you to estimate total size or quota used from your allocated quota.
- ogr2ft feature is removed since Earth Engine now allows vector and table uploading.
