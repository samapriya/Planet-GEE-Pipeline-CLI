import os
import csv
import getpass
print("Enter your Planet API Key")
password=getpass.getpass()
with open('./pkey.csv','w') as completed:
    writer=csv.writer(completed,delimiter=',',lineterminator='\n')
    writer.writerow([password])
