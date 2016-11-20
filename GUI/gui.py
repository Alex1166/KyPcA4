# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import sip
import xml.etree.ElementTree as ET
from functools import lru_cache
from ctypes import windll

list_of_db_types = ['XML', 'SQLite', 'MS SQL Server']


class TableWindow(QtGui.QMainWindow):
    def __init__(self, path_db=''):
        """
            Окно с таблицей
            Принимает:
                path_db - путь к базе данных в XML
        """

        QtGui.QMainWindow.__init__(self)
        # настройки окна
        self.setWindowTitle('Database viewer')

        # создание виджета таблицы
        self.table_widget = QtGui.QTableWidget()
        self.setCentralWidget(self.table_widget)

        table_lay = QtGui.QGridLayout()
        self.table_widget.setLayout(table_lay)

        # отрисовка таблицы
        if path_db != '':
            self.draw_table(path_db)

        # отображается меню
        self.menuBar()

        # создается строка статуса
        self.statusBar()

        # добавление кнопки открытия файла
        self.open_button = QtGui.QAction(u"Открыть", self)
        self.open_button.setShortcut('Ctrl+O')
        self.open_button.setStatusTip('Открыть базу данных')
        self.connect(self.open_button, QtCore.SIGNAL('triggered()'), self.open)


        # добавление кнопки выхода
        self.exit_button = QtGui.QAction(u"Выйти", self)
        self.exit_button.setShortcut('Ctrl+Q')
        self.exit_button.setStatusTip('Выйти из программы')
        self.connect(self.exit_button, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        # создание панели инструментов
        self.menu_bar = self.menuBar()

        # создание кнопки файл
        self.file_menu = self.menu_bar.addMenu('&Меню')

        # добавление кнопки выхода в меню
        self.file_menu.addAction(self.open_button)

        self.file_menu.addAction(self.exit_button)

    def draw_table(self, path_db):
        # подключение к базе данных
        try:
            tree = ET.ElementTree(file=path_db)
        except FileNotFoundError:
            return 'База данных по данному пути не найдена'
        # получение структуры XML-базы
        root = tree.getroot()

        col_list, data_list = [], []
        # получение названий столбцов
        for data in root.findall('METADATA'):
            # занесение всех строк в виде триплексных строк в список
            for row in data.iter('FIELD'):
                attributes = row.attrib
                col_list.append(attributes.get('attrname'))
        # перебор всех записей в БД
        for data in root.findall('ROWDATA'):
            # занесение всех строк в виде триплексных строк в список
            for row in data.iter('ROW'):
                attributes = row.attrib
                attributes.pop('RowState')
                data_list.append(attributes)
        row_nums_list = [str(i+1) for i in range(len(data_list))]

        # очистка таблицы
        self.table_widget.clear()

        # создание ячеек
        self.table_widget.setRowCount(len(row_nums_list))
        self.table_widget.setColumnCount(len(col_list))

        # заполнение шапок
        self.table_widget.setHorizontalHeaderLabels(col_list)
        self.table_widget.setVerticalHeaderLabels(row_nums_list)

        # заполнение ячеек
        for m, row in enumerate(row_nums_list):
            for n, col in enumerate(col_list):
                data_item = QtGui.QTableWidgetItem(data_list[m].get(col))
                data_item.setFlags(QtCore.Qt.ItemIsSelectable |
                                   QtCore.Qt.ItemIsEditable |
                                   QtCore.Qt.ItemIsEnabled
                                   )
                data_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_widget.setItem(m, n, data_item)

        self.align_rows()
        self.table_widget.itemChanged.connect(self.cell_changed)

        # добавление кнопки сохранения базы файла
        save_button = QtGui.QAction(u"Сохранить", self)
        save_button.setShortcut('Ctrl+S')
        save_button.setStatusTip('Сохранить базу данных')
        self.connect(save_button,
                     QtCore.SIGNAL('triggered()'),
                     lambda path=path_db: self.save_table(path))
        self.file_menu.removeAction(self.exit_button)
        self.file_menu.addAction(save_button)
        actions_list = self.file_menu.actions()
        if len(actions_list) == 3:
            self.file_menu.removeAction(actions_list[2])
        self.file_menu.addAction(self.exit_button)

    def save_table(self, path_db):
        print(path_db)
        # подключение к базе данных
        try:
            tree = ET.ElementTree(file=path_db)
        except FileNotFoundError:
            return 'База данных по данному пути не найдена'
        # получение структуры XML-базы
        root = tree.getroot()
        # удаление всей базы данных
        for data in root.findall('ROWDATA'):
            data.clear()

        # получение данных из таблицы
        col_list = [self.table_widget.horizontalHeaderItem(col) for col in range(self.table_widget.columnCount())]
        print(col_list)
        for n in range(self.table_widget.rowCount()):
            try:
                input_voc = {col.text(): self.table_widget.item(n, m).text() for m, col in enumerate(col_list)}
            except AttributeError:
                return
            input_voc.update({'RowState': "4"})
            # создание новой записи и занесение в неё данных из словаря
            new_row = ET.Element('ROW')
            new_row.attrib = input_voc
            root[1].append(new_row)
            # корректировка внешнего вида XML и запись в файл
            indentXML(root)
            tree.write(path_db, encoding="UTF-8", xml_declaration=True)

    def cell_changed(self, item):
        num_rows = self.table_widget.rowCount() - 1
        if item.row() == num_rows:
            empty_row_counter = 0
            prev_row = num_rows - 1
            for col in range(self.table_widget.columnCount()):
                cell = self.table_widget.item(prev_row, col)
                if cell is None or cell.text() == '':
                    empty_row_counter += 1
            if empty_row_counter == 6:
                self.table_widget.removeRow(prev_row)
            else:
                self.align_rows()

    def open(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Открыть', 'E:/Document/ИТМО/5 семестр/СБД/P3375_К_СБД_5_1_Ушаков/SBDcourse5sem/tests/db/')
        file = open(filename)
        path_db = file.name
        self.draw_table(path_db)

    def align_rows(self):
        self.table_widget.insertRow(self.table_widget.rowCount())
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

        self.resize(set_size(self.table_widget))
        self.center()

    def center(self):
        frame_gm = self.frameGeometry()
        center_point = QtGui.QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())


def set_size(widget):
    width, height, add_height = 0, 0, 0
    win_wight = windll.user32.GetSystemMetrics(0)
    win_height = windll.user32.GetSystemMetrics(1)

    for i in range(widget.columnCount()):
        width += widget.columnWidth(i)
    for i in range(widget.rowCount()):
        height += widget.rowHeight(i)
        add_height = widget.rowHeight(i)
    height += add_height * 2

    width += widget.verticalHeader().sizeHint().width()
    height += widget.horizontalHeader().sizeHint().height()

    width += widget.verticalScrollBar().sizeHint().width()
    height += widget.horizontalScrollBar().sizeHint().height()

    width += widget.frameWidth() * 2
    if height > win_height:
        height = win_height - win_height * 0.2

    if width > win_wight:
        width = win_wight - win_wight * 0.2

    return QtCore.QSize(width, height)


def indentXML(elem, level=0):
    """
    Функция для создания отступов
            Принимает:
                elem - элемент XML файла
                level (int) - уровень начального отступа
    """

    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indentXML(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


if __name__ == '__main__':
    sip.setdestroyonexit(False)
    app = QtGui.QApplication(sys.argv)
    main = TableWindow()
    main.show()
    sys.exit(app.exec_())