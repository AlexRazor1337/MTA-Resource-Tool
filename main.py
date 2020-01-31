import subprocess, os, sys

working_dir = os.path.dirname(os.path.realpath(__file__))
arguments = ["-e3", " -o " + os.path.basename(sys.argv[1]) + "c"," -- ", sys.argv[1]]
subprocess.call([working_dir + "\luac_mta.exe", arguments])