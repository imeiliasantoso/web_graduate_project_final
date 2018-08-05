# -*- coding: utf-8 -*-
import sys
import numpy as np
import pandas as pd
import random
import math
import operator
import copy
import random
import json,codecs


mytree_root = 'URL_of_Anchor'
mytree_class = 'Result'
mytree_class_dict = {}
featureSplits = {}

#读取文件到DataFrame
def Read_Data(filename):
    data = pd.read_csv(filename)
    return data

#追加合并数据集,列追加
def Concatenate_Data(data1,data2):
    data = pd.concat([data1,data2],axis = 0,join='inner',ignore_index=True)
    return data

#获取数据列名称
def Columns_Name(data):
    return data.columns

#定义无用列
def NoUse_Columns():
    nouseList = ['ID','host','path']

    return nouseList

#数据过滤无用列
def Filter_Columns(data,filterList):
    usecolumns = Columns_Name(data)
    usecolumns = [c for c in usecolumns if c not in filterList]
    return data[usecolumns]

#普通字符串列处理
def Column_String(data):
    #根据字符串列去重排序，使用数值替换，向量化
    string_columns = data.select_dtypes(include=[object])
   
    for name in string_columns:
        tmplist = data[name].drop_duplicates().tolist()
        if name == mytree_class:
            for i,v in enumerate(tmplist):
                mytree_class_dict[i] = v
        data[name].replace(tmplist,range(len(tmplist)),inplace=True)
    return data



#数据集划分，num为划分训练集和测试集的比例，默认为0.2
#标签列为Dept. Status
def Split_Data(data,num=0.2):
    rangelist = list(range(0,len(data)))
    start = int((1-0.2)*len(data))
    rangelist = random.sample(rangelist,start)
    trainData = data[data.index.isin(rangelist)]
    testData = data[~data.index.isin(rangelist)]
    return trainData,testData



