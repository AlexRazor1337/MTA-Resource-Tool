import subprocess, os, sys, json, collections.abc
from datetime import datetime

ids = [1, 2, 3, 4]

config = {'manual': False,'info_level': 0, 'restricted_extensions': [], 'ignore_files': ["meta.xml", "meta-generated.xml"], 'author': "Default", 'cache': False, 'override': True, 'generate_exported': True}

def from_json(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def to_json(dict, filename):
    with open(filename, 'w') as fp:
        json.dump(dict, fp,  indent=4)


def check_linking_rule(name, rules):
    print(name)
    for item in rules:
        if name in rules[item]:
            print("INFO: FOUND RULE FOR", name)
            return item
    return None

def resolve_dependencies(queue, model):
    model_addition = {'world_objects': dict(), 'other': dict()}
    print(queue)
    print(model)
    while queue:
        cur = queue.pop(0)
        for item in model[cur[2]]:
            name, ext = os.path.splitext(item)
            print("CH", name, cur[1])
            if name == cur[1]:
                print("ADDING", model[cur[2]][item])
                prev_id = model[cur[2]][item]
                model_addition[cur[2]][item] = [prev_id, {cur[0]: ids.pop(0)}]
                continue
    return model_addition

def dict_merge(dct, merge_dct):
    for k, v in iter(merge_dct.items()):
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.abc.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

def verifyFiles(filename, check_col):
    is_dff = os.path.isfile(working_folder + "\\" + filename + ".dff")
    is_txd = os.path.isfile(working_folder + "\\" + filename + ".txd")
    if check_col:
        is_col = os.path.isfile(working_folder + "\\" + filename + ".col")
    else:
        is_col = True
    return is_dff and is_txd and is_col


models_data = dict(world_objects = dict(), other = dict())
dependency_queue = list()
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
            linking_rules = from_json(working_folder + "\\linking-rules.json")
        models_data = from_json(working_folder + "\\assigment-model.json")
        for root, dirs, files in os.walk(working_folder):
            folders = root.split("\\")
            if not folders[-1].startswith('.'): #ignoring .git and etc. basically
                for file in files:
                    file_path = os.path.join(root, file)
                    file_path = file_path.replace(working_folder + os.sep, "")

                    file_path_writable = file_path.replace(os.sep, "/").replace(".dff", "")
                    name, ext = os.path.splitext(file)
                    if ext == ".dff":
                        if "skins" in file_path and not file_path_writable in models_data['other']:
                            if check_linking_rule(file_path, linking_rules):
                                print('rule1')
                                dependency_queue.append((file_path_writable, check_linking_rule(file_path, linking_rules), "others"))
                            elif verifyFiles(file_path.replace(".dff", ""), False):
                                models_data['other'][file_path_writable] = ids.pop(0)
                            else:
                                print("WARNING: NOT FOUND VALID SET OF FILES FOR SKIN:", file_path)
                        elif not file_path_writable in models_data['world_objects']:
                            if check_linking_rule(file_path, linking_rules):
                                print('rule2')
                                dependency_queue.append((file_path_writable, check_linking_rule(file_path, linking_rules), "world_objects"))
                            elif verifyFiles(file_path.replace(".dff", ""), True):
                                models_data['world_objects'][file_path_writable] = ids.pop(0)
                            else:
                                print("WARNING: NOT FOUND VALID SET OF FILES FOR WORLD OBJECT:", file_path)

        model_addition = resolve_dependencies(dependency_queue, models_data)
        print("INFO: Saving assigment model")
        print(models_data)
        print(model_addition)
        dict_merge(models_data, model_addition)
        to_json(models_data, "assigment-model2.json")
    else:
        print("INFO: No assigment model specified, generating new one!")
        linking_rules = {}
        if os.path.isfile(working_folder + "\\linking-rules.json"):
            print("INFO: Loading linking rules!")
            linking_rules = from_json(working_folder + "\\linking-rules.json")
        for root, dirs, files in os.walk(working_folder):
            folders = root.split("\\")
            if not folders[-1].startswith('.'): #ignoring .git and etc. basically
                for file in files:
                    file_path = os.path.join(root, file)
                    file_path = file_path.replace(working_folder + os.sep, "")

                    file_path_writable = file_path.replace(os.sep, "/").replace(".dff", "")
                    name, ext = os.path.splitext(file)
                    if ext == ".dff":
                        if "skins" in file_path:
                            if check_linking_rule(file_path, linking_rules):
                                print('rule1')
                                dependency_queue.append((file_path_writable, check_linking_rule(file_path, linking_rules), "others"))
                            elif verifyFiles(file_path.replace(".dff", ""), False):
                                models_data['other'][file_path_writable] = ids.pop(0)
                            else:
                                print("WARNING: NOT FOUND VALID SET OF FILES FOR SKIN:", file_path)
                        else:
                            if check_linking_rule(file_path, linking_rules):
                                print('rule2')
                                dependency_queue.append((file_path_writable, check_linking_rule(file_path, linking_rules), "world_objects"))
                            elif verifyFiles(file_path.replace(".dff", ""), True):
                                models_data['world_objects'][file_path_writable] = ids.pop(0)
                            else:
                                print("WARNING: NOT FOUND VALID SET OF FILES FOR WORLD OBJECT:", file_path)
        model_addition = resolve_dependencies(dependency_queue, models_data)
        print("INFO: Saving assigment model")
        print(models_data)
        print(model_addition)
        dict_merge(models_data, model_addition)
        to_json(models_data, "assigment-model.json")
            
else:
    sys.exit("ERROR: No file or directory specified!")