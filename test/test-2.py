import pandas as pd
from Ares.brain import ML_Brain

# 假設資料
df = pd.DataFrame({
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [2, 4, 6, 8, 10],
    'target': [0, 0, 1, 1, 0]
})
X = df[['feature1', 'feature2']]
y = df['target']

# 呼叫大腦
brain = ML_Brain()

# 大腦自動訓練並挑選
best_model = brain.think_and_train(
    X, y, X, y, # 這裡為了演示，train/test 用一樣的
    task_type='classification',
    label_map={0: 'Safe', 1: 'Toxic'}
)

# 使用冠軍模型
best_model.evaluate(X, y)