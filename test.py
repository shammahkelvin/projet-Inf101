person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "postal_code": "10001"
}

# print(type(person))  # Output: 4


number = {
    1:"one",
    7: "seven",
    3: "three",
    2: "two",
    10: "ten",
    8: "eight",
    7: "seven"
}

def lire(n):
    dict_coef = {}
    while n >= 0:
        coef = int(input(f"Coeff de x**{n}? "))
        dict_coef[n] =  coef
        n -= 1
    return dict_coef

# print(lire(3))


def valeur(p, x):
    somme=0
    for puiss in p:
        coef = p[puiss]
        somme += coef * (x**puiss)
    return somme


# res = lire(3)
# print(valeur(res, 1))

def deg(p):
    maxi = -1
    for i in p:
        if i > maxi:
            maxi = i
    return maxi

print(deg({3: 2, 2: -5, 1: 1, 0: -7}))

def simplifier(p):
    for puis in p:
        if p[puis] == 0:
            del p[puis]

def affiche(p):
    pass

res = {3: 2, 2: -5, 1: 1, 0: -7}

