print "/////////// ML Project ///////////"

import csv
import numpy as np
import os
import codecs

y_labels = ['O', 'B-positive', 'I-positive', 'B-negative', 'I-negative', 'B-neutral', 'I-neutral']
def read_data(filename):
    f = codecs.open(filename, "r",'UTF-8')
    dic = {}
    for line in f:
        # line = line.rstrip()
        if line != '\n':
            x = line.split()[0]
            if x not in dic:
                dic[x] = 1
            else:
                dic[x] += 1
    return dic # count_x

    f.close()
    # with  as f:
    #     content = [line.strip() for line in f]
    # print(content)
    # with open(filename, 'r') as fp:
    #     data = [line.strip() for line in fp if line.strip()]
# print read_data('CN' + '/train')

def count_data(filename):
    with codecs.open(filename, "r") as f:
        content = [line.strip() for line in f if line.strip()]
    label = {} #count_y
    for i in content:
        if i != '\n':
            y = i.split()[-1]
            if y not in label:
                label[y] = 1
            else:
                label[y] += 1
    ylist = list(label.keys())
    pair = {} #count_y_x (y_-> x)
    for y in ylist:
        ydic = {}
        for i in content:
            if i != '\n':
                x = i.split()[0]
                ydic[x] = 0
        pair[y] = ydic
    for i in content:
        if i != '\n':
            x = i.split()[0]
            y = i.split()[-1]
            pair[y][x] += 1
    return label, pair


# count_y, count_y_x = count_data('EN' + '/train')  ## filename is 'EN' + '/train'
# print count_x, count_y, count_y_x

def MLE_emission (label, pair):  # get emission parameter (bu(o)) before fix.
    e = {}
    for i in pair.keys():
        pe = {}
        for j in pair[i].keys():
            pe[j] = pair[i][j]/float(label[i])
        e[i] = pe
    return e

# emission = MLE_emission(count_y, count_y_x)
# print emission
# y_labels = ['O', 'B-positive', 'I-positive', 'B-negative', 'I-negative', 'B-neutral', 'I-neutral']

print 'Set k = 1. we assume from any label y there is a certain chance of generating #UNK# as a rare event. ' \
      'Empirically we assume we have observed that there are k occurrences of such an event.'

def fix_test(testfile, testfix, dic):
    with codecs.open(testfile, "r") as test:
        with codecs.open(testfix, 'w') as fix:
            for line in test:
                if line != '\n':
                    x = line.split()[0]
                    if x not in dic.keys():
                        fix.write('#UNK#'+'\n')
                    else:
                        fix.write(x + '\n')
                else:
                    fix.write('\n')
    fix.close()

languagelist = ['CN', 'EN', 'ES', 'RU']
# for language in languagelist:
#     fix = fix_test(language + '/dev.in', language + '/devfix.in', read_data(language + '/train'))


def fix_MLE_emission (label, pair, k):
    e = {}
    for i in pair.keys():
        pe = {}
        for j in pair[i].keys():
            pe[j] = pair[i][j]/float(label[i]+k)
        pe['#UNK#'] = k/float(label[i]+k)
        e[i] = pe
    return e

# new_emission = fix_MLE_emission(count_y, count_y_x, 1)
# print new_emission
# print count_y

def simple_test(language, inputfile):
    input = codecs.open(language + inputfile, 'r')
    output = codecs.open(language + '/dev.p2.out', 'w')
    countx, county = count_data(language + '/train')
    emission = fix_MLE_emission(countx, county, 1)
    # print emission
    for line in input:
        if line != '\n':
            x = line.split()[0]
            value = np.argmax(np.array(list(emission[i][x] for i in emission.keys())))
            y = emission.keys()[value]
            output.write(x + ' ' + y + '\n')
        else:
            output.write('\n')
    output.close()

# for language in languagelist:
#     simple_test(language, '/devfix.in')

