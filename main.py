import subprocess, os, sys
from datetime import datetime
from shutil import copyfile

def compile_file(file_path):
    file_basename = os.path.basename(file_path)
    if os.path.isfile(file_basename + "c"):
        file_basename = str(datetime.now().time()).replace(":", ".", -1) + file_basename
        print("File with this name already exists, compiling to " + file_basename + " instead")
    arguments = ["-e3", " -o " + file_basename + "c"," -- ", file_path]
    subprocess.call([working_dir + "\luac_mta.exe", arguments])

if len(sys.argv) > 1:
    working_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(working_dir)
    if os.path.isfile(sys.argv[1]):
        file_basename = os.path.basename(sys.argv[1])
        print("Working with single file, compiling to " + file_basename + "c")
        compile_file(sys.argv[1])
    elif os.path.isdir(sys.argv[1]):
        
        if not os.path.exists("Compiled Resources"):
            os.mkdir("Compiled Resources")
        os.chdir("Compiled Resources")

        resource_name = os.path.basename(sys.argv[1])
        if not os.path.exists(resource_name):
            os.mkdir(resource_name)
        else:
            resource_name += " " + str(datetime.now().time()).replace(":", ".", -1) #adds time to folder name to handle name dublicates
            os.mkdir(resource_name)
        os.chdir(resource_name)
        print("Working with folder, compiling to", resource_name)
        for dirPath, dirs, files in os.walk(sys.argv[1]): #walks through everything in root folder
            for dir in dirs:
                if not dir.startswith('.'): #ignoring .git and etc. basically
                    dir_path = dirPath.replace(sys.argv[1], "")
                    if dir_path != "": #check if it is not in the root folder
                        folders = dir_path.split("\\")
                        os.chdir(folders[-1])
                    os.mkdir(dir)

                    for file in files:
                        name, ext = os.path.splitext(file)
                        if ext == ".lua":
                            compile_file(dirPath + "\\" + file)
                        else:
                            copyfile(dirPath + "\\" + file, file)

            if len(dirs) == 0: #when there are no folders inside another folder, it can't iterate through it, so previsios cycle won't run
                dir_path = dirPath.replace(sys.argv[1], "")
                folders = dir_path.split("\\")
                if not folders[-1].startswith('.'):
                    if dir_path != "":
                        os.chdir(folders[-1])
                    for file in files:
                        name, ext = os.path.splitext(file)
                        if ext == ".lua":
                            compile_file(dirPath + "\\" + file)
                        else:
                            copyfile(dirPath + "\\" + file, file)
        
        os.chdir(working_dir + "\Compiled Resources\\" + "\\" + resource_name)
        if os.path.isfile("meta.xml"):
            with open("meta.xml", "r+") as meta_file:
                file_string = meta_file.read()
                meta_file.seek(0)
                file_string = file_string.replace(".lua", ".luac", -1)
                meta_file.write(file_string)
                meta_file.truncate()            
        else:
            print("WARNING: No meta file was found in the resource directory!")
else:
    sys.exit("No file or directory specified.")