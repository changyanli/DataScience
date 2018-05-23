import numpy as np
import pandas as pd

def predict(user, item1, item2):
    preference = 0
    return preference

train_data = pd.read_csv('train.csv')._get_numeric_data().as_matrix()
test_data = pd.read_csv('test.csv')._get_numeric_data().as_matrix()
users_data = pd.read_csv('users.csv')._get_numeric_data().as_matrix()
items_data = pd.read_csv('items.csv')._get_numeric_data().as_matrix()
answers = None
print(users_data)


for user, item1, item2 in test_data:
    if answers is None:
        answers = np.array([[str(user) + "-" + str(item1) + "-" + str(item2) ,predict(user, item1, item2)]])
    else:
        row = np.array([[str(user) + "-" + str(item1) + "-" + str(item2) ,predict(user, item1, item2)]])
        answers = np.concatenate((answers, row))
np.savetxt("answer.csv", answers, fmt='%s,%s', header="User-Item1-Item2,Preference", comments='')