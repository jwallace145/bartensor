import random

letters = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'X', 'Y', 'Z']]

print('{\n')
for i in range(100):
    drink_id = ''
    for j in range(64):
        if j != 0:
            random.seed(i * j)
        first_rand = random.randrange(3)
        second_rand = random.randrange(26)
        if first_rand == 0:
            second_rand = random.randrange(10)
        drink_id = drink_id + str(letters[first_rand][second_rand])
    print('\t\"' + drink_id + '\":{')
    print('\t\t\"name\":[\"\"],')
    print('\t\t\"ingredients\":[\"\", \"\", \"\", \"\", \"\"],')
    print('\t\t\"method\":[\"\", \"\", \"\", \"\", \"\"]')
    print('\t},')

print('}')
