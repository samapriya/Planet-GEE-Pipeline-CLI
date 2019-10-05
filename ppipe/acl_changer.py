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
import os
import json

##initialize earth engine
ee.Initialize()

##request type of asset, asset path and user to give permission
def access(collection_path, user, role):
    header = ee.data.getInfo(collection_path)["type"]
    if header == "ImageCollection":
        lst = []
        lst.append(collection_path)
        assets_names = lst
    elif header == "Image":
        lst = []
        lst.append(collection_path)
        assets_names = lst
    elif header == "Table":
        lst = []
        lst.append(collection_path)
        assets_names = lst
    else:
        assets_list = ee.data.getList(params={"id": collection_path})
        assets_names = [os.path.basename(asset["id"]) for asset in assets_list]
    print("Changing permission for total of " + str(len(assets_names)) + ".....")
    for count, items in enumerate(assets_names):
        if header == "Folder":
            init = collection_path + "/" + items
            print("Working on item " + str(init))
        else:
            init = items
            print("Working on item " + str(init))
        acl = ee.data.getAssetAcl(init)
        if role == "reader":
            if not user in acl["readers"]:
                baselist = acl["readers"]
                baselist.append(user)
                acl["readers"] = baselist
                acl["owners"] = []
                try:
                    ee.data.setAssetAcl(init, json.dumps(acl))
                except Exception as e:
                    print(e)
            else:
                print("user already has read access to this asset:SKIPPING")
        if role == "writer":
            if not user in acl["writers"]:
                baselist = acl["writers"]
                baselist.append(user)
                acl["readers"] = baselist
                acl["owners"] = []
                try:
                    ee.data.setAssetAcl(init, json.dumps(acl))
                except Exception as e:
                    print(e)
            else:
                print("user already has write access to this asset:SKIPPING")
        if role == "delete":
            if not user in acl["readers"]:
                print("user does not have permission:SKIPPING")
            else:
                baselist = acl["readers"]
                baselist.remove(user)
                acl["readers"] = baselist
                acl["owners"] = []
                try:
                    ee.data.setAssetAcl(init, json.dumps(acl))
                except Exception as e:
                    print(e)
