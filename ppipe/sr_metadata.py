from osgeo import gdal
import json,os,time,csv,argparse,sys
import argparse
from pprint import pprint
from xml.dom import minidom

def srmeta(indir,mfile,errorlog,folder):
        with open(mfile,'wb') as csvfile:
            writer=csv.DictWriter(csvfile,fieldnames=["id_no", "platform", "satType","satID", "numBands", "cloudcover","system:time_start", "AtmModel","Aerosol_Model", "AOT_Method", "AOT_Std", "AOT_Used",
                                                      "AOT_Status","AOT_MeanQual","LUTS_Version","SolarZenAngle","AOT_Coverage","AOT_Source","AtmCorr_Alg","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle"], delimiter=',')
            writer.writeheader()
        for filename in os.listdir(indir):
                if filename.endswith(".tif"):
                    infilename=os.path.join(folder,filename.replace("sr","xml"))
                    print("Processing "+str(filename))
                    print("Sat ID : "+str(filename).split("_")[2])
                    try:
                        from xml.dom import minidom
                        xmldoc = minidom.parse(infilename)
                        platform=xmldoc.getElementsByTagName("eop:shortName")[0].firstChild.data
                        sid=xmldoc.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                        sattype=xmldoc.getElementsByTagName("eop:shortName")[1].firstChild.data
                        platform=xmldoc.getElementsByTagName("eop:shortName")[0].firstChild.data
                        bands=xmldoc.getElementsByTagName("ps:numBands")[0].firstChild.data
                        cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                        psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                        psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                        psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                        psaz=xmldoc.getElementsByTagName("ps:azimuthAngle")[0].firstChild.data
                        pssca=xmldoc.getElementsByTagName("ps:spaceCraftViewAngle")[0].firstChild.data
                        gtif = gdal.Open(os.path.join(indir,filename))
                        date_time = gtif.GetMetadata()['TIFFTAG_DATETIME'].split(" ")[0]
                        pattern = '%Y:%m:%d'
                        epoch = int(time.mktime(time.strptime(date_time, pattern)))*1000
                        conv=json.loads(gtif.GetMetadata()['TIFFTAG_IMAGEDESCRIPTION'])
                        sid=str(filename).split("_")[2]
                        atmmodel=(conv['atmospheric_correction']['atmospheric_model'])
                        sraz=(conv['atmospheric_correction']['solar_azimuth_angle'])
                        aotmethod=(conv['atmospheric_correction']['aot_method'])
                        aotused=(conv['atmospheric_correction']['aot_used'])
                        aotstat=(conv['atmospheric_correction']['aot_status'])
                        aotstd=(conv['atmospheric_correction']['aot_std'])
                        aotmq=(conv['atmospheric_correction']['aot_mean_quality'])
                        luts=(conv['atmospheric_correction']['luts_version'])
                        szen=(conv['atmospheric_correction']['solar_zenith_angle'])
                        aotcov=(conv['atmospheric_correction']['aot_coverage'])
                        arsm=(conv['atmospheric_correction']['aerosol_model'])
                        aotsor=(conv['atmospheric_correction']['aot_source'])
                        atcoralgo=(conv['atmospheric_correction']['atmospheric_correction_algorithm'])
                        #print("Satellite ID: "+str(sid))
                        print("Number of Bands: "+bands)
                        print("Cloud Cover: "+format(float(cloud),'.2f'))
                        print ("Platform: "+str(platform))
                        print("Satellite Type: "+str(sattype))
                        print("Bands: "+str(bands))
                        print("Atmospheric Model : "+str(atmmodel))
                        print("Solar Azimuth Angle : "+format(float(sraz),'.2f'))
                        print("Aerosol Optical Thickness(AOT) Method : "+str(aotmethod))
                        print("Aerosol Optical Thickness(AOT) Used : "+format(float(aotused),'.4f'))
                        print("Aerosol Optical Thickness(AOT) Status : "+str(aotstat))
                        print("Aerosol Optical Thickness(AOT) Std : "+format(float(aotstd),'.4f'))
                        print("Aerosol Optical Thickness(AOT) mean quality : "+str(aotmq))
                        print("LUTS Version : "+str(luts))
                        print("Solar Zenith Angle : "+format(float(szen),'.2f'))
                        print("Aerosol Optical Thickness(AOT) Coverage : "+format(float(aotcov),'.4f'))
                        print("Aerosol Model : "+str(arsm))
                        print("Aerosol Optical Thickness(AOT) Source : "+str(aotsor))
                        print("ATCOR Correction Algorithm : "+str(atcoralgo))
                        print("Date Time : "+str(date_time))
                        print("Epoch Time : "+str(epoch))
                        print(" ")
                        with open(mfile,'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([os.path.splitext(filename)[0],platform,sattype,str(sid),bands,format(float(cloud),'.2f'),epoch,str(atmmodel),str(arsm),str(aotmethod),format(float(aotstd),'.4f'),
                                             format(float(aotused),'.4f'),str(aotstat),aotmq,luts,format(float(szen),'.2f'),format(float(aotcov),'.4f'),str(aotsor),str(atcoralgo),format(float(psia),'.4f'),format(float(psilaz),'.2f'),
                            format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.2f')])
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
