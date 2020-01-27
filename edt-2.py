from pycsp3 import *

class Constants:
    nbStudents = 100
    nbProfs = 10

students = Var(range(Constants.nbStudents))
profs = Var(range(Constants.nbProfs))

nomProfs = ['dl','ls']
cours = {}
cours['IF101'] = {'respo':'dl', 'amphi':8, 'td':16, 'tp':0}
cours['IF102'] = {'respo':'dl', 'amphi':10, 'td':16, 'tp':0}
cours['IS101'] = {'respo':'lg', 'amphi':16, 'td':8, 'tp':0}
cours['IS102'] = {'respo':'lg', 'amphi':16, 'td':8, 'tp':0}
cours['IF107'] = {'respo':'fh', 'amphi':9, 'td':14, 'tp':0}
cours['IF104'] = {'respo':'mf', 'amphi':2, 'td':24, 'tp':0}
cours['IT102'] = {'respo':'db', 'amphi':10, 'td':20, 'tp':0}
cours['PG101'] = {'respo':'fm', 'amphi':10, 'td':20, 'tp':0}
cours['PR103'] = {'respo':'dr', 'amphi':0, 'td':30, 'tp':0}
cours['PR109'] = {'respo':'fh', 'amphi':0, 'td':10, 'tp':0}
cours['LC109'] = {'respo':'dv', 'amphi':0, 'td':24, 'tp':0}
cours['LC101'] = {'respo':'sm', 'amphi':0, 'td':28, 'tp':0}

# 2 hours per slot
slotDuration = 2
slotsByDay = 4
slotsByWeek = slotsByDay * 5
nSemesterWeeks = 5 
slotsBySemester = slotsByWeek * nSemesterWeeks
maxTeachingPerWeek = 1 
nbTDGroups = 2

# Tous respos sont competents dans leur matiere
competent = {}
for c in cours:
    competent[cours[c]['respo']] = c

# Creation of prof lists
numberOfProfName = {}
nameOfProfNumber = []
currentNumber = 0
for c in cours:
    if cours[c]['respo'] not in numberOfProfName:
        numberOfProfName[cours[c]['respo']] = currentNumber
        nameOfProfNumber.append(cours[c]['respo'])
        currentNumber += 1
del currentNumber
print("%d profs" % len(nameOfProfNumber))

# generate lectures constraints
lectures =[] 
slotLectures = []
for c in cours:
    currentcours = cours[c]['amphi']
    lastLecture = None
    if currentcours > 0: 
        lectures.append({})
        currentcours -= 2
        lectures[-1]['profs'] = [numberOfProfName[cours[c]['respo']]]
        lectures[-1]['after'] = -1 if lastLecture is None else lastLecture
        lectures[-1]['kind'] = 'amphi'
        lectures[-1]['group'] = 'all'
        lectures[-1]['name'] = c
        lastLecture = len(lectures) - 1
    currenttd = cours[c]['td']
    while (currentcours > 0 or currenttd > 0):
        if currentcours > 0:
            lectures.append({})
            currentcours -= 2
            lectures[-1]['profs'] = [numberOfProfName[cours[c]['respo']]]
            lectures[-1]['after'] = -1 if lastLecture is None else lastLecture
            lectures[-1]['kind'] = 'amphi'
            lectures[-1]['group'] = 'all'
            lectures[-1]['name'] = c
            lastLecture = len(lectures) - 1
        if currenttd > 0:
            for tdn in range(nbTDGroups):
                lectures.append({})
                currenttd -= 2
                lectures[-1]['profs'] = [numberOfProfName[cours[c]['respo']]] # TODO: add 
                lectures[-1]['after'] = -1 if lastLecture is None else lastLecture
                lectures[-1]['kind'] = 'td'
                lectures[-1]['group'] = 'td'+str(tdn)
                lectures[-1]['name'] = c
            lastLecture = len(lectures) - 1 # On synchronise tous les TD

groups = ['all','td0','td1']
nSemesterWeeks = 8 
slotsByWeek = 20 

nLectures = len(lectures) 
nRooms = 5
nSlots = slotsByWeek * nSemesterWeeks 
nTeachers = 3 
nGroups = 3  
nTypes = 2 # Amphi or TD 

# r[i] is the room for the ith lecture
r = VarArray(size=nLectures, dom=range(nRooms))

