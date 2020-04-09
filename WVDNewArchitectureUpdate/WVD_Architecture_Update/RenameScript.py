import os, subprocess

FileTypes = ['Etalonsample','HKeepsample','Humidity','LLsample','MCSsample','Powsample','UPSsample','WSsample']
FilesDesired = ['Etalon','HKeep','Humidity','LL','MCS','Power','UPS','WS']
MPD  = '01'
Date = '20200409' 

#FileTypes = [(String + '_' + MPD + '_' + '20200409' + '_' ) for String in FilesDesired]
FilesDesired = [(String + '_' + MPD + '_' + Date + '_' ) for String in FilesDesired]

Path = os.path.join(os.getcwd(),'Data','NetCDFOutput',Date)

SubFiles = os.listdir(Path)

for FileDesired, FileType in zip(FilesDesired,FileTypes):
    for File in SubFiles:
        if File[:len(FileType)] == FileType:
            cmd = 'mv ' + os.path.join(Path,File) + ' ' + os.path.join(Path,FileDesired) + File[len(FileType):]
            print(cmd)
            retcode = subprocess.call(cmd,shell=True)




