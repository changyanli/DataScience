import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
def convert_user_car_preference(data, users, cars):
    newData = None
    label = None
    for user, item1, item2, preference in data:
        newRow = np.array(users[user-1][1:])
        newRow = np.append(newRow, cars[item1-1][1:], axis = 0)
        newRow = np.append(newRow, cars[item2-1][1:], axis = 0)
        newRow = np.array([newRow])
        if newData is None:
            newData = newRow
            label = np.array([[preference]])
        else :
            newData = np.concatenate((newData, newRow))
            label = np.concatenate((label, np.array([[preference]])))
    return newData, label

train_data = pd.read_csv('train.csv')._get_numeric_data().values
test_data = pd.read_csv('test.csv')._get_numeric_data().values
users_data = pd.read_csv('users.csv')._get_numeric_data().values
items_data = pd.read_csv('items.csv')._get_numeric_data().values
answers = None
train_data, label = convert_user_car_preference(train_data, users_data, items_data)
model = Sequential()
model.add(Dense(3, input_dim = 12, activation = 'relu'))
model.add(Dense(2, activation = 'relu'))
model.add(Dense(1, activation = 'relu'))
model.compile(optimizer = 'rmsprop', loss = 'binary_crossentropy', metrics = ['accuracy'])
model.fit(train_data, label, epochs = 50, batch_size = 32)
for user, item1, item2 in test_data:
    newRow = np.array(users_data[user-1][1:])
    newRow = np.append(newRow, items_data[item1-1][1:], axis = 0)
    newRow = np.append(newRow, items_data[item2-1][1:], axis = 0)
    newRow = np.array([newRow])
    predict = model.predict(newRow)[0][0]
    if predict >= 0.5:
        predict = 1;
    else:
       predict = 0;
    if answers is None:
        answers = np.array([[str(user) + "-" + str(item1) + "-" + str(item2) ,predict]])
    else:
        row = np.array([[str(user) + "-" + str(item1) + "-" + str(item2) ,predict]])
        answers = np.concatenate((answers, row))
np.savetxt("answer.csv", answers, fmt='%s,%s', header="User-Item1-Item2,Preference", comments='')
