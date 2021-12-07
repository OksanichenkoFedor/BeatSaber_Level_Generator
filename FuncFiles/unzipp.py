import os
import zipfile
from FuncFiles.convert import fastConvert


def unzip_new():
    all_z = os.listdir("Zipped")
    file = open("InfoFiles/unzipped.txt", "r")
    un_z = [row.strip() for row in file]
    file.close()
    file = open("InfoFiles/badzipped.txt", "r")
    b_z = [row.strip() for row in file]
    un_z = un_z + b_z
    file.close()
    no_new = True
    i = 0
    while (no_new and (i < len(all_z))):
        new = True
        for z in un_z:
            if z == all_z[i]:
                new = False
        if new:
            no_new = False
        else:
            i += 1
    if no_new:
        print("No more to unzip")
        return False
    unzipping = all_z[i]
    print("Start unzipping " + unzipping)
    # проверяем наличие всего

    files = checking(unzipping)

    if files == -1:
        file = open("InfoFiles/badzipped.txt", "a")
        file.write(unzipping + "\n")
        file.close()
        return False
    egg = files[0]
    norm = files[1]
    info = files[2]
    files1 = (egg, norm[0], info)
    #fillPure(files, unzipping)

    res = fillToConvert(files, unzipping)
    if res:
        file = open("InfoFiles/unzipped.txt", "a")
        file.write(unzipping + "\n")
        file.close()
    else:
        file = open("InfoFiles/badzipped.txt", "a")
        file.write(unzipping + "\n")
        file.close()
    #print("Unzipped " + unzipping)
    return True


def checking(unzipping):
    zf = zipfile.ZipFile("Zipped/" + unzipping)
    l = zf.infolist()
    egg_uf = True
    egg = ""
    for file in l:
        if file.filename.endswith(".egg"):
            egg_uf = False
            egg = file.filename
    if egg_uf:
        print("--------------")
        print("Error: no .egg")
        print("File: " + unzipping)
        print("--------------")
        return -1

    norm_uf = True
    correct_files = ['ExpertStandard.dat', 'EasyStandard.dat', 'NormalStandard.dat', 'HardStandard.dat',
                     'ExpertPlusStandard.dat', "Expert.dat", "Hard.dat", "Normal.dat", "ExpertPlus.dat", "Easy.dat"]
    incorrect_files = ['ExpertLightshow.dat', 'ExpertPlusLightshow.dat', "Info.dat", 'info.dat', "Lightshow.dat"]
    norm = []
    for file in l:
        if file.filename.endswith(".dat") and (not (file.filename.endswith("ightshow.dat"))) and (
                not (file.filename.endswith("nfo.dat"))):
            if file.filename in correct_files:
                norm_uf = False
                norm.append(file.filename)
            else:
                if file.filename in incorrect_files:
                    pass
                else:
                    if (not (file.filename.endswith("awless.dat"))) and (not (file.filename.endswith("egree.dat"))) and\
                            (not (file.filename.endswith("rrows.dat"))) and \
                            (not (file.filename.endswith("Single Saber.dat"))) and \
                            (not (file.filename.endswith("OneSaber.dat"))):
                        #print(file.filename)
                        #print(unzipping)
                        pass
                    else:
                        norm_uf = False
                        norm.append(file.filename)

    if norm_uf:
        print("--------------")
        print("Error: no Normal level")
        print("File: " + unzipping)
        print("--------------")
        return -1

    info_uf = True
    info = ""
    for file in l:
        if file.filename.endswith("nfo.dat"):
            info_uf = False
            info = file.filename
    if info_uf:
        print("--------------")
        print("Error: no info.dat")
        print("File: " + unzipping)
        print("--------------")
        return -1

    return egg, norm, info


def fillPure(files, unzipping):
    egg, norm, info = files
    zf = zipfile.ZipFile("Zipped/" + unzipping)

    all_p = os.listdir("Converted")
    place = str(len(all_p) + 1)
    os.mkdir("Converted/" + place)

    zf.extract(egg, "Converted/" + place)
    os.rename("Converted/" + place + "/" + egg, "Converted/" + place + "/song.egg")

    zf.extract(norm, "Converted/" + place)
    os.rename("Converted/" + place + "/" + norm, "Converted/" + place + "/Level.dat")

    zf.extract(info, "Pure/" + place)
    os.rename("Converted/" + place + "/" + info, "Converted/" + place + "/info.dat")


def fillToConvert(files, unzipping):
    egg, norms, info = files
    zf = zipfile.ZipFile("Zipped/" + unzipping)
    places = []
    for i in range(len(norms)):
        all_p = os.listdir("Converted")
        place = str(len(all_p) + 1)
        print(place)
        os.mkdir("Converted/" + place)

        zf.extract(egg, "Converted/" + place)
        os.rename("Converted/" + place + "/" + egg, "Converted/" + place + "/song.egg")

        zf.extract(norms[i], "Converted/" + place)
        os.rename("Converted/" + place + "/" + norms[i], "Converted/" + place + "/Level.dat")

        zf.extract(info, "Converted/" + place)
        os.rename("Converted/" + place + "/" + info, "Converted/" + place + "/info.dat")
        places.append(place)
    return fastConvert(places, unzipping, norms)


def unzip_all():
    a = True
    num = 0
    while a:
        print(num)
        a = unzip_new()
        if a:
            num += 1
    print("Totally unzipped " + str(num))
