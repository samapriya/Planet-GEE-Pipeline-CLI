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

import ee
import subprocess
import csv
import os

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


def object_sz(object):
    sz = humansize(object.get("system:asset_size").getInfo())
    return sz


def collect_sz(object):
    sz = humansize(
        object.reduceColumns(ee.Reducer.sum(), ["system:asset_size"])
        .get("sum")
        .getInfo()
    )
    return sz


def lst(location, typ, items=None, output=None):
    if items is None and typ == "print":
        assets_list = ee.data.getList(params={"id": location})
        for things in assets_list:
            header = things["type"]
            tail = things["id"]
            try:
                if header == "ImageCollection":
                    collc = ee.ImageCollection(tail)
                    ast = collc.size().getInfo()
                    sz = collect_sz(collc)
                    print(
                        "Image Collection: "
                        + str(tail)
                        + " has "
                        + str(ast)
                        + " images a total of "
                        + str(sz)
                    )
                elif header == "Image":
                    collc = ee.Image(tail)
                    sz = object_sz(collc)
                    print("Image: " + str(tail) + " is " + str(sz))
                elif header == "Table":
                    collc = ee.FeatureCollection(tail)
                    sz = object_sz(collc)
                    print("Table: " + str(tail) + " is " + str(sz))
                elif (
                    header == "Folder"
                ):  ##Folders are not added to the list but are print
                    assets_list = ee.data.getList(params={"id": location})
                    print("Folder: " + str(tail) + " has " + str(len(assets_list)))
            except Exception as e:
                print(e)
    elif items > 0 and typ == "print":
        assets_list = ee.data.getList(params={"id": location})
        if int(len(assets_list)) > int(items):
            subset = assets_list[: int(items)]
            for things in subset:
                header = things["type"]
                tail = things["id"]
                try:
                    if header == "ImageCollection":
                        collc = ee.ImageCollection(tail)
                        ast = collc.size().getInfo()
                        sz = collect_sz(collc)
                        print(
                            "Image Collection: "
                            + str(tail)
                            + " has "
                            + str(ast)
                            + " images a total of "
                            + str(sz)
                        )
                    elif header == "Image":
                        collc = ee.Image(tail)
                        sz = object_sz(collc)
                        print("Image: " + str(tail) + " is " + str(sz))
                    elif header == "Table":
                        collc = ee.FeatureCollection(tail)
                        sz = object_sz(collc)
                        print("Table: " + str(tail) + " is " + str(sz))
                    elif (
                        header == "Folder"
                    ):  ##Folders are not added to the list but are print
                        assets_list = ee.data.getList(params={"id": location})
                        print("Folder: " + str(tail) + " has " + str(len(assets_list)))
                except Exception as e:
                    print(e)
    elif items is None and typ == "report":
        with open(output, "wb") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=["type", "path", "No of Assets", "size"],
                delimiter=",",
            )
            writer.writeheader()
        assets_list = ee.data.getList(params={"id": location})
        for things in assets_list:
            header = things["type"]
            tail = things["id"]
            try:
                if header == "ImageCollection":
                    collc = ee.ImageCollection(tail)
                    ast = collc.size().getInfo()
                    sz = collect_sz(collc)
                    print(
                        "Image Collection: "
                        + str(tail)
                        + " has "
                        + str(ast)
                        + " images a total of "
                        + str(sz)
                    )
                    with open(output, "a") as csvfile:
                        writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                        writer.writerow([header, tail, ast, str(sz)])
                    csvfile.close()
                elif header == "Image":
                    collc = ee.Image(tail)
                    sz = object_sz(collc)
                    print("Image: " + str(tail) + " is " + str(sz))
                    with open(output, "a") as csvfile:
                        writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                        writer.writerow([header, tail, ast, str(sz)])
                    csvfile.close()
                elif header == "Table":
                    collc = ee.FeatureCollection(tail)
                    sz = object_sz(collc)
                    print("Table: " + str(tail) + " is " + str(sz))
                    with open(output, "a") as csvfile:
                        writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                        writer.writerow([header, tail, ast, str(sz)])
                    csvfile.close()
                elif (
                    header == "Folder"
                ):  ##Folders are not added to the list but are print
                    assets_list = ee.data.getList(params={"id": location})
                    print("Folder: " + str(tail) + " has " + str(len(assets_list)))
            except Exception as e:
                print(e)
    elif items > 0 and typ == "report":
        with open(output, "wb") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=["type", "path", "No of Assets", "size"],
                delimiter=",",
            )
            writer.writeheader()
        assets_list = ee.data.getList(params={"id": location})
        if int(len(assets_list)) > int(items):
            subset = assets_list[: int(items)]
            for things in subset:
                header = things["type"]
                tail = things["id"]
                try:
                    if header == "ImageCollection":
                        collc = ee.ImageCollection(tail)
                        ast = collc.size().getInfo()
                        sz = collect_sz(collc)
                        print(
                            "Image Collection: "
                            + str(tail)
                            + " has "
                            + str(ast)
                            + " images a total of "
                            + str(sz)
                        )
                        with open(output, "a") as csvfile:
                            writer = csv.writer(
                                csvfile, delimiter=",", lineterminator="\n"
                            )
                            writer.writerow([header, tail, ast, str(sz)])
                        csvfile.close()
                    elif header == "Image":
                        collc = ee.Image(tail)
                        sz = object_sz(collc)
                        print("Image: " + str(tail) + " is " + str(sz))
                        with open(output, "a") as csvfile:
                            writer = csv.writer(
                                csvfile, delimiter=",", lineterminator="\n"
                            )
                            writer.writerow([header, tail, 1, str(sz)])
                        csvfile.close()
                    elif header == "Table":
                        collc = ee.FeatureCollection(tail)
                        sz = object_sz(collc)
                        print("Table: " + str(tail) + " is " + str(sz))
                        with open(output, "a") as csvfile:
                            writer = csv.writer(
                                csvfile, delimiter=",", lineterminator="\n"
                            )
                            writer.writerow([header, tail, 1, str(sz)])
                        csvfile.close()
                    elif (
                        header == "Folder"
                    ):  ##Folders are not added to the list but are print
                        assets_list = ee.data.getList(params={"id": location})
                        print("Folder: " + str(tail) + " has " + str(len(assets_list)))
                except Exception as e:
                    print(e)


# lst(location="users/samapriya/Belem", typ="report",items=0,output=r"C:\planet_demo\rep.csv")
