import subprocess, os, sys, json
from datetime import datetime

ids = [1, 2, 3]

config = {'manual': False,'info_level': 0, 'restricted_extensions': [], 'ignore_files': ["meta.xml", "meta-generated.xml"], 'author': "Default", 'cache': False, 'override': True, 'generate_exported': True}

def read_json(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data

def to_json(dict, filename):
    with open(filename, 'w') as fp:
        json.dump(dict, fp,  indent=4)

models_data = dict(world_objects = dict(), other = dict())
if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    working_folder = sys.argv[1]
    if working_folder == ".":
        working_folder = os.path.dirname(os.path.realpath(__file__))
    
    os.chdir(working_folder)
    dff_count = 0
    for root, dirs, files in os.walk(working_folder):
        for file in files:
            if ".dff" in file:
                dff_count += 1
    if dff_count > len(ids):
        sys.exit("ERROR: Not enough free ID's to replace all models!")
    print("INFO: There are " + str(dff_count) + " unique dff models in all subfolders.")
    if os.path.isfile(working_folder + "\\assigment-model.json"):
        print("INFO: Loading assigment model!")
        if os.path.isfile(working_folder + "\\linking-rules.json"):
            print("INFO: Loading linking rules!")
            linking_rules = read_json(working_folder + "\\linking-rules.json")
    else:
        print("INFO: No assigment model specified, generating new one!")
        linking_rules = []
        if os.path.isfile(working_folder + "\\linking-rules.json"):
            print("INFO: Loading linking rules!")
            linking_rules = read_json(working_folder + "\\linking-rules.json")
        for root, dirs, files in os.walk(working_folder):
            folders = root.split("\\")
            if not folders[-1].startswith('.'): #ignoring .git and etc. basically
                for file in files:
                    file_path = os.path.join(root, file)
                    file_path = file_path.replace(working_folder + os.sep, "")
                    name, ext = os.path.splitext(file)
                    if ext == ".dff":
                        if "skins" in file_path:
                            models_data['other'][name] = ids.pop(0)
                        else:
                            models_data['world_objects'][name] = ids.pop(0)
        to_json(models_data, "assigment-model.json")
                    
            
else:
    sys.exit("ERROR: No file or directory specified!")