import pandas as pd
import numpy as np

# create Tree class
class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None
        self.root = None
        self.depth = 0
        # rule of decision tree
        self.rule = None
        # test dataset
        self.test = None
        # set gini
        self.gini = None
        
    def get_depth(self):
        if self.root == None:
            return self.depth
        else:
            return self.root.get_depth()+1
        
    # set left node
    def set_left(self, left):
        self.left = left
        left.root = self
    
    # set right node
    def set_right(self, right):
        self.right = right
        right.root = self
        
    # set rules
    def set_rule(self, column, feature):
        self.rule = (column, feature)
    
    # set test data
    def set_test(self, test):
        self.test = test
        
    # get left node
    def get_left(self):
        return self.left
    
    # get right node
    def get_right(self):
        return self.right
    
    # get rules
    def get_rules(self):
        return self.rule
        
    # check if leaf
    def is_leaf(self):
        return (self.left is None and self.right is None)
    
    # predict label based on data
    def get_label(self):
        n = self.data.shape[0]
        result = self.data.groupby('label')[0].count()/n
        label = result.idxmax()
        return label

# Decision tree class
class DecisionTree:
    
    def __init__(self, max_depth = 3, min_node = 50, threshold = 0.1):
        self.root = None
        self.max_depth = max_depth
        self.min_node = min_node
        self.threshold = threshold
        
        
    # loop over every split and return best gini index
    def test_split(self, node):
        train = node.data
        ## calculate gini
        n = train.shape[0]
        gini_list = []

        # loop over columns except labels
        for column in train.iloc[:,:-1]:
            for feature in np.unique(train[column]):
                gini = self.get_gini(train, column, feature)
                gini_list.append((column, feature, gini))

        column, feature, min_gini = min(gini_list, key=lambda x: x[2])

        return column, feature, min_gini
        
        
    def build(self, data):
        root = Tree()
        root.data = data
        search_list = [root]

        # breadth first search
        while search_list:
            #print('search_list length: '+str(len(search_list) ))
            node = search_list.pop(0)
            # depth check
            #print('node depth: '+str(node.get_depth()))
            if node.get_depth() >= self.max_depth:
                continue

            # get gini based best split
            column, feature, min_gini = self.test_split(node)
            
            # when gini is less than threshold
            node.gini = self.get_gini(node.data)
            if node.gini - min_gini < self.threshold:
                continue
            
            # divide according to split
            left, right = self.get_split(node.data, column, feature)

            # node number check
            #print('left data: '+ str(left.data.shape[0]))
            #print('right data: '+ str(right.data.shape[0]))

            if left.data.shape[0] <= self.min_node | right.data.shape[0] <= self.min_node:
                continue

            # set left and right of node
            node.set_left(left)
            node.set_right(right)
            node.set_rule(column, feature)

            # append nodes
            search_list.append(left)
            search_list.append(right)
            
            # set gini
            left.gini = min_gini
            right.gini = min_gini
            
        # put root into self
        self.root = root
        
    # calculate gini index
    def get_gini(self, data, column = None, feature = None):
        n = data.shape[0]
        
        # get gini for data
        if column is None:
            column_count = data.groupby('label').count()[0]
            
            prob = column_count/n
            gini = 1-np.sum((prob**2))
            
        # get gini for data split
        else:
            # counts of each attribute, each class(label) count
            column_count = data.groupby(column)[column].count()
            class_count = data.groupby([column, 'label'])[column].count()

            # gini for left split
            class_exclude = class_count.unstack().drop(index = feature).sum()
            column_exclude = column_count.drop(index=feature).sum()
            prob_exclude = class_exclude/column_exclude
            ratio_exclude = column_exclude/n
            gini_exclude = (1-np.sum((prob_exclude)**2))

            # gini for right split
            class_feature = class_count.unstack().loc[feature]
            column_feature = column_count.loc[feature].sum()
            prob_feature = class_feature/column_feature
            ratio_feature = column_feature/n
            gini_feature = (1-np.sum((prob_feature)**2))

            # combine two gini index
            gini = ratio_exclude*gini_exclude+ratio_feature*gini_feature
        
        return gini

        
    # split based on data
    def data_split(self, data, column, feature):
        left_data = data[data[column]==feature]
        right_data = data[data[column]!=feature]
        return left_data, right_data
    
    # split based on data
    def get_split(self, data, column, feature):
        # split data
        left_data, right_data = self.data_split(data, column, feature)

        left = Tree()
        right = Tree()
        left.data =  left_data
        right.data = right_data

        return left, right
        
    # predict
    def predict(self, test):
        # create empty predict
        pred = test.copy()
        pred['predict'] = None
        
        self.root.test = test
        divide_list = [self.root]

        # breadth first search
        while divide_list:
            node = divide_list.pop(0)

            # when node is leaf
            if node.is_leaf():
                # set predicted label
                pred.loc[node.test.index, 'predict'] = node.get_label()
                continue

            column, feature = node.get_rules()
            left_data, right_data = self.data_split(node.test, column, feature)

            node.left.set_test(left_data)
            node.right.set_test(right_data)

            divide_list.append(node.left)
            divide_list.append(node.right)

        return pred['predict']
        