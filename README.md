# Planet GEE Pipeline CLI

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1194323.svg)](https://doi.org/10.5281/zenodo.1194323)
[![JetStream](https://img.shields.io/badge/SupportedBy%3A-JetStream-brightgreen.svg)](https://jetstream-cloud.org/)
[![Planet](https://img.shields.io/badge/SupportedBy%3A-Planet%20Ambassador%20Program-brightgreen.svg)](https://www.planet.com/products/education-and-research/)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/samapriya)

This tool is designed to facilitate moving data from Planet's API into Google Earth Engine and using a metadata library. The tool downloads data into a local storage and allows you to process the metadata before uploading into Google Earth Engine. This tool has been updated to account for metadata property type by going through each metadata column and then uses the **upload manifest** function to upload images for ingestion to EE. This tool also draws from an additional tool I created with is the [Google Earth Engine Assest Manager Addon](https://github.com/samapriya/gee_asset_manager_addon) This includes the batch upload feature, but now additional tools such as generating reports of Earth Engine assets and quering quota to name just a few. The ambition is apart from helping users with batch actions on assets along with interacting and extending capabilities of existing GEE CLI. It is developed case by case basis to include more features in the future as it becomes available or as need arises. I have now relesed this as a [PyPI package](https://pypi.org/project/ppipe/) for easy installation and this will be updated along with the github package. 

![CLI](https://i.imgur.com/qTBnQOk.gif)

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [Usage examples](#usage-examples)
* [Planet Tools](#planet-tools)
	* [Planet Key](#planet-key)
    	* [AOI JSON](#aoi-json)
		* [IDlist](#idlist)
    	* [Activate or Check Asset](#activate-or-check-asset)
    	* [Check Total size of assets](#check-total-size-of-assets)
    	* [Download Asset](#download-asset)
		* [Download Saved Searches](#download-saved-searches)
    	* [Metadata Parser](#metadata-parser)
* [Earth Engine Tools](#earth-engine-tools)
	* [EE User](#ee-user)
	* [EE Quota](#ee-quota)
	* [Create](#create)
	* [Batch uploader](#batch-uploader)
	* [Asset List](#asset-list)
	* [Asset Size](#asset-size)
	* [Earth Engine Asset Report](#earth-engine-asset-report)
	* [Task Query](#task-query)
	* [Task Report](#task-report)
	* [Delete a collection with content](#delete-a-collection-with-content)
	* [Assets Move](#assets-move)
	* [Assets Copy](#assets-copy)
	* [Assets Access](#assets-access)
	* [Set Collection Property](#set-collection-property)
	* [Cancel all tasks](#cancel-all-tasks)
* [Credits](#credits)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

If you get no errors and you have python 2.7.14 or higher you should be good to go. Please note that I have released this as a python 2.7 but can be easily modified for python 3.

**This toolbox also uses some functionality from GDAL**
For installing GDAL in Ubuntu
```
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get install gdal-bin
sudo apt-get install python-gdal
```
For Windows I found this [guide](https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows) from UCLA

To install **Planet-GEE-Pipeline-CLI:**
You can install using two methods

```pip install ppipe```

or you can also try 

```
git clone https://github.com/samapriya/Planet-GEE-Pipeline-CLI.git
cd Planet-GEE-Pipeline-CLI
python setup.py install
```
For linux use sudo. This release also contains a windows installer which bypasses the need for you to have admin permission, it does however require you to have python in the system path meaning when you open up command prompt you should be able to type python and start it within the command prompt window. Post installation using the installer you can just call ppipe using the command prompt similar to calling python. Give it a go post installation type

```
ppipe -h
```

Installation is an optional step; the application can be also run directly by executing ppipe.py script. The advantage of having it installed is being able to execute ppipe as any command line tool. I recommend installation within virtual environment. If you don't want to install, browse into the ppipe folder and try ```python ppipe.py``` to get to the same result.

## Getting started

As usual, to print help:
```
usage: ppipe [-h]
             {
             ,planetkey,aoijson,idlist,activatepl,space,downloadpl,metadata,ee_user,quota,create,upload,lst,ee_report,assetsize,tasks,taskreport,delete,mover,copy,access,collprop,cancel}
             ...

Planet Pipeline with Google Earth Engine Batch Addons

positional arguments:
  { ,planetkey,aoijson,idlist,activatepl,space,downloadpl,metadata,ee_user,quota,create,upload,lst,ee_report,assetsize,tasks,taskreport,delete,mover,copy,access,collprop,cancel}
                        ---------------------------------------
                        -----Choose from Planet Tools Below-----
                        ---------------------------------------
    planetkey           Enter your planet API Key
    aoijson             Tool to convert KML, Shapefile,WKT,GeoJSON or Landsat
                        WRS PathRow file to AreaOfInterest.JSON file with
                        structured query for use with Planet API 1.0
    idlist              Creates an IDLIST that intersects AOI JSON
    activatepl          Tool to activate Planet Assets
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
    quota               Print Earth Engine total quota and used quota
    create              Allows the user to create an asset collection or
                        folder in Google Earth Engine
    upload              Batch Asset Uploader.
    lst                 List assets in a folder/collection or write as text
                        file
    ee_report           Prints a detailed report of all Earth Engine Assets
                        includes Asset Type, Path,Number of
                        Assets,size(MB),unit,owner,readers,writers
    assetsize           Prints collection size in Human Readable form & Number
                        of assets
    tasks               Queries current task status
                        [completed,running,ready,failed,cancelled]
    taskreport          Create a report of all tasks and exports to a CSV file
    delete              Deletes collection and all items inside. Supports
                        Unix-like wildcards.
    mover               Moves all assets from one collection to another
    copy                Copies all assets from one collection to another:
                        Including copying from other users if you have read
                        permission to their assets
    access              Sets Permissions for Images, Collection or all assets
                        in EE Folder Example: python ee_permissions.py --mode
                        "folder" --asset "users/john/doe" --user
                        "jimmy@doe.com:R"
    collprop            Sets Overall Properties for Image Collection
    cancel              Cancel all running tasks

optional arguments:
  -h, --help            show this help message and exit
```

To obtain help for a specific functionality, simply call it with _help_ switch, e.g.: `ppipe upload -h`. If you didn't install ppipe, then you can run it just by going to _ppipe_ directory and running `python ppipe.py [arguments go here]`

## Usage examples
Usage examples have been segmented into two parts focusing on both planet tools as well as earth engine tools, earth engine tools include additional developments in CLI which allows you to recursively interact with their python API

## Planet Tools
The Planet Toolsets consists of tools required to access control and download planet labs assets (PlanetScope and RapidEye OrthoTiles) as well as parse metadata in a tabular form which maybe required by other applications.

### Planet Key
This tool basically asks you to input your Planet API Key using a password prompt this is then used for all subsequent tools. This tool now includes an option for a quiet authentication using the API key incase it is unable to invoke an interactive environment such as in Google colaboratory.

```
usage: ppipe planetkey [-h] [--type TYPE] [--key KEY]

optional arguments:
  -h, --help   show this help message and exit

Optional named arguments:
  --type TYPE  For direct key entry type --type quiet
  --key KEY    Your Planet API Key
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

### IDlist
It is not possible to call the tool on an idlist instead of using a JSON , this option is useful when you want when you want to use the same item ID with different asset types quickly. For example the item ID for PSScene4Band analytic and PSScene4Band analytic_sr is the same. This is a quicker way to parse different asset type and create an IDlist for activation and download.
```
usage: ppipe idlist [-h] [--aoi AOI] [--item ITEM] [--asset ASSET]
                    [--number NUMBER]

optional arguments:
  -h, --help       show this help message and exit
  --aoi AOI        Choose aoi.json file created earlier
  --item ITEM      choose between Planet Item types
                   PSOrthoTile|PSScene4Band|PSScene3Band|REOrthoTile
  --asset ASSET    Choose between Planet asset types
                   analytic|analytic_dn|visual
  --number NUMBER  Maximum number of assets for the idlist
```

### Activate or Check Asset
The activatepl tab allows the users to either check or activate planet assets, in this case only PSOrthoTile and REOrthoTile are supported because I was only interested in these two asset types for my work but can be easily extended to other asset types. This tool makes use of an existing json file sturctured for use within Planet API or the aoi.json file created earlier
```
usage: ppipe activatepl [-h] [--asset ASSET] [--aoi AOI]

optional arguments:
  -h, --help     show this help message and exit
  --asset ASSET  Choose between planet asset types (PSOrthoTile
                 analytic/PSOrthoTile analytic_dn/PSOrthoTile
                 visual/PSScene4Band analytic/PSScene4Band
                 analytic_dn/PSScene3Band analytic/PSScene3Band
                 analytic_dn/PSScene3Band visual/REOrthoTile
                 analytic/REOrthoTile visual

Optional named arguments:
  --aoi AOI      Choose aoi.json file created earlier
```

### Check Total size of assets
It is important to sometimes estimate the overall size of download before you can actually download activated assets. This tool allows you to estimate local storage available at any location and overall size of download in MB or GB. This tool makes use of an existing url get request to look at content size and estimate overall download size of download for the activated assets.
```
usage: ppipe space [-h] [--aoi AOI] [--local LOCAL] [--asset ASSET]

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
The downloadpl tab allows the users to download assets. The platform can download Asset or Asset_XML which is the metadata file to desired folders.One again I was only interested in these two asset types(PSOrthoTile and REOrthoTile) for my work but can be easily extended to other asset types. If you don't provide an aoi.json file created earlier, the command uses the idlist created.
```
usage: ppipe downloadpl [-h] [--asset ASSET] [--local LOCAL] [--aoi AOI]

optional arguments:
  -h, --help     show this help message and exit
  --asset ASSET  Choose between planet asset types or for Metadata follow by
                 _xml Eg: PSOrthoTile analytic_xml--->Assets
                 Include:(PSOrthoTile analytic/PSOrthoTile
                 analytic_dn/PSOrthoTile visual/PSScene4Band
                 analytic/PSScene4Band analytic_dn/PSScene3Band
                 analytic/PSScene3Band analytic_dn/PSScene3Band
                 visual/REOrthoTile analytic/REOrthoTile visual
  --local LOCAL  Local Pathways where PlanetAssets are saved exampled
                 ./PlanetScope ./RapidEye

Optional named arguments:
  --aoi AOI      Choose aoi.json file created earlier
```
### Download Saved Searches
Download assets from saved searches which are saved in your planet explorer. 

```
usage: ppipe savedsearch [-h] [--name NAME] [--asset ASSET] [--local LOCAL]
                         [--limit LIMIT]

optional arguments:
  -h, --help     show this help message and exit
  --name NAME    Name of your saved search(It is case sensitive)
  --asset ASSET  Choose asset type analytic, analytic_xml, analytic_sr,
                 analytic_dn etc
  --local LOCAL  Local Path (full path address) where PlanetAssets are saved

Optional named arguments:
  --limit LIMIT  Choose number of assets you want to download
  ```

### Metadata Parser
The metadata tab is a more powerful tool and consists of metadata parsing for All PlanetScope and RapiEye Assets along with Digital Globe MultiSpectral and DigitalGlobe PanChromatic datasets. This was developed as a standalone to process xml metadata files from multiple sources and is important step is the user plans to upload these assets to Google Earth Engine.

```
usage: ppipe metadata [-h] [--asset ASSET] [--mf MF] [--mfile MFILE]
                      [--errorlog ERRORLOG] [--dir DIR]

optional arguments:
  -h, --help           show this help message and exit
  --asset ASSET        Choose PS OrthoTile(PSO)|PS OrthoTile DN(PSO_DN)|PS
                       OrthoTile Visual(PSO_V)|PS4Band Analytic(PS4B)|PS4Band
                       DN(PS4B_DN)|PS4Band SR(PS4B_SR)|PS3Band
                       Analytic(PS3B)|PS3Band DN(PS3B_DN)|PS3Band
                       Visual(PS3B_V)|RE OrthoTile (REO)|RE OrthoTile
                       Visual(REO_V)|DigitalGlobe
                       MultiSpectral(DGMS)|DigitalGlobe
                       Panchromatic(DGP)|PolarGeospatial CenterDEM
                       Strip(PGCDEM)?
  --mf MF              Metadata folder?
  --mfile MFILE        Metadata filename to be exported along with Path.csv
  --errorlog ERRORLOG  Errorlog to be exported along with Path.csv

Optional named arguments:
  --dir DIR            Path to Image Directory to be used to get ImageTags
                       with metadata. use only with PS4B_SR
```

## Earth Engine Tools
The ambition is apart from helping user with batch actions on assets along with interacting and extending capabilities of existing GEE CLI. It is developed case by case basis to include more features in the future as it becomes available or as need arises. This is also a seperate package for earth engine users to use and can be downloaded [here](https://github.com/samapriya/gee_asset_manager_addon)

### EE User
This tool is designed to allow different users to change earth engine authentication credentials. The tool invokes the authentication call and copies the authentication key verification website to the clipboard which can then be pasted onto a browser and the generated key can be pasted back. This command takes in no arguments.

```ppipe ee_user```
### EE Quota
This tool prints earthengine quota tools, used and remaining quota. No argument is required

```ppipe quota```

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

### Batch uploader
The script creates an Image Collection from GeoTIFFs in your local directory. By default, the collection name is the same as the local
directory name; with optional parameter you can provide a different name. You have to process the metadata for images, which is covered in the next section along with a manifest type for Planet image and asset:
[Metadata parser](#metadata-parser).

```
usage: ppipe upload [-h] --source SOURCE --dest DEST [-m METADATA]
                    [-mf MANIFEST] [--large] [--nodata NODATA] [-u USER]
                    [-s SERVICE_ACCOUNT] [-k PRIVATE_KEY] [-b BUCKET]

optional arguments:
  -h, --help            show this help message and exit

Required named arguments.:
  --source SOURCE       Path to the directory with images for upload.
  --dest DEST           Destination. Full path for upload to Google Earth
                        Engine, e.g. users/pinkiepie/myponycollection
  -m METADATA, --metadata METADATA
                        Path to CSV with metadata.
  -mf MANIFEST, --manifest MANIFEST
                        Manifest type to be used,Choose PS OrthoTile(PSO)|PS
                        OrthoTile DN(PSO_DN)|PS OrthoTile
                        Visual(PSO_V)|PS4Band Analytic(PS4B)|PS4Band
                        DN(PS4B_DN)|PS4Band SR(PS4B_SR)|PS3Band
                        Analytic(PS3B)|PS3Band DN(PS3B_DN)|PS3Band
                        Visual(PS3B_V)|RE OrthoTile (REO)|RE OrthoTile
                        Visual(REO_V)
  -u USER, --user USER  Google account name (gmail address).

Optional named arguments:
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

### Asset List
This tool is designed to either print or output asset lists within folders or collections using earthengine ls tool functions.
```
usage: ppipe lst [-h] --location LOCATION --typ TYP [--items ITEMS]
                 [--output OUTPUT]

optional arguments:
  -h, --help           show this help message and exit

Required named arguments.:
  --location LOCATION  This it the location of your folder/collection
  --typ TYP            Whether you want the list to be printed or output as
                       text[print/report]

Optional named arguments:
  --items ITEMS        Number of items to list
  --output OUTPUT      Folder location for report to be exported
```

### Asset Size
This tool allows you to query the size of any Earth Engine asset[Images, Image Collections, Tables and Folders] and prints out the number of assets and total asset size in non-byte encoding meaning KB, MB, GB, TB depending on size.

```
usage: ppipe assetsize [-h] --asset ASSET

optional arguments:
  -h, --help     show this help message and exit
  --asset ASSET  Earth Engine Asset for which to get size properties
```

### Earth Engine Asset Report
This tool recursively goes through all your assets(Includes Images, ImageCollection,Table,) and generates a report containing the following fields
[Type,Asset Type, Path,Number of Assets,size(MB),unit,owner,readers,writers].

```
usage: ppipe ee_report [-h] --outfile OUTFILE

optional arguments:
  -h, --help         show this help message and exit
  --outfile OUTFILE  This it the location of your report csv file
```
A simple setup is the following
``` ppipe ee_report --outfile "C:\johndoe\report.csv"```

### Task Query
This script counts all currently running,ready,completed,failed and cancelled tasks along with failed tasks. This is linked to the account you initialized with your google earth engine account. This takes no argument.
```
usage: geeadd.py tasks [-h]

optional arguments:
  -h, --help  show this help message and exit

geeadd.py tasks
```

### Task Report
Sometimes it is important to generate a report based on all tasks that is running or has finished. Generated report includes taskId, data time, task status and type
```
usage: ppipe taskreport [-h] [--r R]

optional arguments:
  -h, --help  show this help message and exit
  --r R       Folder Path where the reports will be saved
```

### Delete a collection with content

The delete is recursive, meaning it will delete also all children assets: images, collections and folders. Use with caution!
```
usage: ppipe delete [-h] id

positional arguments:
  id          Full path to asset for deletion. Recursively removes all
              folders, collections and images.

optional arguments:
  -h, --help  show this help message and exit
```

Typical usage would be 
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

### Assets Move
This script allows us to recursively move assets from one collection to the other.
```
usage: ppipe mover [-h] [--assetpath ASSETPATH] [--finalpath FINALPATH]

optional arguments:
  -h, --help            show this help message and exit
  --assetpath ASSETPATH
                        Existing path of assets
  --finalpath FINALPATH
                        New path for assets
ppipe mover --assetpath "users/johndoe/myfolder/myponycollection" --destination "users/johndoe/myfolder/myotherponycollection"
```

### Assets Copy
This script allows us to recursively copy assets from one collection to the other. If you have read acess to assets from another user this will also allow you to copy assets from their collections.
```
usage: ppipe copy [-h] [--initial INITIAL] [--final FINAL]

optional arguments:
  -h, --help         show this help message and exit
  --initial INITIAL  Existing path of assets
  --final FINAL      New path for assets
ppipe mover --initial "users/johndoe/myfolder/myponycollection" --final "users/johndoe/myfolder/myotherponycollection"
```

### Assets Access
This tool allows you to set asset acess for either folder , collection or image recursively meaning you can add collection access properties for multiple assets at the same time.
```
usage: geeadd access [-h] --mode MODE --asset ASSET --user USER

optional arguments:
  -h, --help     show this help message and exit
  --mode MODE    This lets you select if you want to change permission or
                 folder/collection/image
  --asset ASSET  This is the path to the earth engine asset whose permission
                 you are changing folder/collection/image
  --user USER    This is the email address to whom you want to give read or
                 write permission Usage: "john@doe.com:R" or "john@doe.com:W"
                 R/W refers to read or write permission
geeadd.py access --mode folder --asset "folder/collection/image" --user "john@doe.com:R"
```

### Set Collection Property
This script is derived from the ee tool to set collection properties and will set overall properties for collection.
```
usage: ppipe collprop [-h] [--coll COLL] [--p P]

optional arguments:
  -h, --help   show this help message and exit
  --coll COLL  Path of Image Collection
  --p P        "system:description=Description"/"system:provider_url=url"/"sys
               tem:tags=tags"/"system:title=title
```

### Cancel all tasks
This is a simpler tool, can be called directly from the earthengine cli as well
```
earthengine cli command
earthengine task cancel all
```
Usage using this tool
```
usage: ppipe cancel [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### Credits
[JetStream](https://jetstream-cloud.org/) A portion of the work is suported by JetStream Grant TG-GEO160014.

Also supported by [Planet Labs Ambassador Program](https://www.planet.com/markets/ambassador-signup/)

Original upload function adapted from [Lukasz's asset manager tool](https://github.com/tracek/gee_asset_manager)


# Changelog

### v0.3.7

- Now allows users to download from saved searches in planet explorer

### v0.3.6

- Now handles complex geometry by using a bounding box for GeoJSON files

### v0.3.5

- Fixed issues with space function
- Improved file size parsing

### v0.3.2

- Generalized CLI arguments
- Fixed subprocess shell issue for upload

### v0.3.0

- Allows for quiet authentication for use in Google Colab or non interactive environments
- Improved planet key entry and authentication protocols

### v0.2.91

- Fixed issue with Surface Reflectance metadata and manifest lib
- Improved ingestion support for (PSScene4Band analytic_Sr)[PS4B_SR]

### v0.2.9

- Fixed issues with generating id list
- Improved overall security of command calls

### v0.2.2

- Major improvements to ingestion using manifest ingest in Google Earth Engine
- Contains manifest for all commonly used Planet Data item and asset combinations
- Added additional tool to Earth Engine Enhancement including quota check before upload to GEE

### v0.2.1
- Fixed initialization loop issue

### v0.2.0
- Metadata parser and Uploader Can now handle PlanetScope 4 Band Surface Reflectance Datasets
- General Improvements

### v0.1.9
- Changes made to reflect updated GEE Addon tools
- general improvements

### v0.1.8
- Minor fixes to parser and general improvements
- Planet Key is now stored in a configuration folder which is safer "C:\users\.config\planet"
- Earth Engine now requires you to assign a field type for metadata meaning an alphanumeric column like satID cannot also have numeric values unless specified explicitly . Manifest option has been added to handle this (just use -mf "planetscope")
- Added capability to query download size and local disk capacity before downloading planet assets.
- Added the list function to generate list of collections or folders including reports
- Added the collection size tool which allows you to estimate total size or quota used from your allocated quota.
- ogr2ft feature is removed since Earth Engine now allows vector and table uploading.
