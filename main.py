from Stock_Predict import *
import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('預測股價漲跌幅GUI')
        self.window.geometry('600x400')
        self.window.configure(bg="SkyBlue")
        self.company = ["FB","MCD","AAPL","GOOG","MSFT","TSLA","DIS","TSM","UMC"]
        self.accuracy_list = []   #預測正確率的list
        self.prediction_next_week_list = []  #股票預測結果的list，資料為0(跌)或1(漲)
        self.turn = []  #股票預測結果0,1轉成跌,漲的list
        #self.button_image =
        self.index = 0
        self.main()
    def create_label_1(self,txt):  #label透過機器學習來預測股價
        self.label_1 = tk.Label(self.window, text = txt , font=('Arial', 22 ) , bg = "LavenderBlush" ,)
        self.label_1.grid( column = 0 , row = 1 , padx = 20 , pady = 5 , sticky='w' )
    def create_label_2(self,txt):  #label請選擇股票:
        self.lbl_1 = tk.Label(self.window, text = txt , font=('Arial', 14) , bg = "LavenderBlush" ,)
        self.lbl_1.grid( column = 0 , row = 2 , padx = 20 , pady = 5 , sticky='w')
    def create_label_3(self,txt):  #根據2020以來的數據預測接下來4天可能的漲跌
        self.lbl_2 = tk.Label(self.window, text = txt , font=('Arial', 16) , bg = "SkyBlue"  )
        self.lbl_2.grid( column = 0 , row = 5 , padx = 20 , pady = 5 , sticky='w')
    def create_label_4_0(self,txt):  #未來4天的漲或跌
        self.lbl_3_0 = tk.Label(self.window , text = txt , font=('Arial', 20) ,
                                bg = self.check_color(txt) , fg = "white" )
        self.lbl_3_0.grid( column = 0 , row = 6 , padx = 20 , pady = 5 , sticky='w')
    def create_label_4_1(self,txt):  #未來4天的漲或跌
        self.lbl_3_1 = tk.Label(self.window, text = txt , font=('Arial', 20) ,
                                bg = self.check_color(txt) , fg = "white" )
        self.lbl_3_1.grid( column = 0 , row = 6 , padx = 60 , pady = 5 , sticky='w')
    def create_label_4_2(self,txt):  #未來4天的漲或跌
        self.lbl_3_2 = tk.Label(self.window, text = txt , font=('Arial', 20) ,
                                bg = self.check_color(txt) , fg = "white" )
        self.lbl_3_2.grid( column = 0 , row = 6 , padx = 100 , pady = 5 , sticky='w')
    def create_label_4_3(self,txt):  #未來4天的漲或跌
        self.lbl_3_3 = tk.Label(self.window, text = txt , font=('Arial', 20) ,
                                bg = self.check_color(txt) , fg = "white" )
        self.lbl_3_3.grid( column = 0 , row = 6 , padx = 140 , pady = 5 , sticky='w')
    def create_label_5(self,txt):  #本次預測成功機率為：
        self.lbl_4 = tk.Label(self.window, text = txt , font=('Arial', 16) , bg = "SkyBlue"  )
        self.lbl_4.grid( column = 0 , row = 7 , padx = 20 , pady = 5 , sticky='w')
    def create_label_6(self,txt):  #預測之正確率
        self.lbl_5 = tk.Label(self.window, text = txt , font=('Arial', 16) , bg = "SkyBlue"  )
        self.lbl_5.grid( column = 0 , row = 7 , padx = 200 , pady = 5 , sticky='e')
    def create_label_7(self,txt):  #投資有賺有賠
        self.lbl_6 = tk.Label(self.window, text = txt , font=('Arial', 16) , bg = "Yellow" ,
                             fg = "Red")
        self.lbl_6.grid( column = 0 , row = 8 , padx = 20 , pady = 5 , sticky='w')
    def combobox(self):   #下拉是選單
        self.comboExample = ttk.Combobox(self.window, values = self.company, state = "readonly")
        self.comboExample.grid(column=0, row = 3 , padx = 20 , pady = 5 , sticky='w')
    def create_button_1(self,txt):  #"選擇"的按鈕
        self.button_1 = tk.Button(self.window, text = txt , height = 1 , width = 4 ,
                                   font=('Arial', 12) , command = self.get_Text_Input ,
                                 bg = "LightGray")
        self.button_1.grid( column = 0 , row = 3 , padx = 300 , pady = 5 , sticky='w')
    def get_Text_Input(self):#按下按鈕後會顯示相對應的資料
        self.stock = self.comboExample.get()
        for i in range(len(self.company)):
            if(self.stock == self.company[i]):
                self.index = i
        self.prediction_turn()
        self.create_label_3("以下為根據2020以來的數據預測接下來4天可能的漲跌：")
        self.create_label_4_0(self.turn[0])
        self.create_label_4_1(self.turn[1])
        self.create_label_4_2(self.turn[2])
        self.create_label_4_3(self.turn[3])
        self.create_label_5("本次預測成功機率為：")
        self.create_label_6(str(self.accuracy_list[self.index]))
        self.create_label_7("*投資有賺有賠，申購前應詳閱公開說明書")
    def prediction_turn(self):  #股票預測結果0,1轉成跌,漲的函式
        self.turn = []
        for i in self.prediction_next_week_list[self.index]:
            if(i == 1):
                self.turn.append("漲")
            else:
                self.turn.append("跌")
    def calculate_stock_prediction(self):  #把每間公司的預測結果與正確率存進相對應的list
        for i in self.company:
            stock = Stock_Predict(i)
            self.confusion_matrix, self.accuracy, self.prediction_next_week = stock.main_loop()
            self.accuracy_list.append(self.accuracy)
            self.prediction_next_week_list.append(self.prediction_next_week)
    def check_color(self,string):
        if(string == "漲"):
            return "red"
        else:
            return "green"
    def check(self):  #check結果而已
        for i in range(len(self.company)):
            print(self.company[i])
            print(self.accuracy_list[i])
            print(self.prediction_next_week_list[i])
    def main(self):
        self.calculate_stock_prediction()
        self.create_label_1("透過機器學習來預測股價")
        self.create_label_2("請選擇股票")
        self.combobox()
        self.create_button_1("選擇")
        #self.check()
        self.window.mainloop()

go = GUI()