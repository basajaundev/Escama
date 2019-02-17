from PyQt5.QtCore import Qt, pyqtSlot, QPoint
from PyQt5.QtWidgets import QTableWidget, QComboBox, QCheckBox, QTableWidgetItem, QHBoxLayout, QWidget, qApp, QToolTip, \
    QMenu, QAction


class tableCards(QTableWidget):
    def __init__(self, parent=None, cmarket=None):
        super(tableCards, self).__init__(parent)
        self.parent = parent
        self.cm = cmarket

        self.setSelectionBehavior(QTableWidget.SelectItems)
        self.setSelectionMode(QTableWidget.SingleSelection)

        self.setColumnCount(10)
        self.setHorizontalHeaderLabels(
            ['Nombre de la carta', 'Expansión', 'Idioma', 'Estado', 'Foil',
             'Firmada', 'Alterada', 'Stock', 'Precio', 'Cantidad'])
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.horizontalHeaderItem(5).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.horizontalHeaderItem(6).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.horizontalHeaderItem(7).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.horizontalHeaderItem(8).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.horizontalHeaderItem(9).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.resizeColumnsToContents()

        self.itemChanged.connect(self.update_item)

        self.setMouseTracking(True)
        self.cellEntered.connect(self.on_cell)

        self.row_sel_data = []
        self.all_data = []

    @pyqtSlot(QTableWidgetItem)
    def update_item(self):
        row = self.currentRow()
        col = self.currentColumn()
        if col == 8 and not self.item(row, col).text().replace(".", "", 1).isdigit():
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            idprod = self.cm.get_idproduct(self.item(row, 0).text(), self.item(row, 1).text())
            item.setText(str(self.cm.get_productprice(idprod)))
            self.setItem(row, col, item)
        if col == 9 and not self.item(row, col).text().isdigit():
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            item.setText(str(1))
            self.setItem(row, col, item)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        del_row_action = menu.addAction('Borrar la carta')
        del_row_action.triggered.connect(self.del_sel_row)

        del_all_action = menu.addAction('Borrar la tabla')
        del_all_action.triggered.connect(self.del_all_rows)

        sell_all_action = menu.addAction('Vender {} cartas'.format(self.rowCount()))
        sell_all_action.triggered.connect(self.parent.sellAllCards)

        menu.exec_(self.mapToGlobal(event.pos()))

    def on_cell(self, row, col):
        QToolTip.hideText()
        # print('Row: {0} Col: {1}'.format(row, col))

    def is_checked(self):
        clickme = qApp.focusWidget()
        index = self.indexAt(clickme.parent().pos())
        if index.isValid():
            # print(index.row(), index.column(), clickme.isChecked())
            if index.column() == 4 and clickme.isChecked():
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
                idprod = self.cm.get_idproduct(self.item(index.row(), 0).text(), self.item(index.row(), 1).text())
                item.setText(str(self.cm.get_foilprice(idprod)))
                self.setItem(index.row(), 8, item)
            elif index.column() == 4 and not clickme.isChecked():
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
                idprod = self.cm.get_idproduct(self.item(index.row(), 0).text(), self.item(index.row(), 1).text())
                item.setText(str(self.cm.get_productprice(idprod)))
                self.setItem(index.row(), 8, item)

    def del_sel_row(self):
        self.removeRow(self.currentRow())

    def del_all_rows(self):
        for i in reversed(range(self.rowCount())):
            self.removeRow(i)

    def read_all_cards(self):
        data = []
        cond = ['MT', 'NM', 'EX', 'GD', 'LP', 'PL', 'PO']
        self.all_data = []
        for row in range(self.rowCount()):
            data.append(row)

            val1 = self.item(row, 0).text()
            data.append(val1)

            val2 = self.item(row, 1).text()
            data.append(val2)

            if type(self.cellWidget(row, 2)) == QComboBox:
                val3 = self.cellWidget(row, 2).currentIndex() + 1
                data.append(val3)

            if type(self.cellWidget(row, 3)) == QComboBox:
                val4 = cond[self.cellWidget(row, 3).currentIndex()]
                data.append(val4)

            if self.cellWidget(row, 4).findChild(type(QCheckBox())).isChecked():
                val5 = 'true'
                data.append(val5)
            else:
                val5 = 'false'
                data.append(val5)

            if self.cellWidget(row, 5).findChild(type(QCheckBox())).isChecked():
                val6 = 'true'
                data.append(val6)
            else:
                val6 = 'false'
                data.append(val6)

            if self.cellWidget(row, 6).findChild(type(QCheckBox())).isChecked():
                val7 = 'true'
                data.append(val7)
            else:
                val7 = 'false'
                data.append(val7)

            val8 = int(self.item(row, 7).text())
            data.append(val8)

            val9 = float(self.item(row, 8).text())
            data.append(val9)

            val10 = int(self.item(row, 9).text())
            data.append(val10)

            self.all_data.append(data)
            data = []

        return self.all_data

    def insert_card(self, row, name, exp, stock, price):
        self.insert_value(row, 0, name)  # Nombre de la carta
        self.insert_value(row, 1, exp)  # Expansion
        self.insert_cmb_lang(row)  # Idioma
        self.insert_cmb_state(row)  # Estado
        self.insert_check(row, 4)  # Foil
        self.insert_check(row, 5)  # Firmada
        self.insert_check(row, 6)  # Alterada
        self.insert_value(row, 7, stock)  # Stock
        self.insert_value(row, 8, price)  # Precio
        self.insert_value(row, 9, '1')  # cantidad

    def insert_value(self, row, col, val):
        item = QTableWidgetItem('{0}'.format(val))
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        if col == 8 or col == 9:
            item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
        else:
            item.setFlags(Qt.ItemIsEnabled)
        self.setItem(row, col, item)

    def insert_check(self, row, col):
        qwd = QWidget()
        chk = QCheckBox()
        qly = QHBoxLayout(qwd)
        qly.addWidget(chk)
        qly.setAlignment(Qt.AlignCenter)
        qly.setContentsMargins(0, 0, 0, 0)
        self.setCellWidget(row, col, qwd)
        chk.clicked.connect(self.is_checked)

    def insert_cmb_lang(self, row):
        cmb = QComboBox()
        cmb.addItems(['Ingles', 'Frances', 'Aleman', 'Castellano', 'Italiano', 'Chino Simplificado',
                      'Japones', 'Portuges', 'Ruso', 'Koreano', 'Chino Tradicional'])
        self.setCellWidget(row, 2, cmb)

    def insert_cmb_state(self, row):
        cmb = QComboBox()
        cmb.addItems(['Mint', 'Near Mint', 'Excelent', 'Good', 'Light Played', 'Played', 'Poor'])
        cmb.setCurrentIndex(1)
        self.setCellWidget(row, 3, cmb)