class Tree():
    def __init__(self):
        self.MyUseFeatures=[]
        

    #将数据集转换为矩阵
    def Trans_Data(self,data,lableName=mytree_class):
        reslist = []
        rownames = Columns_Name(data).tolist()
        
        rownames.remove(lableName)
        
        for idx,row in data.iterrows():
            tmplist = [row[name] for name in rownames]
            tmplist.append(row[lableName])
            reslist.append(tmplist)
        return np.array(reslist)
    

    # 对连续变量划分数据集，返回数据只包括最后一列
    def Split_DataSet(self,dataSet, featIndex, value):
        leftData, rightData = [], []
        for dt in dataSet:
            if dt[featIndex] <= value:
                leftData.append(dt[-1])
            else:
                rightData.append(dt[-1])
        return leftData, rightData

    # 选择最好的数据集划分方式，使得误差平方和最小
    def Best_Feature(self,dataSet):
        bestR2 = float('inf')
        bestFeatureIndex = -1
        bestSplitValue = None
        # 第i个特征
        for i in range(len(dataSet[0]) - 1):
            featList = [dt[i] for dt in dataSet]
            # 产生候选划分点
            sortfeatList = sorted(list(set(featList)))
            splitList = []
            # 如果值相同，不存在候选划分点
            if len(sortfeatList) == 1:
                splitList.append(sortfeatList[0])
            else:
                for j in range(len(sortfeatList) - 1):
                    splitList.append((sortfeatList[j] + sortfeatList[j + 1]) / 2)
            # 第j个候选划分点，记录最佳划分点
            for splitValue in splitList:
                subDataSet0, subDataSet1 = self.Split_DataSet(dataSet, i, splitValue)
                lenLeft, lenRight = len(subDataSet0), len(subDataSet1)
                # 防止数据集为空，mean不能计算
                if lenLeft == 0 and lenRight != 0:
                    rightMean = np.mean(subDataSet1)
                    R2 = sum([(x - rightMean)**2 for x in subDataSet1])
                elif lenLeft != 0 and lenRight == 0:
                    leftMean = np.mean(subDataSet0)
                    R2 = sum([(x - leftMean) ** 2 for x in subDataSet0])
                else:
                    leftMean, rightMean = np.mean(subDataSet0), np.mean(subDataSet1)
                    leftR2 = sum([(x - leftMean)**2 for x in subDataSet0])
                    rightR2 = sum([(x - rightMean)**2 for x in subDataSet1])
                    R2 = leftR2 + rightR2
                if R2 < bestR2:
                    bestR2 = R2
                    bestFeatureIndex = i
                    bestSplitValue = splitValue
        return bestFeatureIndex, bestSplitValue

    # 去掉第i个属性，生成新的数据集
    def Get_NewData(self,dataSet, featIndex, features, value):
        newFeatures = copy.deepcopy(features)
        newFeatures.remove(features[featIndex])
        leftData, rightData = [], []
        for dt in dataSet:
            temp = []
            temp.extend(dt[:featIndex])
            temp.extend(dt[featIndex + 1:])
            if dt[featIndex] <= value:
                leftData.append(temp)
            else:
                rightData.append(temp)
        return newFeatures, leftData, rightData

    # 建立决策树
    def Decision_Tree(self,dataSet, features):
        classList = [dt[-1] for dt in dataSet]
        # label一样，全部分到一边
        if classList.count(classList[0]) == len(classList):
            return classList[0]
        # 最后一个特征还不能把所有样本分到一边，则划分到平均值
        if len(features) == 1:
            return int(np.mean(classList))
        bestFeatureIndex, bestSplitValue = self.Best_Feature(dataSet)
        bestFeature = features[bestFeatureIndex]
        #print(bestFeature)
        self.MyUseFeatures.append(bestFeature)
        # 删除root特征，生成新的去掉root特征的数据集
        newFeatures, leftData, rightData = self.Get_NewData(dataSet, bestFeatureIndex, features, bestSplitValue)

        
        # 左右子树有一个为空，则返回该节点下样本均值
        if len(leftData) == 0 or len(rightData) == 0:
            return np.mean([dt[-1] for dt in leftData] + [dt[-1] for dt in rightData])
        else:
            # 左右子树不为空，则继续分裂
            '''
            myTree = {bestFeature: {'<' + str(bestSplitValue): {}, '>=' + str(bestSplitValue): {}}}
            myTree[bestFeature]['<' + str(bestSplitValue)] = self.Decision_Tree(leftData, newFeatures)
            myTree[bestFeature]['>=' + str(bestSplitValue)] = self.Decision_Tree(rightData, newFeatures)
            '''
            featureSplits[bestFeature] = int(bestSplitValue)
            myTree = {bestFeature+'<' + str(int(bestSplitValue)): {}, bestFeature+'>=' + str(int(bestSplitValue)): {}}
            myTree[bestFeature+'<' + str(int(bestSplitValue))] = self.Decision_Tree(leftData, newFeatures)
            myTree[bestFeature+'>=' + str(int(bestSplitValue))] = self.Decision_Tree(rightData, newFeatures)
        return myTree

    # 由决策树得到用于展示决策树的json文件，用于d3展示
    def Get_D3Json(self,myTree,state = ''):

        firstStr = list(myTree.keys())  # 树的第一个节点
        if state == '':
            d3json = {'name':mytree_root,"size":10,'children':[]}
        else:
            d3json = {'name':state,"size":10,'children':[]}

        for s in firstStr:
            tjson = {'name':s,"size":10,'children': []}
            secondDict = myTree[s]  # 树的第一个节点对应的键值
            
            #print ('sss',secondDict)
            if type(secondDict)==dict:
             
             for key in secondDict.keys():
                if type(secondDict[key]).__name__ == "dict":  # 如果为判断节点
                    # 则递归调用函数计算该判断节点下的叶子节点
                    tjson['children'].append(self.Get_D3Json(secondDict[key],state = key))
                    
                else:  # 如果为叶子节点
                    tjson['children'].append({'name':key,"size":10,'children':[{'name':mytree_class_dict[int(secondDict[key])],"size":10,'children':[]}]})
            else:
                tjson['children'].append({'name':mytree_class_dict[int(secondDict)],"size":10,'children':[]})
            d3json['children'].append(tjson)
        return d3json

    def Get_D3Json2(self,myTree):
        d3json = {}
        firstStr = list(myTree.keys())[0]  # 树的第一个节点
        d3json = {'name':firstStr,"size":10,'children': []}
        secondDict = myTree[firstStr]  # 树的第一个节点对应的键值
        if type(secondDict)==dict:
         for key in secondDict.keys():
            if type(secondDict[key]).__name__ == "dict":  # 如果为判断节点
                #numLeafs = numLeafs + getNumLeafs(secondDict[key])  # 则递归调用函数计算该判断节点下的叶子节点
                tmp={'name':key,"size":10,'children':[]}
                tmp['children'].append(self.Get_D3Json(secondDict[key]))
                d3json['children'].append(tmp)
                
            else:  # 如果为叶子节点
                d3json['children'].append({'name':key,"size":10,'children':[{'name':str((secondDict[key])),"size":10,'children':[]}]})

        return d3json

    #根据决策树，判断url路径
    def get_path(self,data,url,decisiontree):
        res = []
        i = 0
        for idx,row in data.iterrows():
            path = self.treeClassify(decisiontree,row)
            tmp = {'ID':url[i],'p':[mytree_root]+path}
            if tmp not in res:
                res.append(tmp)
            i+=1

        return res

    #输出决策树可视化文件
    def Decisiontree_D3json(self,mytree,data,url):
        d3json = self.Get_D3Json(mytree)
        #根据决策树，判断url路径
        res = self.get_path(data,url,mytree)

        outdict = {'tree':d3json,'path':res}

        fr = codecs.open('decisiontree.json','w','utf-8-sig')
        outstr = (json.dumps(outdict,indent=2))
        fr.write(outstr.strip())
        fr.close()


    # 随机抽取样本，样本数量与原训练样本集一样，维度为m-3,此处可以调整
    def Random_DataSet(self,dataSet):
        n, m = dataSet.shape
        features = random.sample(list(dataSet.columns.values[:-1]), m-2)
        features.append(dataSet.columns.values[-1])
        rows = [random.randint(0, n-1) for _ in range(n)]
        trainData = dataSet.iloc[rows][features]
        return trainData.values.tolist(), features


    # 对决策树测试样本求预测值，准确率
    def Decisiontree_Predict(self,mytree,rownames,testDataSet):
        predictions = []
        correct = 0
        for i in range(len(testDataSet)):
            value = int(self.treeClassify(mytree, rownames[:-1], testDataSet[i][:-1]))
            predictions.append(value)
            if testDataSet[i][-1] == value:
                correct += 1
        return predictions,(correct/float(len(testDataSet))) * 100.0
        

    # 用生成的回归树对测试样本进行测试
    def treeClassify2(self,decisionTree, featureLabel, testDataSet):
        firstFeature = list(decisionTree.keys())[0]
        secondFeatDict = decisionTree[firstFeature]
        splitValue = (list(secondFeatDict.keys())[0][1:].replace("=",""))
        featureIndex = featureLabel.index(firstFeature)
        if testDataSet[featureIndex] <= splitValue:
            valueOfFeat = secondFeatDict['<' + str(splitValue)]
        else:
            valueOfFeat = secondFeatDict['>=' + str(splitValue)]
        if isinstance(valueOfFeat, dict):
            pred_label = self.treeClassify(valueOfFeat, featureLabel, testDataSet)
        else:
            pred_label = valueOfFeat
        return pred_label

    # 用生成的回归树对测试样本进行测试
    def treeClassify(self,decisionTree,testDataSet):
        firstFeature = list(decisionTree.keys())
        path = []
        for t in firstFeature:
            idx1 = t.find('>=')
            if idx1>=0:
                name = t[:idx1]
                value = int(t[idx1+2:])
                #print (name,value)
            idx2 = t.find('<')
            if idx2>=0:
                name = t[:idx2]
                value = int(t[idx2+1:])
                #print (name,value)

            if testDataSet[name]>=value and idx1>=0:
                ss = name+'>='+str(value)
                if ss not in path:
                    path.append(ss)
            if testDataSet[name]<value and idx2<0:
                ss = name+'<'+str(value)
                if ss not in path:
                    path.append(ss)

            #print (path,testDataSet[name])
            
        valueOfFeat = decisionTree[path[-1]]
        if isinstance(valueOfFeat, dict):
            path+=(self.treeClassify(valueOfFeat, testDataSet))
        else:
            path+=[mytree_class_dict[int(valueOfFeat)]]
        return path



#分析过程
def main():
    #读取文件1
    filename = 'new_data2.csv'
    data = Read_Data(filename)
    
    #查看数据长度
    #print (len(data))
    #print (Columns_Name(data))

    url = (data['ID'].tolist())
    #获取无用数据列名称
    filterList = NoUse_Columns()
    
    #数据过滤，剔除无用数据列
    data = Filter_Columns(data,filterList)
    #查看剔除后的数据
    #print (data.head())
    #查看剔除后的数据剩余的列
    #print (Columns_Name(data))
    


    #普通字符串列数据处理
    data = (Column_String(data))

    rownames = Columns_Name(data).tolist()


    mytree = Tree()

    #将数据集转换为矩阵
    trainDataSet = mytree.Trans_Data(data,lableName=mytree_class)
    
    #创建决策树
    mytree.MyUseFeatures=[]
    decisiontree = mytree.Decision_Tree(trainDataSet, rownames)
    

    #输出有用属性
    MyUseFeatures = list(set(mytree.MyUseFeatures))
    print('输出决策树有用属性',MyUseFeatures)


    #输出决策树可视化文件
    mytree.Decisiontree_D3json(decisiontree,data,url)
    
    

    


if __name__ == '__main__':
    main()





