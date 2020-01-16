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
skills, n_skills = data["skills"], len(data["skills"])

course_in_slot_room = VarArray(
    size=(n_slots, n_rooms), dom=range(-1, n_courses))

course_prof = VarArray(size=(n_courses), dom=range(n_profs))

# print(courses[0]["theme"] in profs[0]["skills"])
satisfy(
    # Assigner les cours à des salles et des creneaux (Hard 0)
    AllDifferent(course_in_slot_room, excepting=[-1]),
    Cardinality(course_in_slot_room, occurrences={
                i: 1 for i in range(n_courses)})


)
