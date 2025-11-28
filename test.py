person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "postal_code": "10001"
}

print(type(person))  # Output: 4


number = {
    1:"one",
    7: "seven",
    3: "three",
    2: "two",
    10: "ten",
    8: "eight",
    7: "seven"
}
del number[7]
number[8] = "EIGHT"
number[11] = "eleven"
print(number)  