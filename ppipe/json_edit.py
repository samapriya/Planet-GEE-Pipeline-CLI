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

data_pso={"id": "","bands": [{"id": "b1"},{"id": "b2"},{"id": "b3"},{"id": "b4"}],"missingData": {"value": "0"},"properties": {"system:time_start":"","product_type":"","orbit":"",
"provider":"","instrument":"","satellite_id":"","tile_id":"","number_of_bands":"","epsg_code":"","resampling_kernel":"","number_of_rows":"","number_of_columns":"","gsd":"",
"cloud_cover":"","incidence_angle":"","sun_azimuth":"","sun_elevation":"","azimuth_angle":"","spacecraft_angle":"","radiometric_scale_factor":"","reflectance_coefficient_b1":"",
"reflectance_coefficient_b2":"","reflectance_coefficient_b3":"","reflectance_coefficient_b4":""},"tilesets": [{"sources": [{"primaryPath": "gs://earthengine-uploads/ee-L2.tif"}]}]}

data_psodn={"id": "","bands": [{"id": "b1"},{"id": "b2"},{"id": "b3"},{"id": "b4"}],"missingData": {"value": "0"},"properties": {"system:time_start":"","product_type":"","orbit":"",
"provider":"","instrument":"","satellite_id":"","tile_id":"","number_of_bands":"","epsg_code":"","resampling_kernel":"","number_of_rows":"","number_of_columns":"","gsd":"",
"cloud_cover":"","incidence_angle":"","sun_azimuth":"","sun_elevation":"","azimuth_angle":"","spacecraft_angle":""},"tilesets": [{"sources": [{"primaryPath": "gs://earthengine-uploads/ee-L2.tif"}]}]}

data_psov={"id": "","bands": [{"id": "b1"},{"id": "b2"},{"id": "b3"}],"missingData": {"value": "0"},"properties": {"system:time_start":"","product_type":"","orbit":"",
"provider":"","instrument":"","satellite_id":"","tile_id":"","number_of_bands":"","epsg_code":"","resampling_kernel":"","number_of_rows":"","number_of_columns":"","gsd":"",
"cloud_cover":"","incidence_angle":"","sun_azimuth":"","sun_elevation":"","azimuth_angle":"","spacecraft_angle":""},"tilesets": [{"sources": [{"primaryPath": "gs://earthengine-uploads/ee-L2.tif"}]}]}

data_ps4b={"id": "","bands": [{"id": "b1"},{"id": "b2"},{"id": "b3"},{"id": "b4"}],"missingData": {"value": "0"},"properties": {"system:time_start":"","product_type":"","orbit":"",
"provider":"","instrument":"","satellite_id":"","number_of_bands":"","epsg_code":"","resampling_kernel":"","number_of_rows":"","number_of_columns":"","gsd":"",
"cloud_cover":"","incidence_angle":"","sun_azimuth":"","sun_elevation":"","azimuth_angle":"","spacecraft_angle":"","radiometric_scale_factor":"","reflectance_coefficient_b1":"",
"reflectance_coefficient_b2":"","reflectance_coefficient_b3":"","reflectance_coefficient_b4":""},"tilesets": [{"sources": [{"primaryPath": "gs://earthengine-uploads/ee-L2.tif"}]}]}

data_ps4bdn={"id": "","bands": [{"id": "b1"},{"id": "b2"},{"id": "b3"},{"id": "b4"}],"missingData": {"value": "0"},"properties": {"system:time_start":"","product_type":"","orbit":"",
"provider":"","instrument":"","satellite_id":"","number_of_bands":"","epsg_code":"","resampling_kernel":"","number_of_rows":"","number_of_columns":"","gsd":"",
"cloud_cover":"","incidence_angle":"","sun_azimuth":"","sun_elevation":"","azimuth_angle":"","spacecraft_angle":""},"tilesets": [{"sources": [{"primaryPath": "gs://earthengine-uploads/ee-L2.tif"}]}]}

data_ps3b={"id": "","bands": [{"id": "b1"},{"id": "b2"},{"id": "b3"}],"missingData": {"value": "0"},"properties": {"system:time_start":"","product_type":"","orbit":"",
"provider":"","instrument":"","satellite_id":"","number_of_bands":"","epsg_code":"","resampling_kernel":"","number_of_rows":"","number_of_columns":"","gsd":"",
"cloud_cover":"","incidence_angle":"","sun_azimuth":"","sun_elevation":"","azimuth_angle":"","spacecraft_angle":"","radiometric_scale_factor":"","reflectance_coefficient_b1":"",
"reflectance_coefficient_b2":"","reflectance_coefficient_b3":""},"tilesets": [{"sources": [{"primaryPath": "gs://earthengine-uploads/ee-L2.tif"}]}]}

data_ps3bdn={"id": "","bands": [{"id": "b1"},{"id": "b2"},{"id": "b3"}],"missingData": {"value": "0"},"properties": {"system:time_start":"","product_type":"","orbit":"",
"provider":"","instrument":"","satellite_id":"","number_of_bands":"","epsg_code":"","resampling_kernel":"","number_of_rows":"","number_of_columns":"","gsd":"",
"cloud_cover":"","incidence_angle":"","sun_azimuth":"","sun_elevation":"","azimuth_angle":"","spacecraft_angle":""},"tilesets": [{"sources": [{"primaryPath": "gs://earthengine-uploads/ee-L2.tif"}]}]}

data_ps3bv={"id": "","bands": [{"id": "b1"},{"id": "b2"},{"id": "b3"}],"missingData": {"value": "0"},"properties": {"system:time_start":"","product_type":"","orbit":"",
"provider":"","instrument":"","satellite_id":"","number_of_bands":"","epsg_code":"","resampling_kernel":"","number_of_rows":"","number_of_columns":"","gsd":"",
"cloud_cover":"","incidence_angle":"","sun_azimuth":"","sun_elevation":"","azimuth_angle":"","spacecraft_angle":""},"tilesets": [{"sources": [{"primaryPath": "gs://earthengine-uploads/ee-L2.tif"}]}]}

data_reo={"id": "","bands": [{"id": "b1"},{"id": "b2"},{"id": "b3"},{"id": "b4"},{"id": "b5"}],"missingData": {"value": "0"},"properties": {"system:time_start":"", "product_type":"",
"tile_id":"","order_id":"","orbit":"","provider":"","instrument":"","satellite_id":"","number_of_bands":"","epsg_code":"","resampling_kernel":"","number_of_rows":"",
"number_of_columns":"","gsd":"","cloud_cover":"","incidence_angle":"","sun_azimuth":"","sun_elevation":"","azimuth_angle":"","spacecraft_angle":"",
"radiometric_scale_factor":""},"tilesets": [{"sources": [{"primaryPath": "gs://earthengine-uploads/ee-L2.tif"}]}]}

data_reov={"id": "","bands": [{"id": "b1"},{"id": "b2"},{"id": "b3"}],"missingData": {"value": "0"},"properties": {"system:time_start":"", "product_type":"",
"tile_id":"","order_id":"","orbit":"","provider":"","instrument":"","satellite_id":"","number_of_bands":"","epsg_code":"","resampling_kernel":"","number_of_rows":"",
"number_of_columns":"","gsd":"","cloud_cover":"","incidence_angle":"","sun_azimuth":"","sun_elevation":"","azimuth_angle":"","spacecraft_angle":"",
"radiometric_scale_factor":""},"tilesets": [{"sources": [{"primaryPath": "gs://earthengine-uploads/ee-L2.tif"}]}]}
