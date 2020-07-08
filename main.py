import subprocess, os, sys, json
from datetime import datetime
from shutil import copyfile

#info levels: 0 - detailed info, 1 - default info, 2 - warnings, 3 - errors
default_config = {'obfuscation_level': 'e3','info_level': 1, 'restricted_extensions': []}
possible_obfuscation_levels = ["e", "e2", "e3"]
config = {}

def init_settings():
    try:
        with open('settings.json', 'r') as f:
            config = json.load(f)
    except IOError:
        with open('settings.json', 'w+') as f:
            json.dump(default_config, f)
            config = default_config
    if not config['obfuscation_level'] in possible_obfuscation_levels:
        print("ERROR: Inappropriate obfuscation level, settings will be reset.")
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
            print(file_path)
            print("WARNING: File with this name already exists, compiling to", file_basename, "instead!")
    arguments = ["-" + config['obfuscation_level'], " -o " + file_basename + "c"," -- ", file_path]
    subprocess.call([working_dir + "\luac_mta.exe", arguments])

if len(sys.argv) > 1:
    working_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(working_dir)
    config = init_settings()
    if os.path.isfile(sys.argv[1]):
        file_basename = os.path.basename(sys.argv[1])
        if config['info_level'] < 2:
            print("INFO: Working with single file, compiling to ", file_basename, "c")
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
        for dirPath, dirs, files in os.walk(sys.argv[1]): #main cycle, walks through everything in root folder
            current_dir = dirPath.replace(sys.argv[1], "")
            check_dirs = [d for d in current_dir.split("\\") if d.startswith(".")]
            if check_dirs:
                continue

            if current_dir != "":
                os.chdir(working_dir + os.sep + "Compiled Resources" + os.sep + resource_name + os.sep + current_dir)
            else:
                os.chdir(working_dir + os.sep + "Compiled Resources" + os.sep + resource_name)
            for dir in dirs:
                if not dir.startswith('.'): #ignoring .git and etc. basically
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
        
        os.chdir(working_dir + "\Compiled Resources\\" + "\\" + resource_name)
        if os.path.isfile("meta.xml"):
            with open("meta.xml", "r+") as meta_file:
                file_lines = meta_file.readlines()
                meta_file.seek(0)
                for line in file_lines:
                    if not ".luac" in line:
                        line = line.replace(".lua", ".luac", -1)
                    meta_file.write(line)
                meta_file.truncate()       
        else:
            if config['info_level'] < 3:
                print("WARNING: No meta file was found in the resource directory!")
    if config['info_level'] < 2:
        print("INFO: Compiled successfully.")
else:
    sys.exit("ERROR: No file or directory specified!")