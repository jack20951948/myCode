import pandas as pd 
import random
import time

# 哪個feature的哪個特徵
class query:
    def __init__(self, ft, val):
        self.ft = ft
        self.val = val

    def match(self, test):
        test_val = test[self.ft]
        
        # 若爲連續則定轉折點, 離散則判斷是否吻合
        if isinstance(test_val, int) or isinstance(test_val, float):
          return test_val >= self.val
        else: 
          return test_val == self.val

    def __repr__(self):
        condition = "=="

        if isinstance(self.val, int) or isinstance(self.val, float):
            condition = ">="
        return "Is %s %s %s?" %(
            self.ft, condition, str(self.val))

class leaf: 
    def __init__(self, ds):
        self.ans = lbl_cnt(ds)

class node: 
    def __init__(self, l, r, qr):
        self.l = l
        self.r = r
        self.qr = qr

def k_fold(ds, k):
    split = []
    ref = list(ds)
    fold_sz = int(len(ds)/k)

    for _i in range(k):
        fold = []
        while len(fold) < fold_sz:
            idx = random.randrange(len(ref))
            fold.append(ref.pop(idx))
        split.append(fold)

    return split

def unique_vals(ds, ft):
    return set([row[ft] for row in ds])

def lbl_cnt(ds):
    cnt = {}

    for row in ds: 
        lbl = row[-1]
        if lbl not in cnt: 
            cnt[lbl] = 0
        cnt[lbl] += 1

    return cnt # {0:xx, 1:xx}

def partition(ds, qr):
    matched, not_matched = [], []
    
    for row in ds: 
        if qr.match(row):
            matched.append(row)
        else:
            not_matched.append(row)
    
    return matched, not_matched

def gini(ds):
    counts = lbl_cnt(ds)
    imp = 1

    for lbl in counts:
        prob = counts[lbl] / float(len(ds))
        imp -= prob**2

    return imp

def info_gain(l, r, g):
    p = float(len(l)) / (len(l) + len(r))

    return g - p * gini(l) - (1 - p) * gini(r)

def optimal_split(ds):
    opt_gain = 0
    opt_qr = None
    g = gini(ds)

    # 算每一feature的gain
    for ft in range(len(ds[0])-1):
        # id不跑
        if ft == 0:
            continue
        # 列出該feature所有特徵
        values = unique_vals(ds, ft)

        # 算該feature各特徵的gain
        for val in values: 
            qr = query(ft, val)
            l, r = partition(ds, qr)

            if len(l) == 0 or len(r) == 0:
                continue

            cur_gain = info_gain(l, r ,g)

            if cur_gain > opt_gain:
                opt_gain, opt_qr = cur_gain, qr

    return opt_gain, opt_qr

def CART(ds):
    opt_gain, opt_qr = optimal_split(ds)
    
    if opt_gain == 0 or len(ds) <= 30:
        return leaf(ds)

    l, r = partition(ds, opt_qr)

    _l = CART(l)
    _r = CART(r)

    return node(_l, _r, opt_qr)

def pred(input, _node):
    if isinstance(_node, leaf):
        return _node.ans

    if _node.qr.match(input):
        return pred(input, _node.l)
    else:
        return pred(input, _node.r)

def submitD(tds, tree):
    print("Id, Category")

    for row in tds:
        nominate = pred(row, tree)
        # nominate -> dict{0:xx, 1:xx}, print(max(dict.get))
        print(row[0], max(nominate, key=nominate.get), sep=', ')

def visual_matrix(CM):
    vm = pd.DataFrame(CM, columns = ['predict 0', 'predict 1'])

    print(vm)
    print("Sensitivity :", CM[1][1] / float(CM[1][1] + CM[0][1]) * 100)
    print("Precision :", CM[1][1] / float(CM[1][1] + CM[1][0]) * 100)

def resultD(tds, tree, CM):
    cnt = 0
    for row in tds:
        # row刪掉最後一col, 並存到test
        test = row.pop()
        nominate = pred(row, tree)
        if test == max(nominate, key=nominate.get):
            cnt += 1
        CM[test][max(nominate, key=nominate.get)] += 1
    
    return float(cnt / len(tds) * 100)

# DecisionTree(trainset, testset, mode=0, k:k-folds(in mode 2 only)):
def DecisionTree(df, td, mode=0, k=None):
    print("Planting a dicision tree...")
    ds = df.values.tolist()
    tds = td.values.tolist()

    CM = [[0 for x in range(2)] for y in range(2)] # [[0, 0], [0, 0]]

    if mode == 0:
        tree = CART(ds)
        submitD(tds, tree)  
        print("A tree is planted!")
        print("Predicting test set...\n")
    elif mode == 1:
        tree = CART(ds)
        print("A tree is planted!")
        print("Predicting test set...\n")
        ans = resultD(tds, tree, CM)
        visual_matrix(CM)
        return ans
    elif mode == 2:
        folds = k_fold(ds, k)
        tree = []
        for j in range(k):
            tmp_folds = []
            for _j in range(k):
                if _j == j:
                    continue
                tmp_folds += folds[_j]
            print("\rPlanting a tree in the {} / {} fold...".format(j + 1, k), end='    ')
            tree.append(CART(tmp_folds))
        print("\nPredicting test set...\n")

        avg = 0.0
        for fold in range(k): 
            avg += resultD(folds[fold], tree[fold], CM)

        visual_matrix(CM)
        
        return avg / float(k)

