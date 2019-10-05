# Planet GEE Pipeline CLI

[![PyPI version](https://badge.fury.io/py/ppipe.svg)](https://badge.fury.io/py/ppipe)
![Build Status](https://img.shields.io/badge/dynamic/json.svg?label=downloads&url=https%3A%2F%2Fpypistats.org%2Fapi%2Fpackages%2Fppipe%2Frecent%3Fperiod%3Dmonth&query=%24.data.last_month&colorB=blue&suffix=%2fmonth)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1316886.svg)](https://doi.org/10.5281/zenodo.1316886)
[![Planet](https://img.shields.io/badge/SupportedBy%3A-Planet%20Ambassador%20Program-brightgreen.svg)](https://www.planet.com/markets/education-and-research/)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/samapriya)

This tool is designed to facilitate moving data from Planet's API into Google Earth Engine and using a metadata library. The tool downloads data into a local storage and allows you to process the metadata before uploading into Google Earth Engine. This tool has been updated to account for metadata property type by going through each metadata column and then uses the **upload manifest** function to upload images for ingestion to EE. This tool also draws from an additional tool I created with is the [Google Earth Engine Asset Manager Addon](https://github.com/samapriya/gee_asset_manager_addon) This includes the batch upload feature, but now additional tools such as generating reports of Earth Engine assets and querying quota to name just a few. The ambition is apart from helping users with batch actions on assets along with interacting and extending capabilities of existing GEE CLI. It is developed case by case basis to include more features in the future as it becomes available or as the need arises. I have now released this as a [PyPI package](https://pypi.org/project/ppipe/) for easy installation and this will be updated along with the the GitHub package.

Though this tool is designed to download planet imagery, use [porder](https://github.com/samapriya/porder) to use the new ordersv2 API to download planet imagery. This includes additional filter capabilities along with capability to clip and download.

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [Usage examples](#usage-examples)
* [Planet Tools](#planet-tools)
	* [Planet Key](#planet-key)
	* [Planet Quota](#planet-quota)
	* [Download Async](#download-async)
	* [Download Saved Searches](#download-saved-searches)
	* [Metadata Parser](#metadata-parser)
* [Earth Engine Tools](#earth-engine-tools)
    * [selenium update](#selenium-update)
    * [gee selsetup](#gee-selsetup)
	* [EE User](#ee-user)
	* [EE Quota](#ee-quota)
	* [Create](#create)
	* [Batch uploader](#batch-uploader)
	* [Asset List](#asset-list)
	* [Asset Size](#asset-size)
	* [Task Query](#task-query)
	* [Assets Access](#assets-access)
	* [Cancel all tasks](#cancel-all-tasks)
* [Credits](#credits)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

If you get no errors and you have python 2.7.14 or higher you should be good to go. Please note that I have released this as a python 2.7 but can be easily modified for python 3.

**Make sure you install OpenSSL from [this page](https://www.openssl.org/)**

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
> ppipe -h
usage: ppipe [-h]
             {
             ,planetkey,pquota,dasync,savedsearch,metadata,update,selsetup,ee_user,quota,create,selupload,lst,assetsize,tasks,access,ca
             ...

Planet Pipeline with Google Earth Engine Batch Addons

positional arguments:
  { ,planetkey,pquota,dasync,savedsearch,metadata,update,selsetup,ee_user,quota,create,selupload,lst,assetsize,tasks,access,cancel}
                        ---------------------------------------
                        -----Choose from Planet Tools Below-----
                        ---------------------------------------
    planetkey           Enter your planet API Key
    pquota              Prints your Planet Quota Details
    dasync              Uses the Planet Client Async Downloader to download
                        Planet Assets: Does not require activation
    savedsearch         Tool to download saved searches from Planet Explorer
    metadata            Tool to tabulate and convert all metadata files from
                        Planet or Digital Globe Assets
                        -------------------------------------------
                        ----Choose from Earth Engine Tools Below----
                        -------------------------------------------
    update              Updates Selenium drivers for firefox
    selsetup            Non headless setup for new google account, use if
                        upload throws errors
    ee_user             Get Earth Engine API Key & Paste it back to Command
                        line/shell to change user
    quota               Print Earth Engine total quota and used quota
    create              Allows the user to create an asset collection or
                        folder in Google Earth Engine
    selupload           Batch Asset Uploader for Planet Items & Assets using
                        Selenium
    lst                 List assets in a folder/collection or write as text
                        file
    assetsize           Prints collection size in Human Readable form & Number
                        of assets
    tasks               Queries current task status
                        [completed,running,ready,failed,cancelled]
    access              Sets Permissions for items in folder
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
This tool basically asks you to input your Planet API Key using a password prompt this is then used for all subsequent tools. This tool now includes an option for a quiet authentication using the API key incase it is unable to invoke an interactive environment such as in Google colaboratory. You can also perform ```planet init``` to set the key as the tool can read from it directly.

```
usage: ppipe planetkey [-h] [--type TYPE] [--key KEY]

optional arguments:
  -h, --help   show this help message and exit

Optional named arguments:
  --type TYPE  For direct key entry type --type quiet
  --key KEY    Your Planet API Key
```

If using on a private machine the Key is saved as a csv file for all future runs of the tool.

### Planet Quota
This tool prints your Planet quota including allocation name, Total quota, quota used and quota remaining. Calling it is simple

```
ppipe pquota
```

### Download Async
This tool is built as a wrapper around the Planet Client's own download tool. The tool included in the planet client is multithreaded and allows the user to activate, poll and download at the same time. This will allow you to pass geometry in terms of a geojson files or all filter like start and end date and time using the .json files you created using the ```aoijson``` tool earlier.

```
usage: ppipe dasync [-h] [--infile INFILE] [--item ITEM] [--asset ASSET]
                       [--local LOCAL] [--start START] [--end END]
                       [--cmin CMIN] [--cmax CMAX]

optional arguments:
  -h, --help       show this help message and exit
  --infile INFILE  Choose a geojson from geojson.io or the aoi-json you
                   created earlier using ppipe aoijson
  --item ITEM      Choose from Planet Item types Example: PSScene4Band,
                   PSOrthoTile, REOrthoTile etc
  --asset ASSET    Choose an asset type example: anlaytic,
                   analytic_dn,analytic_sr,analytic_xml etc
  --local LOCAL    Local Path where Planet Item and asset types are saved

Optional named arguments:
  --start START    Start date filter format YYYY-MM-DD
  --end END        End date filter format YYYY-MM-DD
  --cmin CMIN      Cloud cover minimum between 0-1
  --cmax CMAX      Cloud cover maximum between 0-1
```
A setup using geojson needs to include other filters too and a typical setup would be

```
ppipe dasync --infile "C:\Users\johndoe\geometry.geojson" --item "PSScene4Band" --asset "analytic" --local "C:\planet" --start "2018-06-01" --end "2018-08-01" --cmin 0 --cmax 0.4
```

Using a stuctured json file that you might have created earlier means you don't have to pass additional filters everytime

```
python ppipe.py dasync --infile "C:\Users\johndoe\geometry.json" --item "PSScene4Band" --asset "analytic_xml" --local "C:\planet_demo"
```

However, you can still decide to pass the filters and the filters you pass will overwrite existing filters

```
python ppipe.py dasync --infile "C:\Users\johndoe\geometry.json" --item "PSScene4Band" --asset "analytic_xml" --local "C:\planet_demo" --start "2018-06-01" --end "2018-08-01" --cmin "0" --cmax 0.4
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

### selenium update
**This is a key step since all upload function depends on this step, so make sure you run this**. This downloads selenium driver and places to your local directory for windows and Linux subsystems. This is the first step to use selenium supported upload.

``` ppipe update```

### gee selsetup
Once in a while the geckodriver requires manual input before signing into the google earth engine, this tool will allow you to interact with the initialization of Google Earth Engine code editor window. It allows the user to specify the account they want to use, and should only be needed once.

```geeup selsetup```

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
The script creates an Image Collection from GeoTIFFs in your local directory. By default, the image name in the collection is the same as the local directory name; with the optional parameter you can provide a different name.You have to process the metadata for images, which is covered in the next section along with a manifest type for Planet image and asset:
[Metadata parser](#metadata-parser).

```
usage: ppipe selupload [-h] --source SOURCE --dest DEST [-m METADATA]
                          [--large] [--nodata NODATA] [--bands BANDS]
                          [-u USER] [-b BUCKET]

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
  --large               (Advanced) Use multipart upload. Might help if upload
                        of large files is failing on some systems. Might cause
                        other issues.
  --nodata NODATA       The value to burn into the raster as NoData (missing
                        data)
  --bands BANDS         Comma-separated list of names to use for the image
                        bands. Spacesor other special characters are not
                        allowed.
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

### Task Query
This script counts all currently running,ready,completed,failed and cancelled tasks along with failed tasks. This is linked to the account you initialized with your google earth engine account. This takes no argument.
```
usage: ppipe.py tasks [-h]

optional arguments:
  -h, --help  show this help message and exit

ppipe.py tasks
```

### Assets Access
This tool allows you to set asset acess for either folder , collection or image recursively meaning you can add collection access properties for multiple assets at the same time.
```
usage: ppipe.py access [-h] --asset ASSET --user USER --role ROLE

optional arguments:
  -h, --help     show this help message and exit
  --asset ASSET  This is the path to the earth engine asset whose permission
                 you are changing folder/collection/image
  --user USER    Full email address of the user, try using "AllUsers" to make
                 it public
  --role ROLE    Choose between reader, writer or delete
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

### v0.4.7
- Download selenium drivers for all operating systems
- updated asset size, acl changer and other tools
- fixed metadata tool to work with python3
- overall general improvements to the tool and updates
- added selenium setup tools

### v0.4.6
- added fix for downloading selenium drivers
- improved error handling

### v0.4.4
- Fixed selenium download path
- Streamlined overall functions of the tool
- Handles metadata for clipped assets (use [porder](https://github.com/samapriya/porder) to clip)
- Updated selenium uploader to function with earthengine-api
- Overall improvements and stability check

### v0.4.3
- Added selenium uploader to upload images to Earth Engine after auth issues
- Overall improvements to the tools and added notifications and contribution notices

### v0.4.1
- Major improvements to earth engine tools including better task reporting, batch copy and move
- Improvement to the access tool which allows you to add read/write permissions for entire EE folder and collections for specific users

### v0.3.8

- Now include a tool to print your planet quota details ```pquota```
- Tool includes ```dasync``` which uses the [Planet's Python Client Downloader](https://github.com/planetlabs/planet-client-python) to activate, download using multithreading

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
