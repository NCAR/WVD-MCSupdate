import os, subprocess

FileTypes = ['Etalonsample','HKeepsample','Humidity','LLsample','MCSsample','Powsample','UPSsample','WSsample']
FilesDesired = ['Etalon_03_20200408_','HKeep_03_20200408_','Humidity_03_20200408_','LL_03_20200408_','MCS_03_20200408_',\
                'Power_03_20200408_','UPS_03_20200408_','WS_03_20200408_']

Path = os.path.join(os.getcwd(),'Data','NetCDFOutput','20200408')

SubFiles = os.listdir(Path)

for FileDesired, FileType in zip(FilesDesired,FileTypes):
    for File in SubFiles:
        if File[:len(FileType)] == FileType:
            cmd = 'mv ' + os.path.join(Path,File) + ' ' + os.path.join(Path,FileDesired) + File[len(FileType):]
            print(cmd)
            #retcode = subprocess.call(cmd,shell=True)




