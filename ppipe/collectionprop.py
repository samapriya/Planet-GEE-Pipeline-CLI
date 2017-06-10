import argparse
import subprocess
import os,sys,time,csv,sys
import json,ee
from pprint import pprint

def collprop(imcoll,prop):
    tset=str("earthengine asset set "+'"'+imcoll+'"'+" --property "+'"'+str(prop)+'"')
    tinfo=str("earthengine asset info "+imcoll)
    assetset=subprocess.call(tset,shell=True)
    print("Asset Property Set")
    print("New Asset Info========>>>>>")
    for line in subprocess.check_output(tinfo,shell=True).split('\n'):
        print(line)
	
    
