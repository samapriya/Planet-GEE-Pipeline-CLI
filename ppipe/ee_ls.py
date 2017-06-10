import ee
import ee.mapclient
import subprocess
import csv
import os

##initialize earth engine
ee.Initialize()

def lst(location, typ=None, items=None,f=None):
    if items > 0:
        if typ=='print':
            for line in subprocess.check_output("earthengine ls"+" "+'"'+location+'"'+" --max_items "+str(items),shell=True).split('\n'):
                print(line.replace(location,'').strip("/"))
        elif typ =='report':
            os.system("earthengine ls"+" "+location+" --max_items "+str(items)+" >>"+f+"filelist.txt")
    else:
        if typ=='print':
            for line in subprocess.check_output(["earthengine ls"+" "+location],shell=True).split('\n'):
                print(line.replace(location,'').strip("/"))
        elif typ =='report':
            os.system("earthengine ls"+" "+location+" >>"+f+"filelist.txt")
