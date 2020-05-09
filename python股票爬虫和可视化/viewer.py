

import sys
from data_scrapy import get_data
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QTabWidget,QLabel,QTableWidget,QAbstractItemView,QTableWidgetItem,QTableView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class RightTableView(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        # self.setFixedSize(850, 400)
        self.setWindowTitle('股票跌涨幅')

        self.mainLayout = QVBoxLayout()

        tabWidgets = QTabWidget()

        label = QLabel("前一日涨幅排名前十的股票详细信息")
        tabWidgets.addTab(label, "涨幅排名")

        label = QLabel("前一日跌幅排名前十的股票详细信息")
        tabWidgets.addTab(label, "跌幅排名")

        label = QLabel("前一日换手量排名前十的股票详细信息")
        tabWidgets.addTab(label, "换手率排名")


        label = QLabel("前一日科创板涨幅排名前十的股票详细信息")
        tabWidgets.addTab(label, "科创板涨幅排名")

        label = QLabel("前一日科创板跌幅排名前十的股票详细信息")
        tabWidgets.addTab(label, "科创板跌幅排名")

        tabWidgets.currentChanged['int'].connect(self.tabClicked)   # 绑定标签点击时的信号与槽函数

        self.mainLayout.addWidget(tabWidgets)

        self.tableView=QTableView()


        self.mainLayout.addWidget(self.tableView)
        self.mainLayout.setStretch(0,1)
        self.mainLayout.setStretch(1,12)
        self.setLayout(self.mainLayout)

        self.updateView()


    def updateView(self, index=0):

        data = self.data[index]
        if index==0:
            model = QStandardItemModel(10, 8)
            model.setHorizontalHeaderLabels(["名称", '股票代码', '涨幅', "开盘", "收盘", '最高', '最低', '换手率'])
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    temp = QStandardItem(f'{item}')
                    temp.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
                    temp.setTextAlignment(Qt.AlignCenter)
                    model.setItem(i, j, temp)
            self.tableView.setModel(model)
        elif index==1:
            model = QStandardItemModel(10, 8)
            model.setHorizontalHeaderLabels(["名称", '股票代码', '跌幅', "开盘", "收盘", '最高', '最低', '换手率'])
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    temp = QStandardItem(f'{item}')
                    temp.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
                    temp.setTextAlignment(Qt.AlignCenter)
                    model.setItem(i, j, temp)
            self.tableView.setModel(model)
        elif index==2:
            model = QStandardItemModel(10, 8)
            model.setHorizontalHeaderLabels(["名称", '股票代码', '涨幅', "开盘", "收盘", '最高', '最低', '换手率'])
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    temp = QStandardItem(f'{item}')
                    temp.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
                    temp.setTextAlignment(Qt.AlignCenter)
                    model.setItem(i, j, temp)
            self.tableView.setModel(model)
        elif index==3:
            model = QStandardItemModel(10, 8)
            model.setHorizontalHeaderLabels(["名称", '股票代码', '发行价', "最新价", "涨额", '涨幅', '5分钟涨幅', '换手率'])
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    temp = QStandardItem(f'{item}')
                    temp.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
                    temp.setTextAlignment(Qt.AlignCenter)
                    model.setItem(i, j, temp)
            self.tableView.setModel(model)
        else:
            model = QStandardItemModel(10, 8)
            model.setHorizontalHeaderLabels(["名称", '股票代码', '发行价', "最新价", "跌额", '跌幅', '5分钟跌幅', '换手率'])
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    temp = QStandardItem(f'{item}')
                    temp.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
                    temp.setTextAlignment(Qt.AlignCenter)
                    model.setItem(i, j, temp)
            self.tableView.setModel(model)




    def tabClicked(self,index):
        self.updateView(index)
        print(index)



if __name__ == '__main__':
    print('准备数据中')
    data = get_data()
    print('数据准备完成')
    app = QApplication(sys.argv)
    mainWin = RightTableView(data=data)
    mainWin.show()
    sys.exit(app.exec_())