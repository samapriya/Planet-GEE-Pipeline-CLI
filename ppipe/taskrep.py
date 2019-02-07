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
import datetime
import csv

ee.Initialize()

def genreport(report):
    with open(report,'wb') as failed:
        writer=csv.DictWriter(failed,fieldnames=["Task ID","Task Type", "Task Description","Creation","Start","End","Time to Start","Time to End","Output State"],delimiter=',')
        writer.writeheader()
    status=ee.data.getTaskList()
    for items in status:
        ttype=items['task_type']
        tdesc=items['description']
        tstate=items['state']
        tid=items['id']
        try:
            tcreate=datetime.datetime.fromtimestamp(items['creation_timestamp_ms']/1000).strftime('%c')
            tstart=datetime.datetime.fromtimestamp(items['start_timestamp_ms']/1000).strftime('%c')
            tupdate=datetime.datetime.fromtimestamp(items['update_timestamp_ms']/1000).strftime('%c')
            tdiffstart=items['start_timestamp_ms']/1000-items['creation_timestamp_ms']/1000
            tdiffend=items['update_timestamp_ms']/1000-items['start_timestamp_ms']/1000
            #print(ttype,tdesc,tstate,tid,tcreate,tstart,tupdate,tdiffstart,tdiffend)
            with open(report,'a') as tasks:
                writer=csv.writer(tasks,delimiter=',',lineterminator='\n')
                writer.writerow([tid,ttype,tdesc,str(tcreate),str(tstart),str(tupdate),str(tdiffstart),str(tdiffend),tstate])
        except Exception as e:
            pass
    print('Report exported to '+str(report))
#genreport(report=r'C:\planet_demo\taskrep.csv')
