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

from osgeo import gdal
import json,os,time,csv,argparse,sys
import argparse
from pprint import pprint
from xml.dom import minidom

def srmeta(indir,mfile,errorlog,folder):
        path, dirs, files = next(os.walk(folder))
        file_count = len(files)
        i=1
        with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "product_type",
                                                          "orbit","provider","instrument","satellite_id",
                                                          "number_of_bands", "epsg_code","resampling_kernel",
                                                          "number_of_rows","number_of_columns","gsd","cloud_cover","incidence_angle",
                                                          "sun_azimuth","sun_elevation","azimuth_angle","spacecraft_angle","atmospheric_model",
                                                          "aerosol_Model", "aot_method", "aot_std", "aot_used","aot_Status","aot_mean_quality",
                                                          "luts_version","aot_coverage","aot_source","atmospheric_correction_algorithm"], delimiter=',')
                writer.writeheader()
        for filename in os.listdir(indir):
                if filename.endswith(".tif"):
                    infilename=os.path.join(folder,filename.replace("SR.tif","metadata.xml"))
                    try:
                        xmldoc = minidom.parse(infilename)
                        ps4band=xmldoc.getElementsByTagName('ps:EarthObservationMetaData')[0]
                        eopfilename = xmldoc.getElementsByTagName('eop:identifier')[0].firstChild.data
                        productType = xmldoc.getElementsByTagName('eop:productType')[0].firstChild.data
                        orbit = xmldoc.getElementsByTagName('eop:orbitType')[0].firstChild.data
                        acquisition = xmldoc.getElementsByTagName('eop:acquisitionDate')[0].firstChild.data
                        provider=xmldoc.getElementsByTagName("eop:shortName")[0].firstChild.data
                        instrument=xmldoc.getElementsByTagName("eop:shortName")[1].firstChild.data
                        satellite_id=xmldoc.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                        bands=xmldoc.getElementsByTagName("ps:numBands")[0].firstChild.data
                        epsg_code=xmldoc.getElementsByTagName("ps:epsgCode")[0].firstChild.data
                        resampling_kernel=xmldoc.getElementsByTagName("ps:resamplingKernel")[0].firstChild.data
                        number_rows=xmldoc.getElementsByTagName("ps:numRows")[0].firstChild.data
                        number_columns=xmldoc.getElementsByTagName("ps:numColumns")[0].firstChild.data
                        gsd=xmldoc.getElementsByTagName("ps:rowGsd")[0].firstChild.data
                        cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                        psb=xmldoc.getElementsByTagName("ps:bandNumber")[0].firstChild.data
                        psb1=xmldoc.getElementsByTagName("ps:bandNumber")[1].firstChild.data
                        psb3=xmldoc.getElementsByTagName("ps:bandNumber")[2].firstChild.data
                        psb4=xmldoc.getElementsByTagName("ps:bandNumber")[3].firstChild.data
                        psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                        psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                        psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                        psaz=xmldoc.getElementsByTagName("ps:azimuthAngle")[0].firstChild.data
                        pssca=xmldoc.getElementsByTagName("ps:spaceCraftViewAngle")[0].firstChild.data
                        date_time = acquisition.split('T')[0]
                        pattern = '%Y-%m-%d'
                        epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000
                        print("Processing "+str(i)+" of "+str(file_count))
                        i=i+1
                        gtif = gdal.Open(os.path.join(indir,filename))
                        date_time = gtif.GetMetadata()['TIFFTAG_DATETIME'].split(" ")[0]
                        pattern = '%Y:%m:%d'
                        epoch = int(time.mktime(time.strptime(date_time, pattern)))*1000
                        conv=json.loads(gtif.GetMetadata()['TIFFTAG_IMAGEDESCRIPTION'])
                        sid=str(filename).split("_")[2]
                        atmmodel=(conv['atmospheric_correction']['atmospheric_model'])
                        aotmethod=(conv['atmospheric_correction']['aot_method'])
                        aotused=(conv['atmospheric_correction']['aot_used'])
                        aotstat=(conv['atmospheric_correction']['aot_status'])
                        aotstd=(conv['atmospheric_correction']['aot_std'])
                        aotmq=(conv['atmospheric_correction']['aot_mean_quality'])
                        luts=(conv['atmospheric_correction']['luts_version'])
                        aotcov=(conv['atmospheric_correction']['aot_coverage'])
                        arsm=(conv['atmospheric_correction']['aerosol_model'])
                        aotsor=(conv['atmospheric_correction']['aot_source'])
                        atcoralgo=(conv['atmospheric_correction']['atmospheric_correction_algorithm'])
                        with open(mfile,'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([filename.split('.')[0],epoch,productType,orbit,provider,instrument,satellite_id,bands,epsg_code,resampling_kernel,number_rows,
                                             number_columns,format(float(gsd),'.2f'),format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),
                                             format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f'),str(atmmodel),str(arsm),str(aotmethod),
                                             format(float(aotstd),'.4f'),format(float(aotused),'.4f'),str(aotstat),aotmq,luts,format(float(aotcov),'.4f')
                                             ,str(aotsor),str(atcoralgo)])
                        csvfile.close()
                    except Exception as e:
                        print(e)
                        print("Issues with : "+str(os.path.splitext(filename)[0]))
                        with open(errorlog,'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([filename])
                        csvfile.close()
def srmeta_from_parser(args):
    srmeta(indir=args.indir,mfile=args.mfile,errorlog=args.errorlog,folder=args.folder)
def main(args=None):
    parser = argparse.ArgumentParser('Tool to process PlanetScope Surface Reflectance Data')
    subparsers=parser.add_subparsers()
    parser_srmeta=subparsers.add_parser("PSR",help="PlanetScope SR Metadata")
    parser_srmeta.add_argument('--indir', help='Folder with SR images')
    parser_srmeta.add_argument('--mfile', help='metadatafile')
    parser_srmeta.add_argument('--errorlog', help='errorlog file')
    parser_srmeta.add_argument('--folder', help='directory with metadata files')
    parser_srmeta.set_defaults(func=srmeta_from_parser)
    args = parser.parse_args()

    args.func(args)
if __name__ == '__main__':
    main()
