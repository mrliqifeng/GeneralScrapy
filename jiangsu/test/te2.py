import numpy as np


def createDataSet():
    dataSet = np.array([
        [0, 0, 0, 0, 'no'],  # 数据集
        [0, 0, 0, 1, 'no'],
        [0, 1, 0, 1, 'yes'],
        [0, 1, 1, 0, 'yes'],
        [0, 0, 0, 0, 'no'],
        [1, 0, 0, 0, 'no'],
        [1, 0, 0, 1, 'no'],
        [1, 1, 1, 1, 'yes'],
        [1, 0, 1, 2, 'yes'],
        [1, 0, 1, 2, 'yes'],
        [2, 0, 1, 2, 'yes'],
        [2, 0, 1, 1, 'yes'],
        [2, 1, 0, 1, 'yes'],
        [2, 1, 0, 2, 'yes'],
        [2, 0, 0, 0, 'no']
    ])
    return dataSet


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] != value:
            reducedFeatVec = featVec[:axis].tolist()
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


if __name__ == "__main__":
    retDataSet = []
    dataSet = createDataSet()
    retDataSet = splitDataSet(dataSet, 1, 0)
    print(retDataSet)

    # for line in dataSet:
    #     axis_one= line[:1]
    #     axis_two =line[1+1:]
    #     # axis_one.extend(line[1+1:])
    #     # retDataSet.append(axis_one)
    #     print(axis_one)
    #     print("=======")
    #     print(axis_two)
    #     print("############")
    #     #print(retDataSet)
