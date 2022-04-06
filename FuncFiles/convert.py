import os
from FuncFiles.BSLevelFuncs import *
import librosa
from tensorflow import abs, signal
import shutil
import json

def convert_new():
    all_p = os.listdir("Pure")
    file = open("InfoFiles/converted.txt", "r")
    cnv = [row.strip() for row in file]
    file.close()
    no_new = True
    i = 0
    while (no_new and (i < len(all_p))):
        new = True
        for c in cnv:
            if c == all_p[i]:
                new = False
        if new:
            no_new = False
        else:
            i += 1
    if no_new:
        print("No more to convert")
        return False
    converting = all_p[i]
    print("Start converting " + converting)

    fillConverted(converting)

    file = open("InfoFiles/converted.txt", "a")
    file.write(converting + "\n")
    file.close()
    print("Converted " + converting)
    return True


def fillConverted(converting, save = True):
    all_c = os.listdir("Converted")
    place = str(len(all_c) + 1)


    egg_fpath = "Converted/" + place + "/song"
    cat_level_fpath = "Converted/" + place + "/CatLevel.txt"
    text_level_fpath = "Converted/" + place + "/TextLevel.txt"
    token_level_fpath = "Converted/" + place + "/TokenLevel.txt"
    beat_fpath = "Converted/" + place + "/beat.txt"
    info_fpath = "Converted/" + place + "/info.txt"

    egg_path = "Pure/" + converting + "/song.egg"
    norm_path = "Pure/" + converting + "/Normal.dat"
    info_path = "Pure/" + converting + "/info.dat"

    file = open(info_path, 'r')
    dic = file.read()
    dic.replace('\n', ' ')
    info = eval(dic)
    beat = info["_beatsPerMinute"]
    file.close()
    mult = 100
    min_sr = 6000 # минимальное количество элементов в 1 бит
    # меньше 60 bpm нафиг
    if (int(beat) < (min_sr/mult)):
        print("Слишком короткий бит ("+str(int(beat))+")"+" Номер: "+converting)
        return (0, 0)
    else:

        #print("Converted beat")

        l_curr = BSLevel()
        l_curr.readFromFile(norm_path, is_beat=True, beat=beat)
        cat_level = l_curr.getCatNotesVer3(proportion=(1.0 / 12.0), is_beat=True, beat=beat)
        text_level = l_curr.getTextNotes(proportion=(1.0 / 12.0), is_beat=True, beat=beat)
        #l_curr_1 = BSLevel()
        #l_curr_1.readFromTextMass(proportion=(1.0 / 12.0), nts=text_level)
        #text_level_1 = l_curr_1.getTextNotes(proportion=(1.0 / 12.0), is_beat=True, beat=beat)
        #cat_level_1 = l_curr_1.getCatNotesVer3(proportion=(1.0 / 12.0), is_beat=True, beat=beat)
        #print("Converted level")

        #y, sr = librosa.load(egg_path)
        #tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        y, sr = librosa.load(egg_path, sr=int(beat * mult))

        furie = abs(signal.stft(y, frame_length=int(60*mult), frame_step=int(60*mult), pad_end=True))
        np_song = furie.numpy()
        new_level = cat_level.reshape((cat_level.shape[0],
                                       cat_level.shape[1] * cat_level.shape[2] * cat_level.shape[3]))
        if save:
            os.mkdir("Converted/" + place)
            file = open(beat_fpath, "w")
            file.write(str(60.0 / beat))
            file.close()
            file = open(info_fpath, "w")
            file.write(converting)
            file.close()
            new_level = new_level.astype("float16")
            np.savetxt(cat_level_fpath, new_level, fmt='%.0e')
            np_song = np_song.astype("float16")
            np.save(egg_fpath, np_song)
            file = open(text_level_fpath, "w")
            file.write(text_level)
            file.close()

        return new_level, np_song, text_level#, text_level_1) ,(l_curr, l_curr_1), (cat_level, cat_level_1)



