import os
from FuncFiles.tokenizer import *
from FuncFiles.BSLevelFuncs import *


def pure_one(conv_path, pure_path):
    #os.mkdir("Converted/" + place)
    nts = np.loadtxt(conv_path+"/Normal.txt")
    print(nts.shape)
    #print(nts.shape)
    nts = nts.reshape((nts.shape[0], 4, 3, 37))
    print(nts.shape)
    #print(nts.shape)
    f = open(conv_path + "/beat.txt", 'r')
    beat = float(f.read())
    level = BSLevel()
    level.readFromCategoricMassМVer3(proportion=(1.0 / 12.0), nts=nts)
    level.writeLevel(pure_path+"/", "my_song", beat)
    file = open('FuncFiles/info.txt', 'r')
    lines = []
    s = file.readlines()
    print(s[6][:21])
    s[6] = s[6][:21] + str(60.0 / beat) + ",\n"
    print(s[6])
    #leveled["_beatsPerMinute"] = 60.0 / beat
    file.close()
    file = open(pure_path + "/Info.dat", "w")
    for line in s:
        file.write(line)
    file.close()
    #pure_path + "/"

def pure_from_tokens(conv_path, pure_path, token_folder):
    f = open(conv_path + "/TokenLevel.txt", 'r')
    curr = f.read()
    curr = curr.split(" ")
    curr = np.array(curr)
    nts = curr.astype("int")
    f.close()
    text_tokenizer = MultigrammTokenizer()
    text_tokenizer.load(token_folder)
    nts = text_tokenizer.detokenize(nts, string=True)
    # print(nts.shape)
    f = open(conv_path + "/beat.txt", 'r')
    beat = float(f.read())
    level = BSLevel()
    level.readFromTextMass(proportion=(1.0 / 12.0), nts=nts)
    level.writeLevel(pure_path + "/", "my_song", beat)
    file = open('FuncFiles/info.txt', 'r')
    lines = []
    s = file.readlines()
    #print(s[6][:21])
    s[6] = s[6][:21] + str(60.0 / beat) + ",\n"
    #print(s[6])
    # leveled["_beatsPerMinute"] = 60.0 / beat
    file.close()
    file = open(pure_path + "/Info.dat", "w")
    for line in s:
        file.write(line)
    file.close()


