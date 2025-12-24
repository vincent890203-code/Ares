# 匯入必要的 sklearn 模組
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# 從上一層的 base.py 匯入 BaseRegressor
# .. 代表「上一層目錄 (brain)」，所以 ..base 就是 brain/base.py
from ..base import BaseRegressor

class LinearRegressionWeapon(BaseRegressor):
    def __init__(self):
        super().__init__(model_name="LinearRegression")
        self.model = LinearRegression()

    def fit(self, X, y):
        X_val = self._validate_input(X, is_training=True)
        self.model.fit(X_val, y)
        print(f"{self.model_name} 訓練完成。")
    def get_default_param_grid(self):
        # 線性回歸通常沒什麼好調的，但可以調是否擬合截距
        return {'fit_intercept': [True, False]}
    
class PolynomialRegressionWeapon(BaseRegressor):
    def __init__(self, degree=2):
        super().__init__(model_name=f"PolyRegression(deg={degree})")
        self.model = make_pipeline(PolynomialFeatures(degree), LinearRegression())

    def fit(self, X, y):
        X_val = self._validate_input(X, is_training=True)
        self.model.fit(X_val, y)
        print(f"{self.model_name} 訓練完成。")
    def get_default_param_grid(self):
        # Pipeline 的參數名稱要加前綴，例如 polynomialfeatures__degree
        # 但因為我們目前架構比較簡單，先暫時回傳空字典，或是需要改寫 base.py 來支援 pipeline 參數
        # 為了 Day 3 進度順利，我們先不調這隻，讓它回傳空字典
        return {}
    
class DecisionTreeRegressorWeapon(BaseRegressor):
    def __init__(self, max_depth=None):
        super().__init__(model_name="RegressionTree")
        self.model = DecisionTreeRegressor(max_depth=max_depth, random_state=42)

    def fit(self, X, y):
        X_val = self._validate_input(X, is_training=True)
        self.model.fit(X_val, y)
        print(f"{self.model_name} 訓練完成。")
    
    def get_default_param_grid(self):
        return {
            'max_depth': [3, 5, 10, None],
            'min_samples_split': [2, 5, 10]
        }
    
class SVRWeapon(BaseRegressor):
    def __init__(self, kernel='rbf', C=1.0):
        super().__init__(model_name=f"SVR({kernel})")
        self.model = SVR(kernel=kernel, C=C)

    def fit(self, X, y):
        X_val = self._validate_input(X, is_training=True)
        self.model.fit(X_val, y)
        print(f"{self.model_name} 訓練完成。")
    
    def get_default_param_grid(self):
        return {
            'C': [0.1, 1, 10],
            'kernel': ['rbf', 'linear']
        }