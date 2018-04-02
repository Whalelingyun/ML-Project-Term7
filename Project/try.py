import numpy as np
dic = {}
dic[1] = {}
dic['num'] = {}
for i in range(10):
    dic[1][i] = i
for i in range(10):
    dic['num'][i] = i+2


print dic


# value = np.argmax()
# value = np.array()
value = np.argmax(np.array(list(dic[i][5] for i in dic.keys())))

print dic.keys()[value]
