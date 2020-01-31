import subprocess, os, sys

if len(sys.argv) > 1:
    working_dir = os.path.dirname(os.path.realpath(__file__))
    if os.path.isfile(sys.argv[1]):
        file_basename = os.path.basename(sys.argv[1])
        print("Working with single file, compiling to " + file_basename + "c")
        arguments = ["-e3", " -o " + file_basename + "c"," -- ", sys.argv[1]]
    else:
        pass
    subprocess.call([working_dir + "\luac_mta.exe", arguments])
else:
    sys.exit("No file or directory specified.")