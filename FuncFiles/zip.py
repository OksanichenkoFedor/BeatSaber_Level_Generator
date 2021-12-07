import zipfile
import os

def zip_one(pure_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as myzip:
        os.walk(pure_path+"/")
        myzip.write("Info.dat")
        myzip.write("Normal.dat")
        myzip.write("song.ogg")