def submitR(tds, trees):
    print("Id, Category")

    for row in tds:
        cnt = {1:0, 0:0}

        for tree in trees:
            nominate = pred(row, tree)
            cnt[max(nominate, key=nominate.get)] += 1

        print(row[0], max(cnt, key=cnt.get), sep=', ')

def resultR(tds, trees, CM):
    _cnt = 0

    for row in tds:
        cnt = {1:0, 0:0}
        test = row.pop()
        for tree in trees:
            nominate = pred(row, tree)
            cnt[max(nominate, key=nominate.get)] += 1
        row.append(test)
        if test == max(cnt, key=cnt.get):
            _cnt += 1

        CM[test][max(cnt, key=cnt.get)] += 1

    return float(_cnt / len(tds) * 100)
    
# RandomForest(trainset, testset, n_sam:sample, m:tree, mode=0, k:k-folds(in mode 2 only)):
def RandomForest(df, td, n_sam, m, mode=0, k=None):
    print("Create forest...")
    trees = []
    tds = td.values.tolist()

    CM = [[0 for x in range(2)] for y in range(2)] 

    if mode == 0:
        for _i in range(m):
            print("\rPlanting the {} / {} tree...".format(_i + 1, m), end='     ')
            ds = df.sample(n=n_sam).values.tolist()
            trees.append(CART(ds))
        print("\nPredict test set...\n")
        
        submitR(tds, trees)
    
    elif mode == 1:
        for _i in range(m):
            print("\rPlanting the {} / {} tree...".format(_i + 1, m), end='     ')
            ds = df.sample(n=n_sam).values.tolist()
            trees.append(CART(ds))   
        print("\nPredicting test set...\n")

        ans = resultR(tds, trees, CM)
        visual_matrix(CM)
        return ans
    
    elif mode == 2:
        ds = df.values.tolist()
        folds = k_fold(ds, k)
        samples = []
        for j in range(k):
            tmp_folds = []
            for _j in range(k):
                if _j == j:
                    continue
                tmp_folds += folds[_j]
            samples.append(tmp_folds)

        avg = 0.0
        for i in range(len(folds)):
            for _i in range(m):
                print("\rPlanting the {} / {} tree in the {} / {} fold...".format(_i + 1, m, i + 1, k), end='           ')
                ds_t = random.sample(samples[i], n_sam)
                trees.append(CART(ds_t))
            
            avg += resultR(folds[i], trees, CM)
        
        visual_matrix(CM)
        return avg / float(k)

def main():
    # 併行
    df = pd.concat([pd.read_csv(r'Random_Forest_handmake\X_train.csv'), pd.read_csv(r'Random_Forest_handmake\y_train.csv')['Category']], axis = 1)

    # df.sample取樣(frac=比例1=100%), 重設index, 此舉為了重新排列
    df = df.sample(frac=1).reset_index(drop=True) 

    # 對df每行進行操作, 為str()即去頭去尾, 若非則不處理
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # 將?值替換成那行的第一個[0]衆數
    for col in df.columns:
        df[col] = df[col].replace('?', df[col].mode()[0])

    # drop掉["fnlwgt"]行
    del df['fnlwgt']

    # //相除取整數商
    # df['fnlwgt'] = df['fnlwgt']//50000

    td = pd.read_csv(r'Random_Forest_handmake\X_test.csv')
    td = td.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    for col in td.columns:
        td[col] = td[col].replace('?', td[col].mode()[0])
    del td['fnlwgt']
    # td['fnlwgt'] = td['fnlwgt']//50000

    # RandomForest(df, td, len(df)//5, 150)

    #################################################################################################
    train, test = df[0:int((len(df.index)+1)*.70)], df[int((len(df.index)+1)*.70):]

    # decision tree method 
    # holdout validation 
    print("\nHoldout validation with DecisionTree :")
    print("Accuracy", DecisionTree(train, test, 1))

    # k-fold validation
    print("\nk-fold validation with DecisionTree :")
    print("Accuracy :", DecisionTree(train, test, 2, 10))

    # random forest method 
    # holdout validation 
    print("\nHoldout validation with RandomForest :")
    print("Accuracy", RandomForest(train, test, len(train)//4, 200, 1))

    # k-fold validation
    print("\nk-fold validation with RandomForest :")
    print("Accuracy", RandomForest(train, test, len(train)//4, 200, 2, 10))

if __name__ == "__main__":
    startTime = time.time()
    main()
    print('\n###### Programe End / Process time: %.2f seconds ######' % (time.time() - startTime))
