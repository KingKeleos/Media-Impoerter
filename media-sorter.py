import os, shutil, sys, time, string
from pickle import NONE
from genericpath import isdir
from lib2to3.pytree import Base
from os.path import isfile, join, isdir
from ctypes import windll
from tracemalloc import stop

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

imageFormat = [".RAW",".raw",".RW2",".rw2",".JPG",".jpg"]
videoFormat= [".MP4",".mp4",".mov",".MOV"]

print("|--- Media Importer Dokomi ---|\n\n")
print("Select folder to copy from:\n")
if sys.platform=='win32':
    BaseDir=get_drives()
    for d in BaseDir:
        print(d)
src_dir=NONE

print("Select drive to copy from:")
drive=input("->")+":\\"

print("\n\n\n|-- Found following directories: --|")
for root, dirs, files in os.walk(drive):
    for n in dirs:
        if "." in n or "." in root:
            continue
        print(os.path.join(root,n))

while not isdir(src_dir):
    src_dir=input("->")
    print("Directory %s chosen." % src_dir)
    print("Copies files from folder:\n")
    count=0
    if not isdir(src_dir):
        print("Not a correct Directory, try again or 'exit':")
        stop=input()
        if not stop=="exit":
            continue
        else:
            sys.exit()
    for f in os.listdir(src_dir):
        if isfile(join(src_dir,f)):
            time_code=time.ctime(os.path.getmtime(os.path.join(src_dir,f)))[0:10]
            if f[-4:-1]+f[-1] in imageFormat:
                if not isdir(sys.path[0]+"/Images"):
                    os.mkdir(sys.path[0]+"/Images")
                    print("created Directory for images under "+sys.path[0]+"/Images")
                if not isdir(os.path.join(sys.path[0],"Images",time_code)):
                    os.mkdir(os.path.join(sys.path[0],"Images",time_code))
                if not f in os.listdir(os.path.join(sys.path[0],"Images",time_code)):
                    print("Image %s found | importing..." %f)
                    shutil.copy2(os.path.join(src_dir,f),os.path.join(sys.path[0],"Images",time_code))
                    print("Successfuly imported Image %s into %s" %(f,os.path.join(sys.path[0],"Images",time_code)))
                    count+=1
                else:
                    print("! - Image: %s already imported" % f)
            elif f[-4:-1]+f[-1] in videoFormat:
                if not isdir(os.path.join(sys.path[0],"Videos")):
                    os.mkdir(os.path.join(sys.path[0],"Videos"))
                    print("created Directory for videos under "+sys.path[0]+"/Videos")
                if not isdir(os.path.join(sys.path[0],"Videos",time_code)):
                    os.mkdir(os.path.join(sys.path[0],"Videos",time_code))
                if not f in os.listdir(os.path.join(sys.path[0],"Videos",time_code)):
                    print("Video %s found | importing..." %f)
                    shutil.copy2(os.path.join(src_dir,f),os.path.join(sys.path[0],"Videos",time_code))
                    print("Successfuly imported Video %s into %s" %(f,os.path.join(sys.path[0],"Videos",time_code)))
                    count+=1
                else:
                    print("! - Video %s already imported" %f)
        else:
            print("!----| No files found, ending |---!")


print("!--- Done! Copied: %d Files ---!" % count)
