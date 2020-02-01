import subprocess, os, sys, json
from datetime import datetime
from shutil import copyfile

default_config = {'obfuscation_level': 'e3','info_level': 1, 'restricted_extensions': []}
possible_obfuscation_levels = ["e", "e2", "e3"]
config = {}

def init_settings():
    try:
        with open('settings.json', 'r') as f:
            config = json.load(f)
            print(config)
    except IOError:
        with open('settings.json', 'w+') as f:
            json.dump(default_config, f)
            config = default_config
    if not config['obfuscation_level'] in possible_obfuscation_levels:
        print("WARNING: Inappropriate obfuscation level, settings will be reset.")
        os.remove('settings.json')
        config = default_config
    return config
    
def compile_file(file_path):
    file_basename = os.path.basename(file_path)
    if config['info_level'] == 0:
        print("INFO: Compiling", file_basename)
    if os.path.isfile(file_basename + "c"):
        file_basename = str(datetime.now().time()).replace(":", ".", -1) + file_basename
        if config['info_level'] < 3:
            print("WARNING: File with this name already exists, compiling to " + file_basename + " instead!")
    arguments = ["-" + config['obfuscation_level'], " -o " + file_basename + "c"," -- ", file_path]
    subprocess.call([working_dir + "\luac_mta.exe", arguments])

if len(sys.argv) > 1:
    working_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(working_dir)
    config = init_settings()
    if os.path.isfile(sys.argv[1]):
        file_basename = os.path.basename(sys.argv[1])
        if config['info_level'] < 2:
            print("INFO: Working with single file, compiling to " + file_basename + "c")
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
        if config['info_level'] < 2:
            print("INFO: Working with folder, compiling to", resource_name)
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
                            if not ext in config['restricted_extensions']:
                                copyfile(dirPath + "\\" + file, file)
                                if config['info_level'] == 0:
                                    print("INFO: Copying", file)
                            elif config['info_level'] == 0:
                                print("INFO: Not copying", file, "because it has restricted extension.")

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
                            if config['info_level'] == 0:
                                print("INFO: Copying", file)
        
        os.chdir(working_dir + "\Compiled Resources\\" + "\\" + resource_name)
        if os.path.isfile("meta.xml"):
            with open("meta.xml", "r+") as meta_file:
                file_string = meta_file.read()
                meta_file.seek(0)
                file_string = file_string.replace(".lua", ".luac", -1)
                meta_file.write(file_string)
                meta_file.truncate()       
        else:
            if config['info_level'] < 3:
                print("WARNING: No meta file was found in the resource directory!")
    if config['info_level'] < 2:
        print("INFO: Compiled successfully.")
else:
    sys.exit("ERROR: No file or directory specified!")