# testing git integration

# testing it again

# test IDE with the code below:
from random import randint
init_bet = 100
max_bet = 800
pool = 0

n = 4
for j in range(100):
    for i in range(1, n + 1):
        cur_bet = (2**(i-1)) * init_bet
        roll = randint(0,36)
        if 0 < roll < 19: 
            pool += cur_bet
            # print(pool)
            break
        else: 
            pool -= cur_bet
    print(pool)

