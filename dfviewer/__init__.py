import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,\
                            QLineEdit, QTableWidget, QTableWidgetItem,\
                            QLabel, QHBoxLayout, QVBoxLayout,\
                            QHeaderView, QComboBox, QCheckBox, QStatusBar
from PyQt5.QtCore import pyqtSlot

def v(data, showRows = 100):
    app = QApplication(sys.argv)
    ex = App(data, showRows)
    #sys.exit()
    app.exec_()

class App(QWidget):
    def __init__(self, data, showRows):
        super().__init__()
        self.data = data
        self.showRows = showRows
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('DataFrame Viewer')
        self.showMaximized()
        
        self.activePage = 0
        self.sortIndex = 0
        self.sortAscending = False
                
        #Buttons
        self.prevButton = QPushButton("< Prev",self)
        self.nextButton = QPushButton("Next >",self)
        self.lastButton = QPushButton("Last >>",self)
        self.firstButton = QPushButton("<< First",self)
        
        self.nextButton.clicked.connect(self.nextPage)
        self.prevButton.clicked.connect(self.prevPage)
        self.lastButton.clicked.connect(self.lastPage)
        self.firstButton.clicked.connect(self.firstPage)
        
        #Search
        self.searchBox = QLineEdit(self)
        self.searchBox.setPlaceholderText('Search in selected column...')
        self.searchBox.returnPressed.connect(self.loadDataFrame)
        self.searchComboBox = QComboBox()
        for col_name in list(self.data.columns):
            self.searchComboBox.addItem(col_name)
        self.searchComboBox.currentIndexChanged.connect(self.loadDataFrame)
        
        self.searchQueryCheckBox = QCheckBox("Search Query")
        self.searchQueryCheckBox.stateChanged.connect(self.loadDataFrame)
        
        #Table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.changeSortCriteria)

        #Status bar
        self.statusBar = QStatusBar()

        #Layout
        self.Vlayout = QHBoxLayout()
        self.layout = QVBoxLayout()
        
        self.Vlayout.addWidget(self.searchBox)
        self.Vlayout.addWidget(self.searchComboBox)
        self.Vlayout.addWidget(self.searchQueryCheckBox)
        self.Vlayout.addWidget(self.prevButton)
        self.Vlayout.addWidget(self.nextButton)
        self.Vlayout.addWidget(self.firstButton)
        self.Vlayout.addWidget(self.lastButton)
        
        self.layout.addLayout(self.Vlayout)
        self.layout.addWidget(self.tableWidget) 
        self.layout.addWidget(self.statusBar) 
        self.setLayout(self.layout) 
        self.loadDataFrame()
        self.show()
        
    @pyqtSlot()
    def nextPage(self):
        if self.activePage != self.maxPageNumber:
            self.activePage +=1
        self.loadDataFrame()
        
    def prevPage(self):
        if self.activePage != 0:
            self.activePage -=1
        self.loadDataFrame()
        
    def lastPage(self):
        self.activePage = self.maxPageNumber
        self.loadDataFrame()
        
    def firstPage(self):
        self.activePage = 0
        self.loadDataFrame()
        
    def changeSortCriteria(self,i):
        if i == self.sortIndex:
            if self.sortAscending == True:
                self.sortAscending = False
            else:
                self.sortAscending = True
                
        self.sortIndex = i
        self.loadDataFrame()
        
    def loadDataFrame(self):
        try:
            df = self.data
            if len(self.searchBox.text())>=1:
                if self.searchQueryCheckBox.isChecked():
                    #Query mode
                    df = df.query(self.searchBox.text())
                    #We print query to log
                    print("Search Query: {}".format(self.searchBox.text() ) )
                else:
                    df = df[df[self.searchComboBox.currentText()].astype(str).str.contains(self.searchBox.text())]    
                    
            self.rowsCount = df.shape[0]
            self.colsCount = df.shape[1]
            self.maxPageNumber = int(np.ceil(self.rowsCount / self.showRows)) - 1    
            #to fix wrong page bug in search mode 
            if self.activePage > self.maxPageNumber:
                        self.activePage = 0
            self.statusBar.showMessage("Page {}/{}, Rows: {} - {}, Total Results : {}"\
                                       .format(self.activePage,\
                                           self.maxPageNumber,\
                                           (self.activePage*self.showRows),\
                                           (self.activePage*self.showRows+self.showRows),\
                                           self.rowsCount))
            
            df = df.reset_index()\
                .sort_values(self.data.columns[self.sortIndex], ascending=self.sortAscending)\
                .iloc[(self.activePage*self.showRows):(self.activePage*self.showRows+self.showRows)]
            
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setColumnCount(self.colsCount)
            self.tableWidget.setHorizontalHeaderLabels(list(self.data.columns))
            self.tableWidget.setRowCount(df.shape[0])
            i=0
            for index,row in df.iterrows():
                for col in range(self.colsCount):
                    w_item = QTableWidgetItem(str(row[col+1]))
                    self.tableWidget.setItem(i, col, w_item)
                i+=1         
            
        except Exception as e:
            print("An error occured. {}".format(e))
