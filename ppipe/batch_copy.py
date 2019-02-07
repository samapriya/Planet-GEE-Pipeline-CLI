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
ee.Initialize()

def copy(collection_path,final_path):
    assets_list = ee.data.getList(params={'id': collection_path})
    assets_names = [os.path.basename(asset['id']) for asset in assets_list]
    print('Copying a total of '+str(len(assets_names))+'.....')
    for count,items in enumerate(assets_names):
        print ('Copying '+str(count+1)+' of '+str(len(assets_names)), end='\r')
        init=collection_path+'/'+items
        final=final_path+'/'+items
        try:
            ee.data.copyAsset(init,final)
        except Exception as e:
            pass
#batchcopy(collection_path='users/samapriya/Belem/BelemRE',final_path='users/samapriya/bl')
