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


#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import os
import json

os.chdir(os.path.dirname(os.path.realpath(__file__)))
path = os.path.dirname(os.path.realpath(__file__))
template = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Polygon", "coordinates": []},
        }
    ],
}


def ddownload(infile, item, asset, dirc, start, end, cmin, cmax):
    if cmin is None:
        cmin = 0
    if cmax is None:
        cmax = 100
    try:
        if infile.endswith(".geojson"):
            st = start
            ed = end
            ccovermin = cmin
            ccovermax = cmax
            subprocess.call(
                "planet data download --item-type "
                + str(item)
                + " --geom "
                + '"'
                + infile
                + '"'
                + " --date acquired gt "
                + str(st)
                + " --date acquired lt "
                + str(ed)
                + " --range cloud_cover gt "
                + str(ccovermin)
                + " --range cloud_cover lt "
                + str(ccovermax)
                + " --asset-type "
                + str(asset)
                + " --dest "
                + '"'
                + dirc
                + '"',
                shell=True,
            )
        elif infile.endswith(".json"):
            with open(infile) as aoi:
                aoi_resp = json.load(aoi)
                for items in aoi_resp["config"]:
                    if start == None and end == None:
                        if (
                            items["type"] == "DateRangeFilter"
                            and items["field_name"] == "acquired"
                        ):
                            st = items["config"]["gte"].split("T")[0]
                            ed = items["config"]["lte"].split("T")[0]
                    else:
                        st = start
                        ed = end
                    if items["type"] == "GeometryFilter":

                        # print(items['config']['coordinates'])

                        template["features"][0]["geometry"]["coordinates"] = items[
                            "config"
                        ]["coordinates"]
                        with open(os.path.join(path, "bounds.geojson"), "w") as f:
                            f.write(json.dumps(template))
                    if cmin == None and cmax == None:
                        if (
                            items["type"] == "RangeFilter"
                            and items["field_name"] == "cloud_cover"
                        ):
                            ccovermin = items["config"]["gte"]
                            ccovermax = items["config"]["lte"]
                    else:
                        ccovermin = cmin
                        ccovermax = cmax
                if os.path.exists(os.path.join(path, "bounds.geojson")):
                    subprocess.call(
                        "planet data download --item-type "
                        + str(item)
                        + " --geom "
                        + '"'
                        + os.path.join(path, "bounds.geojson")
                        + '"'
                        + " --date acquired gt "
                        + str(st)
                        + " --date acquired lt "
                        + str(ed)
                        + " --range cloud_cover gt "
                        + str(ccovermin)
                        + " --range cloud_cover lt "
                        + str(ccovermax)
                        + " --asset-type "
                        + str(asset)
                        + " --dest "
                        + '"'
                        + dirc
                        + '"',
                        shell=True,
                    )
    except Exception as e:
        print(e)