def fastConvert(converting, unzipping, curr_file, save = True):




    egg_path = "Converted/" + converting[0] + "/song.egg"
    info_path = "Converted/" + converting[0] + "/info.dat"

    bad_info = True
    beat = 1
    try:
        file = open(info_path, 'r')
        dic = file.read()
        dic = json.loads(dic)
        #dic.replace('\n', ' ')
        #dic.replace('false', 'False')
        #dic.replace('true', 'True')
        #info = eval(dic)
        info = dic
        beat = info["_beatsPerMinute"]
        file.close()
        bad_info = False
    except Exception as e:
        print(e)
        file.close()
        bad_info = True
    #print("2.2")
    mult = 100
    min_sr = 6000 # минимальное количество элементов в 1 бит
    max_sr = 600000 # минимальное количество элементов в 1 бит
    # меньше 60 bpm нафиг
    if (int(beat) < (min_sr/mult)) or bad_info or (int(beat) > (max_sr/mult)):
        if bad_info:
            print("Проблемы с считыванием info.dat: " + unzipping)
        else:
            print("Слишком короткий или слишком длинный бит (" + str(int(beat)) + ")" + " Файл: " + unzipping)
        for i in range(len(converting)):
            shutil.rmtree("Converted/" + converting[i])
        return False
    else:
        unfound_corr_level = True
        #print("2.3")
        #print(egg_path)
        #print(int(beat * mult))
        y, sr = librosa.load(egg_path, sr=int(beat * mult))
        #print("2.3")
        # 60 / 24 - 2.5 за бит делаем 48 ударов
        furie = abs(signal.stft(y, frame_length=int(2.5 * mult), frame_step=int(2.5 * mult), pad_end=True))
        #print("2.3")
        np_song = furie.numpy()
        start_shape = np_song.shape
        np_song = np_song + 0.000001*np.random.uniform(low=-1, high=1, size=start_shape)
        if start_shape!=np_song.shape:
            print("Шумы плохо добавляются в песню")
        for i in range(len(converting)):
            norm_path = "Converted/" + converting[i] + "/Level.dat"
            egg_fpath = "Converted/" + converting[i] + "/song"
            text_level_fpath = "Converted/" + converting[i] + "/TextLevel.txt"
            beat_fpath = "Converted/" + converting[i] + "/SongInfo.txt"
            info_fpath = "Converted/" + converting[i] + "/info.txt"
            egg_path = "Converted/" + converting[i] + "/song.egg"
            info_path = "Converted/" + converting[i] + "/info.dat"

            correct_level = False
            l_curr = BSLevel()
            correct_level = l_curr.checkFile(norm_path)


            if correct_level:
                try:
                    l_curr.readFromFile(norm_path, is_beat=True, beat=beat)
                    cat_level = l_curr.getCatNotesVer3(proportion=(1.0 / 12.0), is_beat=True, beat=beat)
                    new_level = cat_level.reshape((cat_level.shape[0],
                                               cat_level.shape[1] * cat_level.shape[2] * cat_level.shape[3]))
                    text_level = l_curr.getTextNotes(proportion=(1.0 / 12.0), is_beat=True, beat=beat)
                    correct_level = l_curr.checkFile(norm_path)
                    unfound_corr_level = False
                except:
                    print("Ошибка в уровне(нет нот или они странные) из: " + unzipping)
                    print("Уровень: " + curr_file[i])
                    print("---")
                    correct_level = False
            else:
                print("Ошибка в уровне(нет нот) из: " + unzipping)
                print("Уровень: "+curr_file[i])
                print("---")

            if save and correct_level:

                file = open(beat_fpath, "w")
                num_beats = int(np_song.shape[0]/24.0)
                file.write(str(60.0 / beat)+" "+str(num_beats))
                file.close()
                file = open(info_fpath, "w", encoding="utf-8")
                file.write(unzipping+" "+curr_file[i])
                file.close()
                new_level = new_level.astype("float16")
                np_song = np_song.astype("float16")
                np.save(egg_fpath, np_song)
                file = open(text_level_fpath, "w")
                file.write(text_level)
                file.close()
            if save:
                os.remove(norm_path)
                os.remove(egg_path)
                os.remove(info_path)

        if unfound_corr_level:
            for i in range(len(converting)):
                shutil.rmtree("Converted/" + converting[i])
            return False
        else:
            return True#new_level, np_song, text_level#, text_level_1) ,(l_curr, l_curr_1), (cat_level, cat_level_1)


def convert_all():
    a = True
    num = 0
    while a:
        print(num)
        a = convert_new()
        if a:
            num += 1
    print("Totally converted " + str(num))


