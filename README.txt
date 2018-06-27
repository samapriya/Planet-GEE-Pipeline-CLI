=======================
Planet GEE Pipeline CLI
=======================

While moving between assets from Planet Inc and Google Earth Engine it was imperative to create a pipeline that allows for easy transitions between the two service end points and this tool is designed to act as a step by step process chain from Planet Assets to batch upload and modification within the Google Earth Engine environment. The ambition is apart from helping user with batch actions on assets along with interacting and extending capabilities of existing GEE CLI. It is developed case by case basis to include more features in the future as it becomes available or as need arises. You can access the `readme file here <https://github.com/samapriya/Planet-GEE-Pipeline-CLI/blob/master/README.md>`_


Credits
-------
* A portion of the work is suported by `JetStream Grant <https://jetstream-cloud.org/>`_

* Also supported by `Planet Labs Ambassador Program <https://www.planet.com/markets/ambassador-signup/>`_

* Original upload function adapted from `Lukasz's asset manager tool <https://github.com/tracek/gee_asset_manager>`_


Changelog
=========

v0.3.5
```````
* Fixed issues with space function
* Improved file size parsing

v0.3.2
```````
* Generalized CLI arguments
* Fixed subprocess shell issue for upload

v0.3.0
```````
* Allows for quiet authentication for use in Google Colab or non interactive environments
* Improved planet key entry and authentication protocols

v0.2.91
```````
* Fixed issue with Surface Reflectance metadata and manifest lib
* Improved ingestion support for (PSScene4Band analytic_Sr)[PS4B_SR]

v0.2.9
``````
* Fixed issues with generating id list
* Improved overall security of command calls

v0.2.2
``````
* Major improvements to ingestion using manifest ingest in Google Earth Engine
* Contains manifest for all commonly used Planet Data item and asset combinations
* Added additional tool to Earth Engine Enhancement including quota check before upload to GEE

v0.2.1
``````
* Fixed initialization loop issue

v0.2.0
``````
* Metadata parser and Uploader Can now handle PlanetScope 4 Band Surface Reflectance Datasets
* General Improvements

v0.1.9
``````
* Changes made to reflect updated GEE Addon tools
* general improvements

v0.1.8
``````
* Minor fixes to parser and general improvements
* Planet Key is now stored in a configuration folder which is safer "C:\users\.config\planet"
* Earth Engine now requires you to assign a field type for metadata meaning an alphanumeric column like satID cannot also have numeric values unless specified explicitly . Manifest option has been added to handle this (just use -mf "planetscope")
* Added capability to query download size and local disk capacity before downloading planet assets.
* Added the list function to generate list of collections or folders including reports
* Added the collection size tool which allows you to estimate total size or quota used from your allocated quota.
* ogr2ft feature is removed since Earth Engine now allows vector and table uploading.
