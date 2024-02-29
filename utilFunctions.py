def arrToSet(arr):
    s = set()
    for i in arr:
        s.add(i)
    return s

def jsonToDict(json):
    for key in json:
        json[key] = arrToSet(json[key])

def setToArr(s):
    a = []
    for i in s:
        a.append(i)
    return a

def dictToJson(dict):
    for key in dict:
        dict[key] = setToArr(dict[key])