from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import ugrsshapesdetection.definitions as definitions

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self)
        self.datatable = pd.DataFrame([], columns=definitions.TABLE_HEADER)

    def rowCount(self, parent=None):
        return self.datatable.shape[0]

    def columnCount(self, parent=None):
        return self.datatable.shape[1]

    def getDataAt(self, row, column):
        if 0 <= row < self.rowCount() and 0 <= column < self.columnCount():
            return self.datatable[row][column]

    def insertData(self, df):
        self.datatable = df

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                i = index.row()
                j = index.column()
                return str(self.datatable.iloc[i, j])
            elif role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignCenter
            else:
                return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.datatable.columns[col]
        return None

    def update(self, data_in):
        self.datatable = data_in

    def insertRow_(self, row_in):
        # self.datatable = self.datatable.append(pd.DataFrame([row_in], columns=definitions.TABLE_HEADER), ignore_index=True)
        # self.datatable = self.datatable
        self.datatable = pd.concat([pd.DataFrame([row_in], columns=definitions.TABLE_HEADER), self.datatable], ignore_index=True, )

    def isEmpty(self):
        return self.datatable.empty

    def getData(self):
        return self.datatable

    def cleanModel(self):
        self.datatable = pd.DataFrame([], columns=definitions.TABLE_HEADER)

    @QtCore.pyqtSlot()
    def setData(self, QModelIndex, Any, role=None):
        if role == QtCore.Qt.EditRole:
            row = QModelIndex.row()
            color = QtGui.QColor(Any)
            if color.isValid():
                self._datas[row] = color
                self.dataChanged.emit(QModelIndex, QModelIndex, [])
                return True
        return False

    def getLast(self):
        df = self.datatable.copy(deep=True)

        return df[df.index == df.index.max()], df.index.max()
