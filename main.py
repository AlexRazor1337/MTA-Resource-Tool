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
            resource_name += " " + str(datetime.now().time()).replace(":", ".", -1)
            os.mkdir(resource_name)
        os.chdir(resource_name)

        dir_contaiments = os.listdir(sys.argv[1])
        for object in dir_contaiments:
            file_path = sys.argv[1] + "\\" + object

            if os.path.isfile(file_path):
                name, ext = os.path.splitext(object)
                print(name, ext)
                if ext == ".lua":
                    compile_file(file_path)
                else:
                    copyfile(file_path, object)
        if os.path.isfile("meta.xml"):
            with open("meta.xml", "r+") as meta_file:
                file_string = meta_file.read()
                meta_file.seek(0)
                file_string = file_string.replace(".lua", ".luac", -1)
                meta_file.write(file_string)
                meta_file.truncate()            
        else:
            print("WARNING: No meta file found in the resource directory!")
else:
    sys.exit("No file or directory specified.")