# s[i] is the slot for the ith lecture
s = VarArray(size=nLectures, dom=range(nSlots))

# t[i] is the teacher for the ith lecture
t = VarArray(size=nLectures, dom=range(nTeachers))

# g[i] is the group for the ith lecture
g = VarArray(size=nLectures, dom=range(nGroups))

# avt[i][j] true if teacher i is available at slot j
avt = VarArray(size=(nTeachers, nSlots), dom={0,1})

# ts[i][j] is true if teacher i is teaching in slot j
ts = VarArray(size=(nTeachers, nSlots), dom={0,1})

# avg[i][j] true if group i is available at slot j
avg = VarArray(size=(nGroups,nSlots), dom={0,1})

#rt[i] is the room type needed for the ith lecture
rt = VarArray(size=nLectures, dom=range(nTypes))

# sl[i] is the number of students for the lecture i
#sl = VarArray(size=nLectures, dom=range(nStudents))

#sr[i] is the number of students that can be in room i
#sr = VarArray(size=nRooms, dom=range(nStudents))

# All the slots, split by weeks
weeks = [list(range(i*slotsByWeek, (i+1)*slotsByWeek)) for i in range(nSemesterWeeks)]

satisfy(
    # at most 'nRooms' lectures for each time slot
    #[Count(s, value=j) <= nRooms for j in range(nSlots)],

    # at most 'nGroups' lectures for each time slot (trivial but may help)
    #[Count(s, value=j) <= nGroups for j in range(nSlots)],

    # no two lectures in the same room at the same time
    [imply(s[i] == s[j], r[i] != r[j]) for i in range(nLectures) for j in range(i + 1, nLectures)],

    # no two lectures with the same teacher at the same time
    [imply(s[i] == s[j], t[i] != t[j]) for i in range(nLectures) for j in range(i + 1, nLectures)],

    # no two lectures with the same group at the same time
    [imply(s[i] == s[j], g[i] != g[j]) for i in range(nLectures) for j in range(i + 1, nLectures)],

    # The group is consistent with the lecture
    [g[i] == groups.index(lectures[i]['group']) for i in range(nLectures)],

    #[t[i] == lectures[i]['profs'][0] for i in range(nLectures)],
    [t[i] == lectures[i]['profs'][0] for i in range(nLectures)],

    [s[lectures[i]['after']] < s[i] for i in range(nLectures) if lectures[i]['after'] != -1]
    # Ensures that the room has a sufficient capacity for students
    #[imply(r[i] == room, sr[room] > sl[i]) for i in range(nLectures) for room in range(nRooms)],

    # Channeling constraint
    #[imply((t[i] == ti) & (s[i]==si), ts[ti][si]) for i in range(nLectures) for ti in range(nTeachers) for si in range(nSlots)],

    # Teacher does not teach too much per week
    #[ Sum(ts[t][s] for s in week) <= maxTeachingPerWeek for week in weeks for t in range(nTeachers) ]

    # #[ Count((t[i] == ti) & (s[i]==si) for si in week) <= maxTeachingPerWeek for week in weeks for i in range(nLectures) for ti in range(nTeachers) ]


    #[ Count((t[i] == ti) & (s[i]==si) for si in week) <= maxTeachingPerWeek for week in [[1,2]] for i in range(10,12) for ti in range(20,22) ]
    #[Count(t, value=s[j]) <= maxTeachingPerWeek for week in weeks for j in week]
)


#students = VarArray(size=n_students, dom=range())
'''
- prof dispo
- chaque etudiant ne peut être qu'à un seul endroit
- chaque prof ne peut être qu'à un seul endroit
- 1 cours maxi par salle
- la salle est de type nécessaire
- la salle est assez grande
- le cours est dans un ordre précis (contrainte regular pour chaque UE)
- l'étudiant est inscrit à des cours à suivre
- le prof est inscrit à des cours à donner
- dépendance forte entre cours
- un seul prof par lecture
- un seul groupe par lecture

SOFT
- Temps par semaine (maxi, équilibré sur le semestre)
- taille des salles pas trop grande
- 1 créneau de cours par semaine (par matière)
- temps avant exam et avant rendus de projets
- temps de travai du prof (par semaine, par semestre)
- pas de trous dans le planning
- cours pas trop tot, pas trop tard
- jeudi aprem libre
'''
