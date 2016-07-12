# E : enemy
# e : enemy if on playground
# P : player
# p : player if on playground
# 0 : not marked
# ? : state not specified
# - : border


input = """ P x 
            E P """



            
input = "".join(input.replace("\n",",").split())

index = int("".join(input.split()).index("x"))

i = index // len(input.replace(" ", "").split("\n")[0])
j = index % len(input.replace(" ", "").split("\n")[0])

# refer to changelog v1.6. for documentation
priority = "0-0"


print(input + ";" + str(priority))