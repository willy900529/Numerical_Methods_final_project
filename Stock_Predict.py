import yfinance as yf
import pandas as pd
from talib import abstract
import numpy as np
# 匯入決策樹分類器
from sklearn.tree import DecisionTreeClassifier
# 要計算混淆矩陣的話，要從 metrics 裡匯入 confusion_matrix
from sklearn.metrics import confusion_matrix

class Stock_Predict:
    def __init__(self,stock:str):
        self.stock = stock
        self.stk = yf.Ticker(self.stock)  #從yfinance拿取資料
        self.data = self.stk.history(start='2020-01-01') # 取得 2020 年至今的資料

    def data_simply(self):
        '''# 簡化資料，只取開、高、低、收以及成交量'''
        self.data = self.data[['Open', 'High', 'Low', 'Close', 'Volume']]

    def ta_lib(self):
        self.data.columns = ['open', 'high', 'low', 'close', 'volume'] # 改成 TA-Lib 可以辨識的欄位名稱
        self.ta_list = ['MACD','RSI','MOM','STOCH'] # 考慮的因子
        for x in self.ta_list:
            output = eval('abstract.' + x + '(self.data)')
            output.name = x.lower() if type(output) == pd.core.series.Series else None
            self.data = pd.merge(self.data, pd.DataFrame(output), left_on=self.data.index, right_on=output.index)
            self.data = self.data.set_index('key_0')

    def mark(self):
        '''五日後漲標記 1，反之標記 0'''
        self.data['week_trend'] = np.where(self.data.close.shift(-5) > self.data.close, 1, 0)

    def data_pre_deal(self):
        '''做資料的預處理'''
        self.data.isnull().sum()  # 檢查資料有無缺值
        self.data = self.data.dropna()  # 最簡單的作法是把有缺值的資料整列拿掉
        self.split_point = int(len(self.data) * 0.7)  # 決定切割比例為 70%:30%
        self.train = self.data.iloc[:self.split_point, :].copy()  # 切割成學習樣本以及測試樣本
        self.test = self.data.iloc[self.split_point:-5, :].copy()  # 切割成學習樣本以及測試樣本
        self.test_data = self.data.iloc[-5:-1, :].copy()  # 最近五天的資料

    def data_divide_into_x_and_y(self):
        # 訓練樣本再分成目標序列 y 以及因子矩陣 X
        self.train_X = self.train.drop('week_trend', axis=1)
        self.train_y = self.train.week_trend
        # 測試樣本再分成目標序列 y 以及因子矩陣 X
        self.test_X = self.test.drop('week_trend', axis=1)
        self.test_y = self.test.week_trend
        # 最後要輸出當結果的測試樣本再分成目標序列 y 以及因子矩陣 X
        self.test_data_X = self.test_data.drop('week_trend', axis=1)
        self.test_data_y = self.test_data.week_trend

    def make_decision_tree(self):
        self.model = DecisionTreeClassifier(max_depth=7)  # 叫出一棵決策樹
        self.model.fit(self.train_X, self.train_y)# 讓 A.I. 學習

    def predict(self):
        self.prediction = self.model.predict(self.test_X)  #原始資料預測
        self.prediction_next_week = self.model.predict(self.test_data_X) #預測未來一周的股價
        self.confusion_matrix = confusion_matrix(self.test_y, self.prediction)  #計算混淆矩陣
        self.accuracy = self.model.score(self.test_X, self.test_y)  #計算準確率

    def main_loop(self):
        self.data_simply()
        self.ta_lib()
        self.mark()
        self.data_pre_deal()
        self.data_divide_into_x_and_y()
        self.make_decision_tree()
        self.predict()
        return self.confusion_matrix ,self.accuracy, self.prediction_next_week


'''company = ["FB","MCD","AAPL","GOOG","MSFT","TSLA","DIS","TSM","UMC"]
for i in company:
    stock = Stock_Predict(i)
    confusion_matrix_, accuracy, prediction_next_week = stock.main_loop()
    print(i)
    print(confusion_matrix_)
    print(accuracy) #準確率
    print(prediction_next_week)  #股票未來四天的表現
    print("----------")'''


