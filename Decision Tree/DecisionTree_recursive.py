import pandas as pd
import numpy as np

# Decision tree class
class DecisionTree:
    
    def __init__(self, max_depth = 3, min_node = 50, min_leaf=30, threshold = 0.1):
        self.max_depth = max_depth
        self.min_node = min_node
        self.min_leaf = min_leaf
        self.threshold = threshold
        
    # calculate gini
    def get_gini(self, data):
        _, counts = np.unique(np.array(data.label), return_counts= True)

        return 1-np.sum(np.square(counts/data.shape[0]))
    
    # split data
    def data_split(self, data, column, feature):
        left = data[column][data[column]==feature].index.values
        right = data[column][data[column]!=feature].index.values

        return left, right
    
    # predict label
    def get_label(self, data):
        label_count = data.groupby('label')['label'].count()

        return label_count.idxmax()
    
    # find best split
    def find_best_split(self, data):
        # setup
        n = data.shape[0]
        min_leaf = self.min_leaf
        subset_n = int(np.sqrt(data.shape[1]))
        # exclude 'label' column
        columns = np.random.choice(data.columns[:-1], size = subset_n, replace=False)
        gini_list = []
        # loop over columns except labels
        for column in data.loc[:,columns]:
            for feature in np.unique(data[column]):
                left_idx, right_idx = self.data_split(data, column, feature)

                # check if splits are smaller than min_leaf
                left_n = len(left_idx)
                right_n = len(right_idx)
                if left_n <= min_leaf and right_n <= min_leaf:
                    pass
                elif left_n > min_leaf and right_n > min_leaf:
                    left_ratio = left_n/n
                    right_ratio = right_n/n
                    gini = left_ratio*self.get_gini(data.loc[left_idx,:])+right_ratio*self.get_gini(data.loc[right_idx, :])
                    gini_list.append((column, feature, gini))

        if not gini_list:
            return None, None, None
        else:
            return min(gini_list, key= lambda x: x[2])
    
    
    # Build tree
    def build_tree(self, data, depth, base_gini):
        min_node = self.min_node
        threshold = self.threshold

        if depth == 0 or data.shape[0] < min_node:
            pass
        else:
            column, feature, min_gini = self.find_best_split(data)
            if not min_gini:
                pass
            elif base_gini-min_gini > threshold:
                left_idx, right_idx = self.data_split(data, column, feature)
                left_label = self.get_label(data.loc[left_idx, :])
                right_label = self.get_label(data.loc[right_idx, :])

                tree = {}
                tree[(column, feature, 'left', len(left_idx), left_label)] = self.build_tree(data.loc[left_idx, :], depth-1, min_gini)
                tree[(column, feature, 'right', len(right_idx), right_label)] = self.build_tree(data.loc[right_idx, :], depth-1, min_gini)

                return tree
            else:
                pass
            
    ## Predict
    def predict(self, data, tree):
        train = data.copy()
        tree_list = [(train ,tree)]
        while tree_list:
            train, tree_dict = tree_list.pop(0)

            for key, item in tree_dict.items():
                if item is not None:
                    column, feature, side, number, label = key
                    #print(key)

                    # on left leaf
                    if side == 'left':
                        left_idx, right_idx = self.data_split(train, column, feature)
                        data.loc[left_idx, 'predict'] = label
                        tree_list.append((data.loc[left_idx, :],item))

                    # on right leaf
                    else:
                        left_idx, right_idx = self.data_split(train, column, feature)
                        data.loc[right_idx, 'predict'] = label
                        # append leaf
                        tree_list.append((data.loc[right_idx, :], item))


        return 0







