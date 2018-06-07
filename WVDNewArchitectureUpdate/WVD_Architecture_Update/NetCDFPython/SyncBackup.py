import subprocess
import datetime
import os
import shutil
import SharedPythonFunctions as SPF

def DoRSync(syncFrom, syncTo,WarningFile,ErrorFile):
    try:
        subprocess.call(["C:\\Users\\h2odial\\Documents\\MobaXterm\\slash\\bin\\rsync", "-avz", "--compress-level=9", syncFrom, syncTo])
    except:
        writeString = "WARNING: unable to RSync to external hard drive - "+str(NowTime) + '\n' + str(sys.exc_info()[0]) + '\n\n'
        SPF.Write2ErrorFile(WarningFile, writeString)

    # Everything below this can be deleted when we get RSync working
    # some of the imports above can also be deleted. 
    """
    LocalOutputPath = syncFrom

    #copy NetCDF files to external drive if applicable.
    copyFiles = True
    #copyFiles = False
    if copyFiles:
        print ("Copying files", datetime.datetime.utcnow().strftime("%H:%M:%S"))
        OutputPath = LocalOutputPath

        if os.path.isdir(syncTo):
            #ensure output directory exists
            OutputPath = os.path.join(syncTo,"Data","")
            SPF.ensure_dir(OutputPath)
        else:
            writeString = "WARNING: argument 2 (path to external hard drive to copy data onto) - "+syncTo+" - is not a valid directory to write to. Writing to local data directory instead. - "+str(NowTime) + '\n'
            Write2ErrorFile(ErrorFile, writeString)
            
        if LocalOutputPath != OutputPath:
            #recursive_overwrite(LocalOutputPath,OutputPath,ignore=None)
            data_dirs_list = os.listdir(LocalOutputPath)
            #print (data_dirs_list)
            for data_dir in data_dirs_list:
                print ("Copying ",data_dir, datetime.datetime.utcnow().strftime("%H:%M:%S"))
                if os.path.isfile(os.path.join(LocalOutputPath,data_dir)):
                    shutil.copy(os.path.join(LocalOutputPath,data_dir), os.path.join(OutputPath,data_dir))
                else:
                    day_dirs_list = os.listdir(os.path.join(LocalOutputPath,data_dir))
                    for day_dir in day_dirs_list:
                        if os.path.isfile(day_dir):
                            shutil.copy(os.path.join(LocalOutputPath,data_dir,day_dir), os.path.join(OutputPath,data_dir,day_dir))
                        else:
                            if day_dir >= ThenDate:
                                #print ("Copying day level ", day_dir, datetime.datetime.utcnow().strftime("%H:%M:%S"))
                                LocalCopyFrom = os.path.join(LocalOutputPath,data_dir,day_dir)
                                src_file_names = ""
                                if os.path.isfile(os.path.join(LocalOutputPath,data_dir,day_dir)):
                                    fromi = os.path.join(LocalCopyFrom,os.path.join(LocalOutputPath,data_dir,day_dir))
                                    toi = os.path.join(OutputPath,data_dir,day_dir)
                                    SPF.ensure_dir(os.path.join(OutputPath,data_dir,""))
                                    shutil.copy(fromi,toi)
                                else:
                                    src_file_names = os.listdir(os.path.join(LocalOutputPath,data_dir,day_dir))
                                SPF.ensure_dir(os.path.join(OutputPath,data_dir,day_dir,""))
                                for file_name in src_file_names:
                                    if (os.path.isfile(os.path.join(LocalCopyFrom,file_name))):
                                        fromt = os.path.join(LocalCopyFrom,file_name)
                                        tot = os.path.join(OutputPath,data_dir,day_dir,"")
                                        shutil.copy(fromt,tot)
    """
