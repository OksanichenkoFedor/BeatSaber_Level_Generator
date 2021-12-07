from BSPM import info, level, events, notes, obstacles
import numpy as np


class BSLevel():
    """

    Class of game level
    :method readFromFile(): make level from file .dat
    :method readFromNumpy(): make level from several numpy tensors events, notes, obstacles (they can be empty) .dat
    :method writeFile(): write file to .dat
    :method eventsToNumpy(): Private method, which generate Numpy version of events massive
    :method notesToNumpy(): Private method, which generate Numpy version of notes massive
    :method obstaclesToNumpy(): Private method, which generate Numpy version of obstacles massive

    :field content: dict, which contains dict versions massives of ev, nt, ob
    :field events: Numpy version of massive events
    :field notes: Numpy version of massive notes
    :field obstacles: Numpy version of massive obstacles

    """

    def __init__(self):
        self.content = {}
        self.events = np.array([])
        self.notes = np.array([])
        self.obstacles = np.array([])
        self.is_filled = False

    def eventsToNumpy(self):
        """
        Make np array filled with every event, with shape (nm of events, 3)
        """
        if self.is_filled:
            res = []
            for ev in self.content["events"]:
                res.append([ev["_time"], ev["_type"], ev["_value"]])
            self.events = np.array(res)
        else:
            print("Error: Empty level")

    def notesToNumpy(self, is_beat=False, beat=None):
        """
        Make np array filled with every note, with shape (nm of notes, 5)
        """
        if self.is_filled:
            res = []
            for nt in self.content["notes"]:
                time = nt["_time"]
                time1 = time

                if is_beat:
                    qtime = 60.0/beat
                    time = int(time / qtime)
                    time = time*qtime
                    correct_note = False
                    if (nt["_type"] > 3) or (nt["_lineIndex"] > 3) or (nt["_lineLayer"] > 2) or (nt["_cutDirection"] > 8):
                        print("Новая нота (мы её не добавляем)")
                        print(nt)
                    else:
                        res.append([time, int(nt["_type"]), int(nt["_lineIndex"]), int(nt["_lineLayer"]),
                                int(nt["_cutDirection"])])
                else:
                    res.append([time1, int(nt["_type"]), int(nt["_lineIndex"]), int(nt["_lineLayer"]),
                                int(nt["_cutDirection"])])

            self.notes = np.array(res)
        else:
            print("Error: Empty level")

    def obstaclesToNumpy(self):
        """
        Make np array filled with every obstacle, with shape (nm of obstacles, 5)
        """
        if self.is_filled:
            res = []

            for ob in self.content["obstacles"]:
                res.append([ob["_time"], ob["_type"], ob["_lineIndex"], ob["_width"], ob["_duration"]])
            self.obstacles = np.array(res)
        else:
            print("Error: Empty level")

    def readFromFile(self, filename, is_beat=False, beat=None):
        """
            Return dict with massives of:
             1.) events: Contains massive of event: dict with "_time" "_type" "_value"
             2.) notes: Contains massive of notes: dist with "_time" "_type" "_lineIndex"(X) "_lineLayer"(Y)  "_cutDirection"
             3.) obstacles: Contains massive of obstacles: dist with "_time" "_type" "_lineIndex" "_width" "_duration"
            :param filename:
            :return:
            """
        file = open(filename, 'r')
        s = file.read()
        s = s.replace("true", "0")
        s = s.replace("null", "0")
        s = s.replace("false", "0")
        s.replace('\n', ' ')

        leveled = eval(s)
        events = leveled["_events"]
        notes = leveled["_notes"]
        obstacles = leveled["_obstacles"]
        self.content = {"events": events, "notes": notes, "obstacles": obstacles}
        self.is_filled = True
        self.eventsToNumpy()
        self.notesToNumpy(is_beat, beat)
        self.obstaclesToNumpy()

    def checkFile(self, filename):
        try:

            file = open(filename, 'r')
            s = file.read()
            file.close()
            s = s.replace("true", "0")
            s = s.replace("null", "0")
            s = s.replace("false", "0")
            s.replace('\n', ' ')
            leveled = eval(s)
            notes = leveled["_notes"]
            return len(notes) > 0
        except:
            return False

    def readFromNumpy(self, events=np.array([]), notes=np.array([]), obstacles=np.array([]), is_beat=False, beat=None):

        self.is_filled = True
        self.events = events
        self.notes = notes
        self.obstacles = obstacles
        ev_dict = []
        for i in range(events.shape[0]):
            ev_dict.append({"_time": events[i][0], "_type": int(events[i][1]), "_value": int(events[i][2])})

        nt_dict = []
        for i in range(notes.shape[0]):
            nt_dict.append({"_time": notes[i][0], "_type": int(notes[i][1]), "_lineIndex": int(notes[i][2]),
                            "_lineLayer": int(notes[i][3]), "_cutDirection": int(notes[i][4])})

        ob_dict = []
        for i in range(obstacles.shape[0]):
            ob_dict.append({"_time": obstacles[i][0], "_type": int(obstacles[i][1]), "_lineIndex": int(obstacles[i][2]),
                            "_width": int(obstacles[i][3]), "_duration": int(obstacles[i][4])})
        self.content = {"events": ev_dict, "notes": nt_dict, "obstacles": ob_dict}

    def readFromCategoricMassМVer1(self, proportion = 1, evs=None, nts=None, obs=None):
        if obs is None:
            obs = []
        if evs is None:
            evs = []
        if nts is None:
            nts = []
        np_ev = []
        # todo дописать для эвентов
        np_ev = np.array(np_ev)
        np_nt = []
        for j in range(len(nts)):
            nt = nts[j]
            is_note = 0
            for i in range(4,9):
                is_note+=nt[0][i]
            if is_note>0.5:
                # добавляем ноту
                type = 0
                for i in range(4):
                    type += nt[1][i]
                if type > 0.5:
                    type = 1
                else:
                    type = 0

                lineIndex = 0
                Ins = []
                for i in range(4):
                    Ins.append(0)
                Ins[0] = nt[2][0] + nt[2][1]
                Ins[1] = nt[2][2] + nt[2][3]
                Ins[2] = nt[2][4] + nt[2][5]
                Ins[3] = nt[2][6] + nt[2][7] + nt[2][8]
                max = Ins[0]
                for i in range(4):
                    if Ins[i]>max:
                        lineIndex = i
                        max = Ins[i]

                lineLayer = 0
                Lys = []
                for i in range(3):
                    Lys.append(0)
                Lys[0] = nt[3][0] + nt[3][1] + nt[3][2]
                Lys[1] = nt[3][3] + nt[3][4] + nt[3][5]
                Lys[2] = nt[3][6] + nt[3][7] + nt[3][8]
                max = Lys[0]
                for i in range(3):
                    if Lys[i] > max:
                        lineLayer = i
                        max = Lys[i]

                cutDirection = 0
                max = nt[4][0]
                for i in range(9):
                    if nt[4][i] > max:
                        max = nt[4][i]
                        cutDirection = i
                np_nt.append([proportion*j, type, lineIndex, lineLayer, cutDirection])

        np_nt = np.array(np_nt)

        np_ob = []
        # todo дописать для препятствий
        np_ob = np.array(np_ob)
        self.readFromNumpy(np_ev, np_nt, np_ob)

    def getCatNotesVer1(self, proportion=1):
        """

        :param proportion: Как сильно надо сжать время у нот
        :return:
        """
        res_mass = []

        note_ind = 0
        time = 0
        not_end = True
        while note_ind<len(self.notes):
            if self.notes[note_ind][0]>(time+1)*proportion:
                # нет ноты
                def_mass = [1, 0, 0, 0, 0, 0, 0, 0, 0]
                res_mass.append([def_mass, def_mass, def_mass, def_mass, def_mass])
                time+=1
            else:
                # есть нота

                note = []
                note.append([0, 0, 0, 0, 0, 1, 0, 0, 0])

                # type
                if self.notes[note_ind][1]==0:
                    note.append([1, 0, 0, 0, 0, 0, 0, 0, 0])
                else:
                    note.append([0, 0, 0, 0, 0, 1, 0, 0, 0])

                # lineIndex
                if self.notes[note_ind][2] == 0:
                    note.append([1, 0, 0, 0, 0, 0, 0, 0, 0])
                elif self.notes[note_ind][2] == 1:
                    note.append([0, 0, 1, 0, 0, 0, 0, 0, 0])
                elif self.notes[note_ind][2] == 2:
                    note.append([0, 0, 0, 0, 1, 0, 0, 0, 0])
                elif self.notes[note_ind][2] == 3:
                    note.append([0, 0, 0, 0, 0, 0, 1, 0, 0])

                # lineLayer
                if self.notes[note_ind][3] == 0:
                    note.append([1, 0, 0, 0, 0, 0, 0, 0, 0])
                elif self.notes[note_ind][3] == 1:
                    note.append([0, 0, 0, 1, 0, 0, 0, 0, 0])
                elif self.notes[note_ind][3] == 2:
                    note.append([0, 0, 0, 0, 0, 0, 1, 0, 0])

                # cutDirection
                curr_mass = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                curr_mass[int(self.notes[note_ind][4])] = 1
                note.append(curr_mass)

                res_mass.append(note)
                note_ind+=1
                time+=1

        return np.array(res_mass)

    def getCatEventsVer1(self):
        pass
        # todo написать генерацию категориального

    def getCatObstaclesVer1(self):
        pass

    def readFromCategoricMassМVer2(self, proportion=1, evs=None, nts=None, obs=None):
        """

                :param proportion: Как сильно надо сжать время у нот
                :return:
        """
        if obs is None:
            obs = []
        if evs is None:
            evs = []
        if nts is None:
            nts = []
        np_ev = []
        # todo дописать для эвентов
        np_ev = np.array(np_ev)
        np_nt = []
        for i in range(len(nts)):
            nt = nts[i]
            for type in range(4):
                for lineIndex in range(4):
                    for lineLayer in range(3):
                        cutDir = 0
                        for j in range(10):
                            if nt[type][lineIndex][lineLayer][j] > nt[type][lineIndex][lineLayer][cutDir]:
                                cutDir = j
                        if cutDir!=0:
                            np_nt.append([proportion * i, type, lineIndex, lineLayer, cutDir-1])

        np_nt = np.array(np_nt)

        np_ob = []
        # todo дописать для препятствий
        np_ob = np.array(np_ob)
        self.readFromNumpy(np_ev, np_nt, np_ob)

    def getCatNotesVer2(self, proportion=1):
        """

                :param proportion: Как сильно надо сжать время у нот
                :return:
        """
        res_mass = []

        note_ind = 0
        time = 0
        not_end = True
        fin_time = float(self.notes[-1][0]) / (proportion*1.0)
        while time <= fin_time:
            curr_mass = np.zeros((4, 4, 3, 10))
            while (self.notes[note_ind % self.notes.shape[0]][0] < (time+1)*proportion) and (note_ind<self.notes.shape[0]) and\
                    (self.notes[note_ind % self.notes.shape[0]][0] >= (time)*proportion):
                curr_mass[int(self.notes[note_ind][1])][int(self.notes[note_ind][2])][int(self.notes[note_ind][3])][int(self.notes[note_ind][4])+1] = 1
                note_ind+=1
            res_mass.append(curr_mass)

            time+=1
        return np.array(res_mass)

    def writeLevel(self, file_path, song_name, beat):
        if self.is_filled:
            OurLevel = level
            path = ""

            # events

            LevelEvents = events.events()

            for ev in self.content["events"]:
                LevelEvents.append(ev["_time"], ev["_type"], ev["_value"])

            OurLevel.events = LevelEvents.events

            # notes

            LevelNotes = notes.notes()

            for nt in self.content["notes"]:
                LevelNotes.append(nt["_time"], nt["_type"], nt["_lineIndex"], nt["_lineLayer"], nt["_cutDirection"])
            #LevelNotes.append(1.1, 0, 0, 0, 0)

            OurLevel.notes = LevelNotes.notes

            # obstacles

            LevelObstacles = obstacles.obstacles()

            for ob in self.content["obstacles"]:
                LevelObstacles.append(ob["_time"], ob["_type"], ob["_lineIndex"], ob["_width"], ob["_duration"])

            OurLevel.obstacles = LevelObstacles.obstacles

            OurLevel.write(file_path)
        else:
            print("Error: Empty level")

    def getCatNotesVer3(self, proportion=1, is_beat=False, beat=None):
        """

                :param proportion: Как сильно надо сжать время у нот
                :return:
        """
        res_mass = []

        note_ind = 0
        time = 0
        not_end = True
        fin_time = float(self.notes[-1][0]) / (proportion * 1.0)

        fin_time = float(self.notes[-1][0]) / (proportion * 1.0)
        if is_beat:
            qtime = (60.0 / beat) * proportion
            fin_time = int(float((self.notes[-1][0] + 0.000000001) / qtime) * qtime / (proportion * 1.0))
        while time <= fin_time:
            # default = np.array([1,0,0,0,0,0,0,0,0,0])
            curr_mass = np.zeros((4, 3, 37))
            for i2 in range(4):
                for i3 in range(3):
                    curr_mass[i2][i3][0] = 1
            while (self.notes[note_ind % self.notes.shape[0]][0] < (time + 1) * proportion) and (
                    note_ind < self.notes.shape[0]) and \
                    (self.notes[note_ind % self.notes.shape[0]][0] >= (time) * proportion):
                for i in range(37):
                    curr_mass[int(self.notes[note_ind][2])%4][int(self.notes[note_ind][3])%3][i] = 0
                curr_mass[int(self.notes[note_ind][2])%4][int(self.notes[note_ind][3])%3][
                    int(self.notes[note_ind][1]) * 9 + int(self.notes[note_ind][4]) + 1] = 1
                note_ind += 1
            res_mass.append(curr_mass)

            time += 1
        return np.array(res_mass)

    def getTextNotes(self, proportion=1, is_beat=False, beat=None):
        """

                        :param proportion: Как сильно надо сжать время у нот
                        :return:
                """
        res_mass = []

        note_ind = 0
        time = 0
        not_end = True

        fin_time = float(self.notes[-1][0]) / (proportion * 1.0)

        if is_beat:
            qtime = (60.0/beat)*proportion
            fin_time = int(float((self.notes[-1][0]+0.000000001)/qtime)*qtime / (proportion * 1.0))

        while time <= fin_time:

            while (self.notes[note_ind % self.notes.shape[0]][0] < (time + 1) * proportion) and (
                    note_ind < self.notes.shape[0]) and \
                    (self.notes[note_ind % self.notes.shape[0]][0] >= (time) * proportion):

                num = self.giveTextedNote(note_ind % self.notes.shape[0])
                if num <= 444:
                    res_mass.append(str(num))
                note_ind += 1
            #res_mass.append('0')
            if time % int(1.0/proportion) == 0:
                res_mass.append("-1")
                pass
            if time != fin_time:
                res_mass.append('0')
                pass

            time += 1

        return " ".join(res_mass)

    def giveTextedNote(self, ind):

        x = self.notes[ind][2] #4
        y = self.notes[ind][3] #3
        type = self.notes[ind][1]
        dir = self.notes[ind][4]
        num = int((1+4*9)*(3*x+y)+1+type*9+dir)

        if (num > 445) or (num<0):
            print("В нотах какая-то проблема с индексом(он слишком большой)")
            print(self.notes[ind])

        return num

    def giveNoteFromNum(self, num):
        note = {}
        num = int(num)-1
        full_type = (num%37)
        pos = num//37
        note["x"] = pos//3
        note["y"] = pos%3
        note["type"] = full_type//9
        note["cd"] = full_type%9
        return note

    def readFromCategoricMassМVer3(self, proportion, evs=None, nts=None, obs=None):
        """

                :param proportion: Как сильно надо сжать время у нот
                :return:
        """
        if obs is None:
            obs = []
        if evs is None:
            evs = []
        if nts is None:
            nts = []
        np_ev = []
        # todo дописать для эвентов
        np_ev = np.array(np_ev)
        np_nt = []
        for i in range(len(nts)):
            nt = nts[i]
            for lineIndex in range(4):
                for lineLayer in range(3):
                    cutDir = 0
                    for j in range(37):
                        if nt[lineIndex][lineLayer][j] >= nt[lineIndex][lineLayer][cutDir]:
                            cutDir = j
                    if cutDir != 0:
                        cutDir -= 1
                        print("ehhhf")
                        np_nt.append([proportion * i*1.0, cutDir / 9, lineIndex, lineLayer, cutDir % 9])


        np_nt = np.array(np_nt)
        np_ob = []
        # todo дописать для препятствий
        np_ob = np.array(np_ob)
        self.readFromNumpy(np_ev, np_nt, np_ob)

    def readFromTextMass(self, proportion, evs=None, nts=None, obs=None):
        """

                        :param proportion: Как сильно надо сжать время у нот
                        :return:
                """
        if obs is None:
            obs = []
        if evs is None:
            evs = []
        if nts is None:
            nts = ""
        np_ev = []
        # todo дописать для эвентов
        np_ev = np.array(np_ev)
        np_nt = []
        time = 0
        nts = nts

        nts = nts.split(" ")
        nts = np.array(nts).astype("int")
        for i in range(len(nts)):
            nt = nts[i]
            if (i==len(nts)-1) and (nts[-1]!=nts[i]):
                print("sdsdsdsdsdsdsdsdsdsd")
            if nt == 0:
                time+=1
            elif nt == -1:
                pass
            else:
                note = self.giveNoteFromNum(nt)
                np_nt.append([proportion * time * 1.0, note["type"], note["x"], note["y"], note["cd"]])
                note = np_nt[-1]
                x = note[2]  # 4
                y = note[3]  # 3
                type = note[1]
                dir = note[4]
                num = int(37*(3 * x + y) + 1 + type * 9 + dir)

        np_nt = np.array(np_nt)
        np_ob = []
        # todo дописать для препятствий
        np_ob = np.array(np_ob)
        self.readFromNumpy(np_ev, np_nt, np_ob)
