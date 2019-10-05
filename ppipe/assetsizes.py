from __future__ import print_function

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

import ee, subprocess, os

##initialize earth engine
ee.Initialize()

suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]


def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


l = []


def assetsize(asset):
    header = ee.data.getInfo(asset)["type"]
    if header == "ImageCollection":
        collc = ee.ImageCollection(asset)
        size = collc.aggregate_array("system:asset_size")
        print("")
        print(str(asset) + " ===> " + str(humansize(sum(size.getInfo()))))
        print("Total number of items in collection: " + str(collc.size().getInfo()))
    elif header == "Image":
        collc = ee.Image(asset)
        print("")
        print(
            str(asset)
            + " ===> "
            + str(humansize(collc.get("system:asset_size").getInfo()))
        )
    elif header == "Table":
        collc = ee.FeatureCollection(asset)
        print("")
        print(
            str(asset)
            + " ===> "
            + str(humansize(collc.get("system:asset_size").getInfo()))
        )
    elif header == "Folder":
        b = subprocess.check_output(
            "earthengine --no-use_cloud_api du " + asset + " -s", shell=True
        )
        num = subprocess.check_output(
            "earthengine --no-use_cloud_api ls " + asset, shell=True
        )
        size = humansize(float(b.strip().split(" ")[0]))
        print("")
        print(str(asset) + " ===> " + str(size))
        print("Total number of items in folder: " + str(len(num.split("\n")) - 1))


if __name__ == "__main__":
    assetsize(None)
