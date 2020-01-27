with open("result.txt", "r") as f:
    # print(f.read())
    line = f.readline()
    result = ""
    while not line.startswith("v     <list>"):
        line = f.readline()
    variables = line
    values = f.readline()


variables = variables[len("v     <list>"):- len("</list>")-1]
variables = variables.split(" ")
values = values[len("v     <values>"):-len("</values>")-1]
values = values.split(" ")
print(variables)
print("---------------------")
print(values)

nbLecture = 153

print(len(variables), len(values))
for i in range(nbLecture):
    print("lecture ", i, "room :", values[i], "slot :", values[i+nbLecture], "teacher :", values[i+2*nbLecture])

