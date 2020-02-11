#!/usr/bin/env python
#################################################################
# Python Script to retrieve 1336 online Data files of 'ds083.2',
# total 30.26G. This script uses 'requests' to download data.
#
# Highlight this script by Select All, Copy and Paste it into a file;
# make the file executable and run it on command line.
#
# You need pass in your password as a parameter to execute
# this script; or you can set an environment variable RDAPSWD
# if your Operating System supports it.
#
# Contact rpconroy@ucar.edu (Riley Conroy) for further assistance.
#################################################################


import sys, os
import requests

def check_file_status(filepath, filesize):
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size/filesize)*100
    sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
    sys.stdout.flush()

# Try to get password  程序读取密码有错误
# if len(sys.argv) < 2 and not 'RDAPSWD' in os.environ:
#     try:
#         import getpass
#         input = getpass.getpass
#     except:
#         try:
#             input = raw_input
#         except:
#             pass
#     pswd = input('Password:lj7619087')
# else:
#     try:
#         pswd = sys.argv[1]
#     except:
#         pswd = os.environ['RDAPSWD']

url = 'https://rda.ucar.edu/cgi-bin/login'
values = {'email' : 'xxxx@xxx', 'passwd' : 'xxxxx', 'action' : 'login'} # xxx where you need edit
# Authenticate
ret = requests.post(url,data=values)
if ret.status_code != 200:
    print('Bad Authentication')
    print(ret.text)
    sys.exit()
dspath = 'https://rda.ucar.edu/data/ds083.2/'
filelist = [
'grib2/2019/2019.02/fnl_20190201_00_00.grib2',
'grib2/2019/2019.02/fnl_20190201_06_00.grib2',
'grib2/2019/2019.02/fnl_20190201_12_00.grib2',
'grib2/2019/2019.02/fnl_20190201_18_00.grib2',
'grib2/2019/2019.02/fnl_20190202_00_00.grib2',
'grib2/2019/2019.02/fnl_20190202_06_00.grib2',
'grib2/2019/2019.02/fnl_20190202_12_00.grib2',
'grib2/2019/2019.02/fnl_20190202_18_00.grib2',
'grib2/2019/2019.02/fnl_20190203_00_00.grib2']
for file in filelist:
    filename=dspath+file
    file_base = os.path.basename(file)
    print('Downloading',file_base)
    req = requests.get(filename, cookies = ret.cookies, allow_redirects=True, stream=True)
    filesize = int(req.headers['Content-length'])
    with open(file_base, 'wb') as outfile:
        chunk_size=1048576
        for chunk in req.iter_content(chunk_size=chunk_size):
            outfile.write(chunk)
            if chunk_size < filesize:
                check_file_status(file_base, filesize)
    check_file_status(file_base, filesize)
    print()
