import json


def __orderer(e):
    return e["code"]


def __makeOneMore(array, allSubjects):
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
                    grupoEntrante.sort(key=__orderer)
                    if grupoEntrante not in listResult:
                        listResult.append(grupoEntrante)
    return listResult


def __saveByParam(name, lista, param):
    file = open("output/"+name+".json", "w", encoding="utf-8")
    if param == None:
        stringfy = json.dumps(lista)
        file.write(stringfy)
    else:
        newLista = []
        for grupo in lista:
            newGrupo = []
            for elemento in grupo:
                newGrupo.append(elemento[param])
            newLista.append(newGrupo)

        stringfy = json.dumps(newLista)
        file.write(stringfy)
    file.close()


def __loadFromFile():
    file = open("data/subject.json", "r", encoding="utf-8")
    txtSubject = file.read()
    file.close()

    dictSubject = json.loads(txtSubject)
    return dictSubject


def __getSeed(allSubjects):
    duplas = []
    for cadeira1 in allSubjects:
        for cadeira2 in allSubjects:
            if cadeira1["code"] != cadeira2["code"]:
                choque = False
                for diaCad1 in cadeira1["schedules"].keys():
                    for diaCad2 in cadeira2["schedules"].keys():
                        if diaCad1 == diaCad2:
                            if cadeira1["schedules"][diaCad1][0] == cadeira2["schedules"][diaCad2][0]:
                                choque = True

                if choque == False:
                    duplas.append([cadeira1, cadeira2])
        allSubjects.remove(cadeira1)

    return duplas


def __getAllPossibilities(seed, allSubjects):
    listResult = []
    listResult = listResult + [seed]

    while True:
        tempList = __makeOneMore(seed, allSubjects)
        if (tempList != []):
            listResult = listResult + [tempList]
            seed = tempList
        else:
            break

    return listResult


def outputFiles(results, param):
    i = 2
    for result in results:
        __saveByParam(str(i), result, param)
        i += 1


def getAll():
    allSubjects = __loadFromFile()
    seed = __getSeed(allSubjects)
    listResult = __getAllPossibilities(seed, allSubjects)
    return listResult
