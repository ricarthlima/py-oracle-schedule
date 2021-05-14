import schedules
import json

MANDATORY_POINTS = 10
FROM_CIN_POINTS = 5

# Usado principalmente para definir se "Worth" tem mais ou menos peso que "Danger". 1 é igual
WORTH_MULTIPLIER = 1.5

TEACHER_HARDNESS_MULTIPLIER = 0.5
TEACHER_DIDATIC_MULTIPLIER = 0.75

# Caso uma cadeira do CIn esteja sendo dado por um professor da casa
AT_HOME_POINTS = 5


def __orderByScore(e):
    return e["score"]


def __orderByScoreGroup(e):
    return e["scoreGroup"]


def __loadTeachers():
    file = open("data/teachers.json", "r", encoding="utf-8")
    txtTeachers = file.read()
    file.close()

    dictTeachers = json.loads(txtTeachers)
    return dictTeachers


def __sumByParameter(lista, param):
    soma = 0
    for elemento in lista:
        soma += elemento[param]
    return soma


def addScorePoints(listAll, listTeachers):
    listResult = []
    for combinacoes in listAll:
        newCombinacoes = []
        for grupo in combinacoes:
            newGroup = []
            for elemento in grupo:
                score = 0

                # Cadeira obrigatória
                if elemento["mandatory"]:
                    score += MANDATORY_POINTS

                # Cadeira é do CIn
                if elemento["from_cin"]:
                    score += FROM_CIN_POINTS

                # Subtrai nível de periculosidade
                score -= elemento["danger_rate"]

                # Soma nível de valer a pena
                score += (elemento["worth_rate"] * WORTH_MULTIPLIER)

                if listTeachers != None:
                    teacher = None
                    for t in listTeachers:
                        if (elemento["teacher_code"] == t["code"]):
                            teacher = t
                            break

                    if teacher != None:
                        # Subtrai rigidez do professor
                        if teacher["hardness"] != None:
                            score -= (teacher["hardness"] *
                                      TEACHER_HARDNESS_MULTIPLIER)
                        else:
                            score -= (3 * TEACHER_HARDNESS_MULTIPLIER)

                        # Soma didática do professor
                        if teacher["didatic"] != None:
                            score += (teacher["didatic"] *
                                      TEACHER_DIDATIC_MULTIPLIER)

                        # Verifica se é uma cadeira do CIn dada por um professor do CIn
                        if teacher["from_cin"] and elemento["from_cin"]:
                            score += AT_HOME_POINTS

                elemento["score"] = score
                newGroup.append(elemento)
            newGroup.sort(key=__orderByScore, reverse=True)
            scoreGroup = __sumByParameter(newGroup, "score")
            newCombinacoes.append(
                {"scoreGroup": scoreGroup, "group": newGroup})
        newCombinacoes.sort(key=__orderByScoreGroup, reverse=True)
        listResult.append(newCombinacoes)
    return listResult


def main():
    listTeachers = __loadTeachers()
    listAll = schedules.getAll()
    listResult = addScorePoints(listAll, listTeachers)
    stringfy = json.dumps(listResult)
    input()


main()
