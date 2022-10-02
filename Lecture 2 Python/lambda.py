people=[
    {"name":"Harry","house":"Gryffindor"},
    {"name":"Cho","house":"Ravenclaw"},
    {"name":"Draco","house":"Slytherin"}
]

#def f(person):
#    return person["name"]
#people.sort(key=f)
#instead of the above three lines the following line is enough
people.sort(key=lambda person:person["name"])
print(people)