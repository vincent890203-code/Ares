from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# ★ 關鍵：從上一層的 base.py 匯入 BaseClassifier
from ..base import BaseClassifier

class LogisticRegressionWeapon(BaseClassifier):
    def __init__(self, label_map):
        super().__init__(model_name="LogisticRegression", label_map=label_map)
        self.model = LogisticRegression(max_iter=1000, multi_class='auto')

    def fit(self, X, y):
        X_val = self._validate_input(X, is_training=True)
        self.model.fit(X_val, y)
        print(f"{self.model_name} 訓練完成。")
        
    def get_default_param_grid(self):
        return {
            'C': [0.1, 1, 10],
            'solver': ['liblinear', 'lbfgs']
        }
class SVMClassifierWeapon(BaseClassifier):
    def __init__(self, label_map, kernel='rbf'):
        super().__init__(model_name="SVM", label_map=label_map)
        self.model = SVC(kernel=kernel, probability=True, random_state=42)

    def fit(self, X, y):
        X_val = self._validate_input(X, is_training=True)
        self.model.fit(X_val, y)
        print(f"{self.model_name} 訓練完成。")
    
    def get_default_param_grid(self):
        return{
            'C' : [0.1,1,10],
            'kernel' : ['rbf', 'linear'],
            'gamma' : ['scale','auto']
        }

class KNNClassifierWeapon(BaseClassifier):
    def __init__(self, label_map, k=5):
        super().__init__(model_name=f"KNN(k={k})", label_map=label_map)
        self.model = KNeighborsClassifier(n_neighbors=k)

    def fit(self, X, y):
        X_val = self._validate_input(X, is_training=True)
        self.model.fit(X_val, y)
        print(f"{self.model_name} 訓練完成。")
    
    def get_default_param_grid(self):
        return{
            'n_neighbors': [3,5,7,9,11],
            'weights': ['uniform','distance'],
            'p' : [1,2] # 1=曼哈頓距離 2=歐式距離
            }
    
        