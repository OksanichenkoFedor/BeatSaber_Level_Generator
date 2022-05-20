import os
import shutil
import zipfile
from FuncFiles.convert import fastConvert
import FuncFiles.config as config
from FuncFiles.support_funcs import fprint

def find_new_to_unzip(zip_folder):
    fprint("Find new files to unzip")
    all_z = os.listdir(zip_folder)
    file = open("../Data/InfoFiles/unzipped.txt", "r")
    un_z = [row.strip() for row in file]
    file.close()
    file = open("../Data/InfoFiles/badzipped.txt", "r")
    b_z = [row.strip() for row in file]
    un_z = un_z + b_z
    file.close()
    no_new = True
    i = 0
    while (no_new and (i < len(all_z))):
        new = True
        if all_z[i] in un_z:
            new = False
        if new:
            if all_z[i][-4:] == ".zip":
                no_new = False
            else:
                print("Не архив: " + all_z[i])
                os.remove(zip_folder + "/" + all_z[i])
                i += 1
        else:
            i += 1
    if no_new:
        fprint("No more to unzip")
        curr_downloads = os.listdir("../Data/Downloads")
        fprint("In downloads now " + str(len(curr_downloads)) + " files")
        print("No more to unzip")
        return False
    unzipping = all_z[i]
    try:
        fprint("Found: "+str(all_z[i]))
    except:
        fprint("Can't print file name")
    return unzipping


def unzip_new(zip_folder="../Data/Zipped", verbose=0, frame=None, logger=None):
    unzipping = find_new_to_unzip(zip_folder)
    if unzipping == False:
        return False
    try:
        frame.song_name_lbl["text"] = unzipping
    except:
        pass
    config.conv_logs["song name"] = unzipping

    print("Start unzipping " + unzipping)
    fprint("Start unzipping " + unzipping)
    # проверяем наличие всего

    frame.curr_act_lbl["text"] = "Checking before unzip"
    config.conv_logs["current operation"] = "Checking before unzip"

    files = checking(unzipping, zip_folder)
    if files == -1:
        file = open("../Data/InfoFiles/badzipped.txt", "a")
        try:
            file.write(unzipping + "\n")
        except:
            pass
        file.close()
        fprint("Problems with files")
        return False
    fprint("Files found")
    egg = files[0]
    norm = files[1]
    info = files[2]

    frame.curr_act_lbl["text"] = "Unzipping"
    config.conv_logs["current operation"] = "Unzipping"

    res = fillToConvert(files, unzipping, zip_folder, verbose, frame=frame)

    if res:

        file = open("../Data/InfoFiles/unzipped.txt", "a", encoding="utf-8")
        file.write(unzipping + "\n")
        file.close()
        path = zip_folder + "/" + unzipping
        os.remove(path)
        logger.info["unzipped"]["good"]["num"] += 1
        logger.info["unzipped"]["good"]["arr"].append(unzipping)
    else:
        path = unzipping
        file = open("../Data/InfoFiles/badzipped.txt", "a", encoding="utf-8")
        file.write(path + "\n")
        file.close()
        path = zip_folder + "/" + unzipping
        file_destination = "../Data/BadZipped"
        shutil.move(path, file_destination)
        config.bad_zipped += 1
        logger.info["unzipped"]["bad"]["num"] += 1
        logger.info["unzipped"]["bad"]["arr"].append(unzipping)
        try:
            frame.song_name_lbl["text"] = unzipping
        except:
            pass
        frame.bad_z_lbl["text"] = "Количество плохих песен: " + str(config.bad_zipped)

    return True


def checking(unzipping, zip_folder):
    zf = zipfile.ZipFile(zip_folder + "/" + unzipping)
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
        fprint("Error: no .egg, file: " + unzipping)
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
                    if (not (file.filename.endswith("awless.dat"))) and (not (file.filename.endswith("egree.dat"))) and \
                            (not (file.filename.endswith("rrows.dat"))) and \
                            (not (file.filename.endswith("Single Saber.dat"))) and \
                            (not (file.filename.endswith("OneSaber.dat"))):
                        # print(file.filename)
                        # print(unzipping)
                        pass
                    else:
                        norm_uf = False
                        norm.append(file.filename)
                        fprint("New level: " + str(file.filename))


    if norm_uf:
        print("--------------")
        print("Error: no acceptable level")
        print("File: " + unzipping)
        fprint("No acceptable level, file: " + unzipping)
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
        fprint("No info.dat, file: " + unzipping)
        print("--------------")
        return -1

    return egg, norm, info


def fillPure(files, unzipping, zip_folder):
    egg, norm, info = files
    zf = zipfile.ZipFile(zip_folder + "/" + unzipping)

    all_p = os.listdir("../Data/Converted")
    place = str(len(all_p) + 1)
    os.mkdir("../Data/Converted/" + place)

    zf.extract(egg, "../Data/Converted/" + place)
    os.rename("../Data/Converted/" + place + "/" + egg, "../Data/Converted/" + place + "/song.egg")

    zf.extract(norm, "../Data/Converted/" + place)
    os.rename("../Data/Converted/" + place + "/" + norm, "../Data/Converted/" + place + "/Level.dat")

    zf.extract(info, "../Data/Pure/" + place)
    os.rename("../Data/Converted/" + place + "/" + info, "../Data/Converted/" + place + "/info.dat")


def fillToConvert(files, unzipping, zip_folder, verbose=0, frame=None):
    egg, norms, info = files
    zf = zipfile.ZipFile(zip_folder + "/" + unzipping)
    places = []
    fprint("Make place in Converted")
    for i in range(len(norms)):
        all_p = os.listdir("../Data/Converted")
        place = str(len(all_p) + 1)
        if verbose == 1:
            print(place)
        fprint(place)
        os.mkdir("../Data/Converted/" + place)

        zf.extract(egg, "../Data/Converted/" + place)
        os.rename("../Data/Converted/" + place + "/" + egg, "../Data/Converted/" + place + "/song.egg")

        zf.extract(norms[i], "../Data/Converted/" + place)
        os.rename("../Data/Converted/" + place + "/" + norms[i], "../Data/Converted/" + place + "/Level.dat")

        zf.extract(info, "../Data/Converted/" + place)
        os.rename("../Data/Converted/" + place + "/" + info, "../Data/Converted/" + place + "/info.dat")
        places.append(place)

    frame.curr_act_lbl["text"] = "Converting"
    config.conv_logs["current operation"] = "Converting"

    return fastConvert(places, unzipping, norms, frame=frame)


def unzip_all():
    a = True
    num = 0
    while a:
        print(num)
        a = unzip_new()
        if a:
            num += 1
    print("Totally unzipped " + str(num))
