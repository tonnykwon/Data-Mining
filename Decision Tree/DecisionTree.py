import pandas as pd
import numpy as np

# Decision tree class
class DecisionTree:
    
    def __init__(self, max_depth = 3, min_node = 50, min_leaf=30, threshold = 0.1):
        self.root = None
        self.max_depth = max_depth
        self.min_node = min_node
        self.min_leaf = min_leaf
        self.threshold = threshold
        
    # calculate gini
    def get_gini(self, data):
        n = data.shape[0]
        label_count = data.groupby('label')['label'].count()
        prob = label_count/n

        return 1-np.sum(np.square(prob))
    
    # split data
    def data_split(self, data, column, feature):
        left = data[column][data[column]==feature].index.values
        right = data[column][data[column]!=feature].index.values

        return left, right
    
    # predict label
    def get_label(self, data):
        label_count = data.groupby('label')['label'].count()

        return label_count.idxmax()
    
    # build tree
    def build(self, data):
        ## Build Tree
        max_depth = self.max_depth
        threshold = self.threshold
        min_node = self.min_node
        min_leaf = self.min_leaf
        self.data = data.copy()

        # data copy
        data_copy = data.copy()

        ## setup
        depth = 0
        result_list = []
        search_list = [(data_copy.index.values, depth)]
        base_gini_list = [self.get_gini(data_copy)]

        # breadth first search
        while search_list:

            node, depth = search_list.pop(0)
            base_gini = base_gini_list.pop(0)
            train = data_copy.loc[node]
            gini_list = []

            # case used all columns
            if train.shape[1] <=1:
                break

            # case when depth is higher than max_depth
            if depth >= max_depth:
                result_list.append((None, None, None))
                continue

            n = len(node)
            # case when node is too small to split
            if n <= min_node:
                result_list.append((None, None, None))
                continue

            # loop over columns except labels
            for column in train.iloc[:,:-1]:
                for feature in np.unique(train[column]):
                    left_idx, right_idx = self.data_split(train, column, feature)

                    # check if splits are smaller than min_leaf
                    left_n = len(left_idx)
                    right_n = len(right_idx)
                    if left_n > min_leaf and right_n > min_leaf:
                        left_ratio = left_n/n
                        right_ratio = right_n/n
                        gini = left_ratio*self.get_gini(train.loc[left_idx])+right_ratio*self.get_gini(train.loc[right_idx])
                        gini_list.append((column, feature, gini))

            # find minimum gini
            if len(gini_list) <1:
                result_list.append((None, None, None))
                continue
            column, feature, min_gini = min(gini_list, key= lambda x: x[2])
            #print('min gini: '+ str(min_gini))

            # check if satisfies threshold
            if base_gini-min_gini < threshold:
                result_list.append((None, None, None))
                continue

            # remove used column
            left_idx, right_idx = self.data_split(train, column, feature)
            data_copy = data_copy.drop(columns=column)

            # append left and right node
            depth +=1
            result_list.append((column, feature, depth))
            search_list.append((left_idx, depth))
            search_list.append((right_idx, depth))

            # update base_gini and appends left, right base_gini
            base_gini = min_gini
            base_gini_list.append(base_gini)
            base_gini_list.append(base_gini)

            # print((column, feature, depth))
            # print('left num: '+str(len(left_idx)))
            # print('right num: '+str(len(right_idx)))
            # print('new base gini: '+str(base_gini) + '\n')
        self.result_list = result_list

    # predict
    def predict(self, test):
        # copy test set
        test_set = test.copy()
        train_set = self.data.copy()

        # setup
        split_list = self.result_list.copy()
        train_set['predict'] = None
        test_set['predict'] = None
        train_list = [train_set.index]
        test_list = [test_set.index]
        min_node = self.min_node
        min_leaf = self.min_leaf

        while split_list:
            # get split criteria and datasets from each
            column, feature, depth = split_list.pop(0)

            #print(str(column)+' '+str(feature)+', '+str(depth))
            train_idx = train_list.pop(0)
            test_idx = test_list.pop(0)
            train = train_set.loc[train_idx]
            test = test_set.loc[test_idx]

            # certain condition not met
            if column is None:
                continue

            n = len(train_idx)
            if n <= min_node:
                continue

            train_left_idx, train_right_idx = self.data_split(train, column, feature)
            test_left_idx, test_right_idx = self.data_split(test, column, feature)

            # set label
            left_label = self.get_label(train_set.loc[train_left_idx])
            right_label = self.get_label(train_set.loc[train_right_idx])
            # test set labels
            test_set.loc[test_left_idx, 'predict'] = left_label
            test_set.loc[test_right_idx, 'predict'] = right_label
            # train set labels
            train_set.loc[train_left_idx, 'predict'] = left_label
            train_set.loc[train_right_idx, 'predict'] = right_label

            # put on the list
            if len(train_left_idx) > min_leaf and len(train_right_idx) > min_leaf:
                train_list.append(train_left_idx)
                train_list.append(train_right_idx)
                test_list.append(test_left_idx)
                test_list.append(test_right_idx)
        
        return test_set.predict










