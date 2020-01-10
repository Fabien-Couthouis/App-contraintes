from pycsp3 import *
import random


n_students = 100
n_rooms = 10
n_profs = 20
n_courses = 8


students = VarArray ( size = n_students , dom =range(n_students))

#room[i][t] is the type of the room
#room[i][n] is the size of the room
