import json


def orderer(e):
    return e["code"]


def makeOneMore(array, allSubjects):
    listResult = []
    for grupo in array:
        for cadeiraEntrante in allSubjects:
            if cadeiraEntrante not in grupo:
                choque = False
                for elemento in grupo:
                    for diaCad1 in cadeiraEntrante["schedules"].keys():
                        for diaCad2 in elemento["schedules"].keys():
                            if diaCad1 == diaCad2:
                                if cadeiraEntrante["schedules"][diaCad1][0] == elemento["schedules"][diaCad2][0]:
                                    choque = True
                if choque == False:
                    grupoEntrante = grupo+[cadeiraEntrante]
                    grupoEntrante.sort(key=orderer)
                    if grupoEntrante not in listResult:
                        listResult.append(grupoEntrante)
    return listResult


def printByParam(lista, param):
    for grupo in lista:
        print("[", end="")
        for elemento in grupo:
            print(elemento[param], end=",")
        print("]")


def saveByParam(name, lista, param):
    file = open("output/"+name+".json", "w", encoding="utf-8")
    for grupo in lista:
        file.write("[")
        for elemento in grupo:
            if (param == None):
                file.write(str(elemento) + ",")
            else:
                file.write(str(elemento[param]) + ",")
        file.write("],\n")
    file.close()


file = open("data/subject.json", "r", encoding="utf-8")
txtSubject = file.read()
file.close()

file = open("data/teachers.json", "r", encoding="utf-8")
txtTeachers = file.read()
file.close()


dictSubject = json.loads(txtSubject)
dictTeachers = json.loads(txtTeachers)

duplas = []

for cadeira1 in dictSubject:
    for cadeira2 in dictSubject:
        if cadeira1["code"] != cadeira2["code"]:
            choque = False
            for diaCad1 in cadeira1["schedules"].keys():
                for diaCad2 in cadeira2["schedules"].keys():
                    if diaCad1 == diaCad2:
                        if cadeira1["schedules"][diaCad1][0] == cadeira2["schedules"][diaCad2][0]:
                            choque = True

            if choque == False:
                duplas.append([cadeira1, cadeira2])
    dictSubject.remove(cadeira1)

# print(duplas)

trios = makeOneMore(duplas, dictSubject)
quartetos = makeOneMore(trios, dictSubject)

printByParam(quartetos, "name")

saveByParam("duplas", duplas, "name")
saveByParam("trios", trios, "name")
saveByParam("quartetos", quartetos, "name")
