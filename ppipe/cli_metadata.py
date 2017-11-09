import argparse,sys,os,time,csv,json,subprocess
from xml.dom import minidom
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def metadata(asset,mf,mfile,errorlog,directory=None):
    if directory is None:
        if asset == 'PSO': # PS OrthoTile Analytic
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "satType","satID", "tileID", "numBands", "cloudcover","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle","rsf","refCoeffB1","refCoeffB2","refCoeffB3","refCoeffB4"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                infilename = os.path.join(folder,filename)
                fsp=filename.split("_x")[0]
                try:
                    #This gets the main xml parse tree
                    xmldoc=minidom.parse(infilename)
                    ps=xmldoc.getElementsByTagName("ps:EarthObservationMetaData")[0]
                    observation=xmldoc.getElementsByTagName("ps:EarthObservationResult") [0]
                    eopfilename=xmldoc.getElementsByTagName("eop:fileName")[0].firstChild.data
                    meta=xmldoc.getElementsByTagName("ps:EarthObservationMetaData")[0]
                    acquisition= meta.getElementsByTagName("eop:acquisitionDate")[0].firstChild.data
                    tile=meta.getElementsByTagName("ps:tileId")[0].firstChild.data
                    equip=xmldoc.getElementsByTagName("eop:Platform")[0]
                    platform=equip.getElementsByTagName("eop:shortName")[0].firstChild.data
                    sid=equip.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                    equip=xmldoc.getElementsByTagName("eop:instrument")[0]
                    sattype=equip.getElementsByTagName("eop:shortName")[0].firstChild.data
                    bands=xmldoc.getElementsByTagName("ps:numBands")[0].firstChild.data
                    cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                    psb=xmldoc.getElementsByTagName("ps:bandNumber")[0].firstChild.data
                    psb1=xmldoc.getElementsByTagName("ps:bandNumber")[1].firstChild.data
                    psb3=xmldoc.getElementsByTagName("ps:bandNumber")[2].firstChild.data
                    psb4=xmldoc.getElementsByTagName("ps:bandNumber")[3].firstChild.data
                    psbrad=xmldoc.getElementsByTagName("ps:radiometricScaleFactor")[0].firstChild.data
                    psb1ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
                    psb2ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[1].firstChild.data
                    psb3ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[2].firstChild.data
                    psb4ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[3].firstChild.data
                    psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                    psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                    psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                    psaz=xmldoc.getElementsByTagName("ps:azimuthAngle")[0].firstChild.data
                    pssca=xmldoc.getElementsByTagName("ps:spaceCraftViewAngle")[0].firstChild.data
                    print("ID_Name:", eopfilename.split(".")[0])
                    print("Acquisition Date:", acquisition.split("T")[0])
                    print("Satellite Type:", platform)
                    print("ShortName:", sattype)
                    print("Satellite ID:", str(sid))
                    print("Tile ID:", tile)
                    print("Number of Bands:", bands)
                    print("Cloud Cover:", format(float(cloud),'.2f'))
                    print("PS Incidence Angle",format(float(psia),'.4f'))
                    print("PS illumination azimuth angle",format(float(psilaz),'.2f'))
                    print("PS illumination elevation angle",format(float(psilelv),'.2f'))
                    print("PS Azimuth angle",format(float(psaz),'.2f'))
                    print("PS SpaceCraft angle",format(float(pssca),'.4f'))
                    print("Radiometric Scale Factor",psbrad)
                    print("ReflectanceCoefficient B1",format(float(psb1ref),'.8f'))
                    print("ReflectanceCoefficient B2",format(float(psb2ref),'.8f'))
                    print("ReflectanceCoefficient B3",format(float(psb3ref),'.8f'))
                    print("ReflectanceCoefficient B4",format(float(psb4ref),'.8f'))
                    date_time = acquisition.split("T")[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern)))*1000
                    print("epoch time", epoch)
                    with open(mfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([fsp,epoch,platform,sattype,str(sid),tile,bands,format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),
                        format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f'),psbrad,format(float(psb1ref),'.8f'),
                        format(float(psb2ref),'.8f'),format(float(psb3ref),'.8f'),format(float(psb4ref),'.8f')])
                    csvfile.close()
                except Exception as e:
                    print(infilename)
                    print(e)
                    with open(errorlog,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([infilename])
                    csvfile.close()

        elif asset == 'PSO_DN': #PS OrthoTile Analytic Derivative DN
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "satType","satID", "tileID", "numBands", "cloudcover","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                infilename = os.path.join(folder, filename)
                fsp = filename.split('_x')[0]
                try:
                    xmldoc = minidom.parse(infilename)
                    ps4band=xmldoc.getElementsByTagName('ps:EarthObservationMetaData')[0]
                    eopfilename = xmldoc.getElementsByTagName('eop:identifier')[0].firstChild.data
                    sid=xmldoc.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                    acquisition = xmldoc.getElementsByTagName('eop:acquisitionDate')[0].firstChild.data
                    platform=xmldoc.getElementsByTagName("eop:shortName")[0].firstChild.data
                    tile=xmldoc.getElementsByTagName("ps:tileId")[0].firstChild.data
                    sattype=xmldoc.getElementsByTagName("eop:shortName")[1].firstChild.data
                    bands=xmldoc.getElementsByTagName("ps:numBands")[0].firstChild.data
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
                    print ('ID_Name:', eopfilename.split('.')[0])
                    print ('Acquisition Date:', acquisition.split('T')[0])
                    print("Acquisition Date:", acquisition.split("T")[0])
                    print("Satellite Type:", platform)
                    print("ShortName:", sattype)
                    print("Satellite ID:", str(sid))
                    print("Tile ID:",tile)
                    print("Number of Bands:", bands)
                    print("Cloud Cover:", format(float(cloud),'.2f'))
                    print("PS Incidence Angle",format(float(psia),'.4f'))
                    print("PS illumination azimuth angle",format(float(psilaz),'.2f'))
                    print("PS illumination elevation angle",format(float(psilelv),'.2f'))
                    print("PS Azimuth angle",format(float(psaz),'.2f'))
                    print("PS SpaceCraft angle",format(float(pssca),'.4f'))
                    date_time = acquisition.split('T')[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000
                    print ('epoch time', epoch)
                    with open(mfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([fsp,epoch,platform,sattype,str(sid),tile,bands,format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),
                        format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f')])
                    csvfile.close()
                except Exception as e:
                    print(infilename)
                    print (e)
                    with open(errorlog,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([infilename])
                    csvfile.close()
        elif asset == 'PSO_V': #PS OrthoTile Analytic Derivative Visual
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "satType","satID", "tileID", "numBands", "cloudcover","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                infilename = os.path.join(folder, filename)
                fsp = filename.split('_x')[0]
                try:
                    xmldoc = minidom.parse(infilename)
                    eopfilename = xmldoc.getElementsByTagName('eop:identifier')[0].firstChild.data
                    sid=xmldoc.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                    acquisition = xmldoc.getElementsByTagName('eop:acquisitionDate')[0].firstChild.data
                    platform=xmldoc.getElementsByTagName("eop:shortName")[0].firstChild.data
                    tile=xmldoc.getElementsByTagName("ps:tileId")[0].firstChild.data
                    sattype=xmldoc.getElementsByTagName("eop:shortName")[1].firstChild.data
                    bands=xmldoc.getElementsByTagName("ps:numBands")[0].firstChild.data
                    cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                    psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                    psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                    psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                    psaz=xmldoc.getElementsByTagName("ps:azimuthAngle")[0].firstChild.data
                    pssca=xmldoc.getElementsByTagName("ps:spaceCraftViewAngle")[0].firstChild.data
                    print ('ID_Name:', eopfilename.split('.')[0])
                    print ('Acquisition Date:', acquisition.split('T')[0])
                    print("Acquisition Date:", acquisition.split("T")[0])
                    print("Satellite Type:", platform)
                    print("ShortName:", sattype)
                    print("Satellite ID:", str(sid))
                    print("Tile ID:",tile)
                    print("Number of Bands:", bands)
                    print("Cloud Cover:", format(float(cloud),'.2f'))
                    print("PS Incidence Angle",format(float(psia),'.4f'))
                    print("PS illumination azimuth angle",format(float(psilaz),'.2f'))
                    print("PS illumination elevation angle",format(float(psilelv),'.2f'))
                    print("PS Azimuth angle",format(float(psaz),'.2f'))
                    print("PS SpaceCraft angle",format(float(pssca),'.4f'))
                    date_time = acquisition.split('T')[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000
                    print ('epoch time', epoch)
                    with open(mfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([fsp,epoch,platform,sattype,str(sid),tile,bands,format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),
                        format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f')])
                    csvfile.close()
                except Exception as e:
                    print(infilename)
                    print(e)
                    with open(errorlog,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([infilename])
                    csvfile.close()
        elif asset == 'PS4B': #PS 4 Band Scene Derivative Analytic
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "satType","satID", "numBands", "cloudcover","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle","rsf","refCoeffB1","refCoeffB2","refCoeffB3","refCoeffB4"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                infilename = os.path.join(folder, filename)
                fsp = filename.split('_x')[0]
                try:
                    xmldoc = minidom.parse(infilename)
                    ps4band=xmldoc.getElementsByTagName('ps:EarthObservationMetaData')[0]
                    eopfilename = xmldoc.getElementsByTagName('eop:identifier')[0].firstChild.data
                    acquisition = xmldoc.getElementsByTagName('eop:acquisitionDate')[0].firstChild.data
                    sid=xmldoc.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                    sattype=xmldoc.getElementsByTagName("eop:shortName")[1].firstChild.data
                    platform=xmldoc.getElementsByTagName("eop:shortName")[0].firstChild.data
                    bands=xmldoc.getElementsByTagName("ps:numBands")[0].firstChild.data
                    cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                    psb=xmldoc.getElementsByTagName("ps:bandNumber")[0].firstChild.data
                    psb1=xmldoc.getElementsByTagName("ps:bandNumber")[1].firstChild.data
                    psb3=xmldoc.getElementsByTagName("ps:bandNumber")[2].firstChild.data
                    psb4=xmldoc.getElementsByTagName("ps:bandNumber")[3].firstChild.data
                    psbrad=xmldoc.getElementsByTagName("ps:radiometricScaleFactor")[0].firstChild.data
                    psb1ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
                    psb2ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[1].firstChild.data
                    psb3ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[2].firstChild.data
                    psb4ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[3].firstChild.data
                    psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                    psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                    psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                    psaz=xmldoc.getElementsByTagName("ps:azimuthAngle")[0].firstChild.data
                    pssca=xmldoc.getElementsByTagName("ps:spaceCraftViewAngle")[0].firstChild.data
                    print ('ID_Name:', eopfilename.split('.')[0])
                    print ('Acquisition Date:', acquisition.split('T')[0])
                    print("Acquisition Date:", acquisition.split("T")[0])
                    print("ShortName:", sattype)
                    print("Satellite ID:", str(sid))
                    print("Number of Bands:", bands)
                    print("Cloud Cover:", format(float(cloud),'.2f'))
                    print("PS Incidence Angle",format(float(psia),'.4f'))
                    print("PS illumination azimuth angle",format(float(psilaz),'.2f'))
                    print("PS illumination elevation angle",format(float(psilelv),'.2f'))
                    print("PS Azimuth angle",format(float(psaz),'.2f'))
                    print("PS SpaceCraft angle",format(float(pssca),'.4f'))
                    print("Radiometric Scale Factor",psbrad)
                    print("ReflectanceCoefficient B1",format(float(psb1ref),'.8f'))
                    print("ReflectanceCoefficient B2",format(float(psb2ref),'.8f'))
                    print("ReflectanceCoefficient B3",format(float(psb3ref),'.8f'))
                    print("ReflectanceCoefficient B4",format(float(psb4ref),'.8f'))
                    date_time = acquisition.split('T')[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000
                    with open(mfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([fsp,epoch,platform,sattype,str(sid),bands,format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),
                        format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f'),psbrad,format(float(psb1ref),'.8f'),
                        format(float(psb2ref),'.8f'),format(float(psb3ref),'.8f'),format(float(psb4ref),'.8f')])
                    csvfile.close()
                except Exception as e:
                    print(infilename)
                    print(e)
                    with open(errorlog,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([infilename])
                    csvfile.close()
        elif asset == 'PS4B_DN': #PS 4 Band Scene Derivative DN
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "satType","satID", "numBands", "cloudcover","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                infilename = os.path.join(folder, filename)
                fsp = filename.split('_x')[0]
                try:
                    xmldoc = minidom.parse(infilename)
                    eopfilename = xmldoc.getElementsByTagName('eop:identifier')[0].firstChild.data
                    acquisition = xmldoc.getElementsByTagName('eop:acquisitionDate')[0].firstChild.data
                    bands=xmldoc.getElementsByTagName("ps:numBands")[0].firstChild.data
                    platform=xmldoc.getElementsByTagName("eop:shortName")[0].firstChild.data
                    sid=xmldoc.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                    sattype=xmldoc.getElementsByTagName("eop:shortName")[1].firstChild.data
                    cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                    psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                    psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                    psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                    psaz=xmldoc.getElementsByTagName("ps:azimuthAngle")[0].firstChild.data
                    pssca=xmldoc.getElementsByTagName("ps:spaceCraftViewAngle")[0].firstChild.data
                    print ('ID_Name:', eopfilename.split('.')[0])
                    print ('Acquisition Date:', acquisition.split('T')[0])
                    print("Acquisition Date:", acquisition.split("T")[0])
                    print("Satellite Type:", platform)
                    print("ShortName:", sattype)
                    print("Number of Bands:", bands)
                    print("Cloud Cover:", format(float(cloud),'.2f'))
                    print("PS Incidence Angle",format(float(psia),'.4f'))
                    print("PS illumination azimuth angle",format(float(psilaz),'.2f'))
                    print("PS illumination elevation angle",format(float(psilelv),'.2f'))
                    print("PS Azimuth angle",format(float(psaz),'.2f'))
                    print("PS SpaceCraft angle",format(float(pssca),'.4f'))
                    date_time = acquisition.split('T')[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000
                    with open(mfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([fsp,epoch,platform,sattype,str(sid),bands,format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),
                        format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f')])
                    csvfile.close()
                except Exception as e:
                    print(infilename)
                    print(e)
                    with open(errorlog,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([infilename])
                    csvfile.close()
        elif asset == 'PS3B': #PS 3 Band Scene Derivative Analytic
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "satType","satID", "numBands", "cloudcover","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle","rsf","refCoeffB1","refCoeffB2","refCoeffB3"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                infilename = os.path.join(folder, filename)
                fsp = filename.split('_x')[0]
                print(fsp)
                try:
                    xmldoc = minidom.parse(infilename)
                    eopfilename = xmldoc.getElementsByTagName('eop:identifier')[0].firstChild.data
                    acquisition = xmldoc.getElementsByTagName('eop:acquisitionDate')[0].firstChild.data
                    sid=xmldoc.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                    platform=xmldoc.getElementsByTagName("eop:shortName")[0].firstChild.data
                    sattype=xmldoc.getElementsByTagName("eop:shortName")[1].firstChild.data
                    bands=xmldoc.getElementsByTagName("ps:numBands")[0].firstChild.data
                    cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                    psb=xmldoc.getElementsByTagName("ps:bandNumber")[0].firstChild.data
                    psb1=xmldoc.getElementsByTagName("ps:bandNumber")[1].firstChild.data
                    psb3=xmldoc.getElementsByTagName("ps:bandNumber")[2].firstChild.data
                    psbrad=xmldoc.getElementsByTagName("ps:radiometricScaleFactor")[0].firstChild.data
                    psb1ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
                    psb2ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[1].firstChild.data
                    psb3ref=xmldoc.getElementsByTagName("ps:reflectanceCoefficient")[2].firstChild.data
                    psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                    psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                    psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                    psaz=xmldoc.getElementsByTagName("ps:azimuthAngle")[0].firstChild.data
                    pssca=xmldoc.getElementsByTagName("ps:spaceCraftViewAngle")[0].firstChild.data
                    print ('ID_Name:', eopfilename.split('.')[0])
                    print ('Acquisition Date:', acquisition.split('T')[0])
                    print("Acquisition Date:", acquisition.split("T")[0])
                    print("ShortName:", sattype)
                    print("Satellite ID:", str(sid))
                    print("Number of Bands:", bands)
                    print("Cloud Cover:", format(float(cloud),'.2f'))
                    print("PS Incidence Angle",format(float(psia),'.4f'))
                    print("PS illumination azimuth angle",format(float(psilaz),'.2f'))
                    print("PS illumination elevation angle",format(float(psilelv),'.2f'))
                    print("PS Azimuth angle",format(float(psaz),'.2f'))
                    print("PS SpaceCraft angle",format(float(pssca),'.4f'))
                    print("Radiometric Scale Factor",psbrad)
                    print("ReflectanceCoefficient B1",format(float(psb1ref),'.8f'))
                    print("ReflectanceCoefficient B2",format(float(psb2ref),'.8f'))
                    print("ReflectanceCoefficient B3",format(float(psb3ref),'.8f'))
                    date_time = acquisition.split('T')[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000
                    with open(mfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([fsp,epoch,platform,sattype,str(sid),bands,format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),
                        format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f'),psbrad,format(float(psb1ref),'.8f'),
                        format(float(psb2ref),'.8f'),format(float(psb3ref),'.8f')])
                    csvfile.close()
                except Exception as e:
                    print(infilename)
                    print(e)
                    with open(errorlog,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([infilename])
                    csvfile.close()
        elif asset == 'PS3B_DN': #PS 3 Band Scene Derivative DN
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "satType","satID", "numBands", "cloudcover","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                infilename = os.path.join(folder, filename)
                fsp = filename.split('_x')[0]
                try:
                    xmldoc = minidom.parse(infilename)
                    eopfilename = xmldoc.getElementsByTagName('eop:identifier')[0].firstChild.data
                    acquisition = xmldoc.getElementsByTagName('eop:acquisitionDate')[0].firstChild.data
                    sid=xmldoc.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                    bands=xmldoc.getElementsByTagName("ps:numBands")[0].firstChild.data
                    platform=xmldoc.getElementsByTagName("eop:shortName")[0].firstChild.data
                    sattype=xmldoc.getElementsByTagName("eop:shortName")[1].firstChild.data
                    cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                    psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                    psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                    psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                    psaz=xmldoc.getElementsByTagName("ps:azimuthAngle")[0].firstChild.data
                    pssca=xmldoc.getElementsByTagName("ps:spaceCraftViewAngle")[0].firstChild.data
                    print ('ID_Name:', eopfilename.split('.')[0])
                    print ('Acquisition Date:', acquisition.split('T')[0])
                    print("Acquisition Date:", acquisition.split("T")[0])
                    print("Satellite Type:", platform)
                    print("ShortName:", sattype)
                    print("Number of Bands:", bands)
                    print("Cloud Cover:", format(float(cloud),'.2f'))
                    print("PS Incidence Angle",format(float(psia),'.4f'))
                    print("PS illumination azimuth angle",format(float(psilaz),'.2f'))
                    print("PS illumination elevation angle",format(float(psilelv),'.2f'))
                    print("PS Azimuth angle",format(float(psaz),'.2f'))
                    print("PS SpaceCraft angle",format(float(pssca),'.4f'))
                    date_time = acquisition.split('T')[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000
                    with open(mfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([fsp,epoch,platform,sattype,str(sid),bands,format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),
                        format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f')])
                    csvfile.close()
                except Exception as e:
                    print(infilename)
                    print(e)
                    with open(errorlog,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([infilename])
                    csvfile.close()
        elif asset == 'PS3B_V': #PS 3 Band Scene Derivative Visual
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "satType","satID", "numBands", "cloudcover","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                infilename = os.path.join(folder, filename)
                fsp = filename.split('_x')[0]
                try:
                    xmldoc = minidom.parse(infilename)
                    eopfilename = xmldoc.getElementsByTagName('eop:identifier')[0].firstChild.data
                    acquisition = xmldoc.getElementsByTagName('eop:acquisitionDate')[0].firstChild.data
                    bands=xmldoc.getElementsByTagName("ps:numBands")[0].firstChild.data
                    platform=xmldoc.getElementsByTagName("eop:shortName")[0].firstChild.data
                    sid=xmldoc.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                    sattype=xmldoc.getElementsByTagName("eop:shortName")[1].firstChild.data
                    cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                    psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                    psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                    psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                    psaz=xmldoc.getElementsByTagName("ps:azimuthAngle")[0].firstChild.data
                    pssca=xmldoc.getElementsByTagName("ps:spaceCraftViewAngle")[0].firstChild.data
                    print ('ID_Name:', eopfilename.split('.')[0])
                    print ('Acquisition Date:', acquisition.split('T')[0])
                    print("Acquisition Date:", acquisition.split("T")[0])
                    print("Satellite Type:", platform)
                    print("ShortName:", sattype)
                    print("Number of Bands:", bands)
                    print("Cloud Cover:", format(float(cloud),'.2f'))
                    print("PS Incidence Angle",format(float(psia),'.4f'))
                    print("PS illumination azimuth angle",format(float(psilaz),'.2f'))
                    print("PS illumination elevation angle",format(float(psilelv),'.2f'))
                    print("PS Azimuth angle",format(float(psaz),'.2f'))
                    print("PS SpaceCraft angle",format(float(pssca),'.4f'))
                    date_time = acquisition.split('T')[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000
                    print ('epoch time', epoch)
                    with open(mfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([fsp,epoch,platform,sattype,str(sid),bands,format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),
                        format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f')])
                    csvfile.close()
                except Exception as e:
                    print(infilename)
                    print(e)
                    with open(errorlog,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([infilename])
                    csvfile.close()               
        elif asset == 'REO':
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "satID", "tileID", "numBands", "cloudcover","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle","rsf"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                print(filename)
                infilename = os.path.join(folder,filename)
                fsp=filename.split("_x")[0]
                try:
                    xmldoc=minidom.parse(infilename)
                    re=xmldoc.getElementsByTagName("re:EarthObservationMetaData")[0]
                    eopfilename=xmldoc.getElementsByTagName("eop:identifier")[0].firstChild.data
                    product=xmldoc.getElementsByTagName("re:EarthObservationResult")[0]
                    bands=product.getElementsByTagName("re:numBands")[0].firstChild.data
                    downlink=xmldoc.getElementsByTagName("eop:downlinkedTo")[0]
                    acquisition= downlink.getElementsByTagName("eop:acquisitionDate")[0].firstChild.data
                    tile=xmldoc.getElementsByTagName("re:tileId")[0].firstChild.data
                    equip=xmldoc.getElementsByTagName("eop:EarthObservationEquipment")[0]
                    platform=equip.getElementsByTagName("eop:shortName")[0].firstChild.data
                    sid=equip.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                    cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                    date_time = acquisition.split("T")[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern)))*1000
                    psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                    psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                    psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                    psaz=xmldoc.getElementsByTagName("re:azimuthAngle")[0].firstChild.data
                    pssca=xmldoc.getElementsByTagName("re:spaceCraftViewAngle")[0].firstChild.data
                    psrad=xmldoc.getElementsByTagName("re:radiometricScaleFactor")[0].firstChild.data
                    print("ID_Name:", eopfilename.split(".")[0])
                    print("Acquisition Date:", acquisition.split("T")[0])
                    print("Satellite Type:", str(platform))
                    print("Satellite ID:", str(sid))
                    print("Tile ID:", tile)
                    print("Number of Bands:", bands)
                    print("Cloud Cover:", format(float(cloud),'.2f'))
                    print("Epoch Time:",epoch)
                    print("RE Incidence Angle",format(float(psia),'.4f'))
                    print("RE illumination azimuth angle",format(float(psilaz),'.2f'))
                    print("RE illumination elevation angle",format(float(psilelv),'.2f'))
                    print("RE Azimuth angle",format(float(psaz),'.2f'))
                    print("RE SpaceCraft angle",format(float(pssca),'.4f'))
                    print("Radiometric Scale Factor", format(float(psrad),'.18f'))
                    with open(mfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([fsp,epoch,str(platform),str(sid),tile,bands,format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f'),format(float(psrad),'.18f')])
                    csvfile.close()
                except Exception as e:
                    print(infilename)
                    print(e)
                    with open(errorlog,'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([infilename])
                    csvfile.close()
        elif asset == 'REO_V':
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "satID", "tileID", "numBands", "cloudcover","incAngle","illAzAngle","illElvAngle","azAngle","spcAngle","rsf"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                print(filename)
                infilename = os.path.join(folder,filename)
                fsp=filename.split("_x")[0]
                try:
                    xmldoc=minidom.parse(infilename)
                    eopfilename=xmldoc.getElementsByTagName("eop:identifier")[0].firstChild.data
                    bands=xmldoc.getElementsByTagName("re:numBands")[0].firstChild.data
                    acquisition= xmldoc.getElementsByTagName("eop:acquisitionDate")[0].firstChild.data
                    tile=xmldoc.getElementsByTagName("re:tileId")[0].firstChild.data
                    equip=xmldoc.getElementsByTagName("eop:EarthObservationEquipment")[0]
                    platform=equip.getElementsByTagName("eop:shortName")[0].firstChild.data
                    sid=equip.getElementsByTagName("eop:serialIdentifier")[0].firstChild.data
                    cloud=xmldoc.getElementsByTagName("opt:cloudCoverPercentage")[0].firstChild.data
                    date_time = acquisition.split("T")[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern)))*1000
                    psia=xmldoc.getElementsByTagName("eop:incidenceAngle")[0].firstChild.data
                    psilaz=xmldoc.getElementsByTagName("opt:illuminationAzimuthAngle")[0].firstChild.data
                    psilelv=xmldoc.getElementsByTagName("opt:illuminationElevationAngle")[0].firstChild.data
                    psaz=xmldoc.getElementsByTagName("re:azimuthAngle")[0].firstChild.data
                    pssca=xmldoc.getElementsByTagName("re:spaceCraftViewAngle")[0].firstChild.data
                    psrad=xmldoc.getElementsByTagName("re:radiometricScaleFactor")[0].firstChild.data
                    print("ID_Name:", eopfilename.split(".")[0])
                    print("Acquisition Date:", acquisition.split("T")[0])
                    print("Satellite Type:", str(platform))
                    print("Satellite ID:", str(sid))
                    print("Tile ID:", tile)
                    print("Number of Bands:", bands)
                    print("Cloud Cover:", format(float(cloud),'.2f'))
                    print("Epoch Time:",epoch)
                    print("RE Incidence Angle",format(float(psia),'.4f'))
                    print("RE illumination azimuth angle",format(float(psilaz),'.2f'))
                    print("RE illumination elevation angle",format(float(psilelv),'.2f'))
                    print("RE Azimuth angle",format(float(psaz),'.2f'))
                    print("RE SpaceCraft angle",format(float(pssca),'.4f'))
                    print("Radiometric Scale Factor", format(float(psrad),'.18f'))
                    with open(mfile,'a') as csvfile:
                        writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                        writer.writerow([fsp,epoch,str(platform),str(sid),tile,bands,format(float(cloud),'.2f'),format(float(psia),'.4f'),format(float(psilaz),'.2f'),format(float(psilelv),'.2f'),format(float(psaz),'.2f'),format(float(pssca),'.4f'),format(float(psrad),'.18f')])
                    csvfile.close()
                except Exception as e:
                    print(infilename)
                    print(e)
                    with open(errorlog,'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([infilename])
                    csvfile.close()
        elif asset == 'DGMS':
            folder = mf
            with open(mfile, 'wb') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['id_no', 'satName', 'prodID', 'catID', 'satID', 'stripID', 'numBands', 'cloudcover', 'system:time_start', 'sunaz', 'sunelv', 'sataz', 'satelv', 'absfB1', 'absfB2',
                 'absfB3', 'absfB4', 'absfB5', 'absfB6', 'absfB7', 'absfB8', 'effbwB1', 'effbwB2', 'effbwB3', 'effbwB4', 'effbwB5', 'effbwB6', 'effbwB7', 'effbwB8'], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                print filename
                infilename = os.path.join(folder, filename)
                fsp = filename.split('.')[0]
                try:
                    xmldoc = minidom.parse(infilename)
                    pid = xmldoc.getElementsByTagName('PRODUCTORDERID')[0].firstChild.data
                    cid = xmldoc.getElementsByTagName('PRODUCTCATALOGID')[0].firstChild.data
                    satid = xmldoc.getElementsByTagName('SATID')[0].firstChild.data
                    stripid = xmldoc.getElementsByTagName('STRIPID')[0].firstChild.data
                    acquisition = xmldoc.getElementsByTagName('STARTTIME')[0].firstChild.data
                    cloud = xmldoc.getElementsByTagName('CLOUDCOVER')[0].firstChild.data
                    sunaz = xmldoc.getElementsByTagName('MEANSUNAZ')[0].firstChild.data
                    sunelv = xmldoc.getElementsByTagName('MEANSUNEL')[0].firstChild.data
                    sataz = xmldoc.getElementsByTagName('MEANSATAZ')[0].firstChild.data
                    satelv = xmldoc.getElementsByTagName('MEANSATEL')[0].firstChild.data
                    satelv = xmldoc.getElementsByTagName('MEANOFFNADIRVIEWANGLE')[0].firstChild.data
                    date_time = acquisition.split('T')[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000
                    if satid == 'QB02':
                        satname = 'QuickBird'
                        bands = 4
                        absfb1 = xmldoc.getElementsByTagName('ABSCALFACTOR')[0].firstChild.data
                        absfb2 = xmldoc.getElementsByTagName('ABSCALFACTOR')[1].firstChild.data
                        absfb3 = xmldoc.getElementsByTagName('ABSCALFACTOR')[2].firstChild.data
                        absfb4 = xmldoc.getElementsByTagName('ABSCALFACTOR')[3].firstChild.data
                        absfb5 = 0
                        absfb6 = 0
                        absfb7 = 0
                        absfb8 = 0
                        effbwb1 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[0].firstChild.data
                        effbwb2 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[1].firstChild.data
                        effbwb3 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[2].firstChild.data
                        effbwb4 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[3].firstChild.data
                        effbwb5 = 0
                        effbwb6 = 0
                        effbwb7 = 0
                        effbwb8 = 0
                    elif satid == 'GE01':
                        satname = 'Geoeye'
                        bands = 4
                        absfb1 = xmldoc.getElementsByTagName('ABSCALFACTOR')[0].firstChild.data
                        absfb2 = xmldoc.getElementsByTagName('ABSCALFACTOR')[1].firstChild.data
                        absfb3 = xmldoc.getElementsByTagName('ABSCALFACTOR')[2].firstChild.data
                        absfb4 = xmldoc.getElementsByTagName('ABSCALFACTOR')[3].firstChild.data
                        absfb5 = 0
                        absfb6 = 0
                        absfb7 = 0
                        absfb8 = 0
                        effbwb1 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[0].firstChild.data
                        effbwb2 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[1].firstChild.data
                        effbwb3 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[2].firstChild.data
                        effbwb4 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[3].firstChild.data
                        effbwb5 = 0
                        effbwb6 = 0
                        effbwb7 = 0
                        effbwb8 = 0
                    elif satid == 'WV02':
                        satname = 'WorldView-2'
                        bands = 8
                        absfb1 = xmldoc.getElementsByTagName('ABSCALFACTOR')[0].firstChild.data
                        absfb2 = xmldoc.getElementsByTagName('ABSCALFACTOR')[1].firstChild.data
                        absfb3 = xmldoc.getElementsByTagName('ABSCALFACTOR')[2].firstChild.data
                        absfb4 = xmldoc.getElementsByTagName('ABSCALFACTOR')[3].firstChild.data
                        absfb5 = xmldoc.getElementsByTagName('ABSCALFACTOR')[4].firstChild.data
                        absfb6 = xmldoc.getElementsByTagName('ABSCALFACTOR')[5].firstChild.data
                        absfb7 = xmldoc.getElementsByTagName('ABSCALFACTOR')[6].firstChild.data
                        absfb8 = xmldoc.getElementsByTagName('ABSCALFACTOR')[7].firstChild.data
                        effbwb1 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[0].firstChild.data
                        effbwb2 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[1].firstChild.data
                        effbwb3 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[2].firstChild.data
                        effbwb4 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[3].firstChild.data
                        effbwb5 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[4].firstChild.data
                        effbwb6 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[5].firstChild.data
                        effbwb7 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[6].firstChild.data
                        effbwb8 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[7].firstChild.data
                    else:
                        satname = 'WorldView-3'
                        bands = 8
                        absfb1 = xmldoc.getElementsByTagName('ABSCALFACTOR')[0].firstChild.data
                        absfb2 = xmldoc.getElementsByTagName('ABSCALFACTOR')[1].firstChild.data
                        absfb3 = xmldoc.getElementsByTagName('ABSCALFACTOR')[2].firstChild.data
                        absfb4 = xmldoc.getElementsByTagName('ABSCALFACTOR')[3].firstChild.data
                        absfb5 = xmldoc.getElementsByTagName('ABSCALFACTOR')[4].firstChild.data
                        absfb6 = xmldoc.getElementsByTagName('ABSCALFACTOR')[5].firstChild.data
                        absfb7 = xmldoc.getElementsByTagName('ABSCALFACTOR')[6].firstChild.data
                        absfb8 = xmldoc.getElementsByTagName('ABSCALFACTOR')[7].firstChild.data
                        effbwb1 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[0].firstChild.data
                        effbwb2 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[1].firstChild.data
                        effbwb3 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[2].firstChild.data
                        effbwb4 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[3].firstChild.data
                        effbwb5 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[4].firstChild.data
                        effbwb6 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[5].firstChild.data
                        effbwb7 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[6].firstChild.data
                        effbwb8 = xmldoc.getElementsByTagName('EFFECTIVEBANDWIDTH')[7].firstChild.data
                    print (
                     'ID_Name:', fsp)
                    print ('Satellite Name:', satname)
                    print ('Acquisition Date:', acquisition.split('T')[0])
                    print ('Product Order ID:', str(pid))
                    print ('Product Catalog ID:', str(cid))
                    print ('Satellite ID:', str(satid))
                    print ('Strip ID:', stripid)
                    print ('Number of Bands:', bands)
                    print ('Cloud Cover:', cloud[:4])
                    print ('Epoch Time:', epoch)
                    print ('Abscal Factor', absfb1)
                    print ('Abscal Factor', absfb2)
                    print ('Abscal Factor', absfb3)
                    print ('Abscal Factor', absfb4)
                    print ('Eff Bandwith', effbwb1)
                    print ('Eff Bandwith', effbwb2)
                    print ('Eff Bandwith', effbwb3)
                    print ('Eff Bandwith', effbwb4)
                    print ('Sun Elevation', format(float(sunelv), '.2f'))
                    print ('Sun Azimuth', format(float(sunaz), '.2f'))
                    print ('Sat Elevation', format(float(satelv), '.2f'))
                    print ('Sat Azimuth', format(float(sataz), '.2f'))
                    with open(mfile, 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
                        writer.writerow([fsp, satname, pid, cid, satid, stripid, bands, format(float(cloud), '.2f'), epoch, format(float(sunaz), '.2f'), format(float(sunelv), '.2f'),
                         format(float(sataz), '.2f'), format(float(satelv), '.2f'), format(float(absfb1), '.6f'), format(float(absfb2), '.6f'), format(float(absfb3), '.6f'), format(float(absfb4), '.6f'),
                         format(float(absfb5), '.6f'), format(float(absfb6), '.6f'), format(float(absfb7), '.6f'), format(float(absfb8), '.6f'), format(float(effbwb1), '.6f'), format(float(effbwb2), '.6f'),
                         format(float(effbwb3), '.6f'), format(float(effbwb4), '.6f'), format(float(effbwb5), '.6f'), format(float(effbwb6), '.6f'), format(float(effbwb7), '.6f'), format(float(effbwb8), '.6f')])
                    csvfile.close()
                except Exception as e:
                    print infilename
                    print(e)
                    with open(errorlog, 'wb') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([infilename])
                    csvfile.close()
        elif asset == 'DGP':
            folder = mf
            with open(mfile, 'wb') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['id_no', 'satName', 'prodID', 'catID', 'satID', 'stripID', 'numBands', 'cloudcover', 'system:time_start'], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                print filename
                infilename = os.path.join(folder, filename)
                fsp = filename.split('.')[0]
                try:
                    xmldoc = minidom.parse(infilename)
                    pid = xmldoc.getElementsByTagName('PRODUCTORDERID')[0].firstChild.data
                    cid = xmldoc.getElementsByTagName('PRODUCTCATALOGID')[0].firstChild.data
                    satid = xmldoc.getElementsByTagName('SATID')[0].firstChild.data
                    stripid = xmldoc.getElementsByTagName('STRIPID')[0].firstChild.data
                    acquisition = xmldoc.getElementsByTagName('STARTTIME')[0].firstChild.data
                    cloud = xmldoc.getElementsByTagName('CLOUDCOVER')[0].firstChild.data
                    date_time = acquisition.split('T')[0]
                    pattern = '%Y-%m-%d'
                    epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000
                    if satid == 'QB02':
                        satname = 'QuickBird'
                    elif satid == 'GE01':
                        satname = 'Geoeye'
                    elif satid == 'WV02':
                        satname = 'WorldView-2'
                    else:
                        satname = 'WorldView-3'
                    if satid == 'QB02':
                        bands = 1
                    elif satid == 'GE01':
                        bands = 1
                    elif satid == 'WV02':
                        bands = 1
                    else:
                        bands = 1
                    print (
                     'ID_Name:', fsp)
                    print ('Satellite Name:', satname)
                    print ('Acquisition Date:', acquisition.split('T')[0])
                    print ('Product Order ID:', str(pid))
                    print ('Product Catalog ID:', str(cid))
                    print ('Satellite ID:', str(satid))
                    print ('Strip ID:', stripid)
                    print ('Number of Bands:', bands)
                    print ('Cloud Cover:', cloud[:4])
                    print ('Epoch Time:', epoch)
                    with open(mfile, 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
                        writer.writerow([fsp, satname, pid, cid, satid, stripid, bands, cloud[:4], epoch])
                    csvfile.close()
                except Exception as e:
                    print infilename
                    print(e)
                    with open(errorlog, 'wb') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([infilename])
                    csvfile.close()
        elif asset == 'PGCDEM': #PS OrthoTile Analytic Derivative DN
            folder = mf
            with open(mfile,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no", "system:time_start", "platform", "catId1","catId2", "noDataValue", "releaseVersion", "srcImg1","srcImg2","setsmVersion","resolution","bitdepth","acqDate","minelv","maxelv","units"], delimiter=',')
                writer.writeheader()
            with open(errorlog,'wb') as csvfile:
                writer=csv.DictWriter(csvfile,fieldnames=["id_no"], delimiter=',')
                writer.writeheader()
            for filename in os.listdir(folder):
                infilename = os.path.join(folder, filename)
                fsp = infilename#.split('_x')[0]
                with open(fsp,'r') as myfile:
                    a=myfile.readlines()
                    try:
                        demid=str(a).split('stripDemId = "')[1].split('v2.0";')[0]+"v20_dem"
                        platform=str(a).split('platform = "')[1].split('";')[0]
                        catId1 = str(a).split('catId1 = "')[1].split('";')[0]
                        catId2 = str(a).split('catId2 = "')[1].split('";')[0]
                        noDataValue = str(a).split('noDataValue = ')[1].split(';')[0]
                        date_time = str(a).split('stripCreationTime = ')[1].split('T')[0]
                        rls=str(a).split('releaseVersion = "')[1].split('";')[0]
                        sim=str(a).split('sourceImage1 = "')[1].split('";')[0]
                        sim2=str(a).split('sourceImage2 = "')[1].split('";')[0]
                        setv=str(a).split('setsmVersion = ')[1].split(';')[0]
                        rs=str(a).split('outputResolution = ')[1].split(';')[0]
                        bp=str(a).split('bitsPerPixel = ')[1].split(';')[0]
                        acq=str(a).split('acqDate = ')[1].split(';')[0]
                        minelv=str(a).split('minElevValue = ')[1].split(';')[0]
                        maxelv=str(a).split('maxElevValue = ')[1].split(';')[0]
                        units=str(a).split('horizontalCoordSysUnits = "')[1].split('";')[0]
                        pattern = '%Y-%m-%d'
                        epoch = int(time.mktime(time.strptime(date_time, pattern)))*1000
                        acqtime=int(time.mktime(time.strptime(acq, pattern)))*1000
                        print("DEM ID",demid)
                        print("Platform",platform)
                        print("Acquisition Time",acqtime)
                        print("Strip Creation Time",epoch)
                        print('CatID1',catId1)
                        print('CatID2',catId2)
                        print("noDataValue",noDataValue)
                        print("Release Version",rls)
                        print("SourceImage 1",sim)
                        print('SourceImage 2',sim2)
                        print('SETSM Version',setv)
                        print("BitsPerPixel",bp)
                        print("Unit",units)
                        print("Minimum Elevation",format(float(minelv),'.2f'))
                        print("Maximum Elevation",format(float(maxelv),'.2f'))
                        print("Output Resolution",format(float(rs),'.2f'))
                        with open(mfile,'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([demid,epoch,platform,catId1,catId2,noDataValue,rls,sim,sim2,setv,format(float(rs),'.2f'),bp,acqtime,format(float(minelv),'.2f'),format(float(maxelv),'.2f'),units])
                        csvfile.close()
                    except Exception as e:
                        print(infilename)
                        print(e)
                        with open(errorlog,'a') as csvfile:
                            writer=csv.writer(csvfile,delimiter=',',lineterminator='\n')
                            writer.writerow([infilename])
                        csvfile.close()
    else: #PS 4 Band Scene Derivative DN
        folder = mf
        indir=directory
        mfile=mfile
        errorlog=errorlog
        try:
            subprocess.call("python sr_metadata.py PSR --indir "+'"'+indir+'" --mfile '+'"'+mfile+'" --folder '+'"'+folder+'" --errorlog '+'"'+errorlog+'"',shell=True)
        except Exception as e:
            print(e)
