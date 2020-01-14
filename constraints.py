from pycsp3 import *
import random
import json
from itertools import product

with open("data.json") as json_data:
    data = json.load(json_data)
n_slots = 7*5

students, n_students = data["students"], len(data["students"])
rooms, n_rooms = data["rooms"], len(data["rooms"])
profs, n_profs = data["profs"], len(data["profs"])
courses, n_courses = data["courses"], len(data["courses"])

students_array = VarArray(size=n_students, dom=range(n_students))
rooms_array = VarArray(size=n_rooms, dom=range(n_rooms))
profs_array = VarArray(size=n_profs, dom=range(n_profs))
courses_array = VarArray(size=n_courses, dom=range(n_courses))
slots_array = VarArray(size=n_slots, dom=range(n_slots))


# Y a t il un cours dans ce slot ? 0/1
courses_slots = VarArray(size=[n_courses, n_slots], dom={0, 1})
# Num cours par salle par slot
rooms_slots = VarArray(size=[n_rooms, n_slots], dom=range(n_courses))
# Y a t il un cours dans cette salle ? 0/1
courses_rooms = VarArray(size=[n_courses, n_rooms], dom={0, 1})

courses_profs = VarArray(size=[n_courses, n_profs], dom=range(n_courses))
courses_students = VarArray(size=[n_courses, n_students], dom=range(n_courses))

n = 10
x = VarArray(size=n, dom=range(n))
satisfy(
    # [rooms_slots[i, j] == Sum([courses_slots[x, j] * courses_rooms[x, i]
    #                            for x in range(n_courses)]) for i, j in product(range(n_rooms), range(n_slots))]
    [rooms_slots[0, 0] == Sum([courses_slots[0, 0], courses_slots[0, 1]])]


)
