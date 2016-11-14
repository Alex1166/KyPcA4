# -*- coding: utf-8 -*-
import re
from vsptd import Trp, TrpStr, parse_trp_str, RE_TRIPLET
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.sql.expression import and_
import xml.etree.ElementTree as ET


def trpGetOntVoc(prefix, name, path_db, type_db, table_name=''):
    """
    Получение словаря метаданных из базы данных
            Принимает:
                prefix - префикс реквизита
                name - имя реквизита
                path_db - путь к файлу, содержащему словари метаданных
                type_db - язык, на котором написана БД: 0 - xml, 1 - sqlite, 2 - mssql
                table_name - имя таблицы, содержащей словарь, в этой БД
            Возвращает:
                (TrpStr)
    """

    if type_db == 'XML' or type_db == 0:
        # подключение к базе данных
        try:
            tree = ET.ElementTree(file=path_db)
        except FileNotFoundError:
            return 'База данных по данному пути не найдена'

        # получение структуры XML-базы
        root = tree.getroot()
        triplex_string = TrpStr()
        # перебор всех записей в БД
        for data in root.findall('ROWDATA'):
            for row in data.iter('ROW'):
                attributes = row.attrib
                # выбор записей по совпадению префикса и имени
                if attributes.get('Q.OBJ') == prefix and attributes.get('Q.NAME') == name:
                    for attr in attributes:
                        xml_value = attributes.get(attr)
                        if attr != 'RowState':
                            if re.match(RE_TRIPLET, xml_value) is None:
                                # занесение данных из записи в триплексную строку
                                xml_prefix, xml_name = attr.split('.')
                                triplex_string += Trp(xml_prefix, xml_name, xml_value)
                            else:
                                triplex_string += parse_trp_str(xml_value)
        return triplex_string

    else:
        # подключение к базе данных
        engine = sql_engine(type_db, path_db)
        metadata = MetaData(engine)
        # подключение к таблице
        try:
            q_table = Table(table_name, metadata, autoload=True)
        except NoSuchTableError:
            return 'Таблица с таким именем не найдена'

        # получение названий столбцов из таблицы
        col_list, pref_list, name_list = [], [], []
        for col in q_table.columns:
            col_list.append(col)
            pref_list.append(col.name.split('.')[0])
            name_list.append(col.name.split('.')[1])
        # SQL-запрос для получения данных из таблицы по совпадению префикса и имени
        sql_query = q_table.select().where(and_(col_list[0] == prefix, col_list[1] == name))
        result = engine.execute(sql_query).fetchone()
        # занесение полученных данных в триплексную строку
        triplex_string = TrpStr(Trp(pref_list[0], name_list[0], result[0]),
                                Trp(pref_list[1], name_list[1], result[1]),
                                Trp(pref_list[2], name_list[2], result[2]),
                                Trp(pref_list[3], name_list[3], result[3]),
                                Trp(pref_list[4], name_list[4], result[4]),
                                )
        triplex_string += parse_trp_str(result[5])
        return triplex_string


def trpPutOntVoc(prefix, name, trp_voc, path_db, type_db, table_name=''):
    """
    Запись в словарь сторки метаданных, представленной в триплетной форме
            Принимает:
                prefix - префикс реквизита
                name - имя реквизита
                trp_voc – триплетная строка метаданных (TrpStr)
                path_db - путь к файлу, содержащему словари метаданных
                type_db - язык, на котором написана БД: 0 - xml, 1 - sqlite, 3 - mssql
                table_name - имя таблицы, содержащей словарь, в этой БД
            Возвращает:
                (TrpStr)
    """

    if type_db == 'XML' or type_db == 0:
        # подключение к базе данных
        try:
            tree = ET.ElementTree(file=path_db)
        except FileNotFoundError:
            return 'База данных по данному пути не найдена'
        # получение структуры XML-базы
        root = tree.getroot()
        # field_map = {'RowState': 0, 'Q.OBJ': 1, 'Q.NAME': 2, 'Q.FRMT': 3, 'Q.NM': 4, 'Q.K': 5, 'Q.LINK': 6}
        tree = ET.parse(path_db)
        root = tree.getroot()

        # удаление строки с реквизитом с тем же префиксом и именем
        for data in root.findall('ROWDATA'):
            for row in data.iter('ROW'):
                attributes = row.attrib
                if attributes.get('Q.OBJ') == prefix and attributes.get('Q.NAME') == name:
                    data.remove(row)

        # получение данных из триплексной строки
        trp_list = list(parse_trp_str(trp_voc))
        # создание словаря с данными
        input_voc = {(trp.prefix + '.' + trp.name): trp.value for trp in trp_list if trp.prefix == 'Q'}
        link = ''.join(str(trp) for trp in trp_list if trp.prefix != 'Q')
        input_voc.update({'Q.OBJ': prefix, 'Q.NAME': name, 'Q.LINK': link, 'RowState': "4"})
        # создание новой записи и занесение в неё данных из словаря
        new_row = ET.Element('ROW')
        new_row.attrib = input_voc
        root[1].append(new_row)
        # корректировка внешнего вида XML и запись в файл
        indentXML(root)
        tree.write(path_db, encoding="UTF-8", xml_declaration=True)

    else:
        # подключение к базе данных
        engine = sql_engine(type_db, path_db)
        metadata = MetaData(engine)
        # подключение к таблице
        try:
            q_table = Table(table_name, metadata, autoload=True)
        except NoSuchTableError:
            return 'Таблица с таким именем не найдена'
        col_list = []
        for col in q_table.columns:
            col_list.append(col)

        # удаление строки с реквизитом с тем же префиксом и именем
        engine.execute(q_table.delete().where(and_(col_list[0] == prefix, col_list[1] == name)))

        values = []
        link = ''
        trp_str = parse_trp_str(trp_voc)
        # занесение данных из триплексной строки в талбицу
        for col in col_list:
            for trp in trp_str:
                if 'Q.' + trp.name == col.name:
                    if trp.prefix == 'Q':
                        if trp.value != prefix and trp.value != name:
                            values.append(trp.value)
                    else:
                        link += str(trp)
        engine.execute(q_table.insert().values({col_list[0]: prefix,
                                                col_list[1]: name,
                                                col_list[2]: values[0],
                                                col_list[3]: values[1],
                                                col_list[4]: values[2],
                                                col_list[5]: link}
                                               )
                       )


def sql_engine(type_db, path_db):
    """
    Функция создания движка базы данных
        Принимает:
            type_db - язык, на котором написана БД: 0 - xml, 1 - sqlite, 3 - mssql
            path_db - путь к файлу, содержащему словари метаданных
        Возвращает:
            (Engine)
    """

    dialect = ''
    driver = ''
    if type_db == 'SQLite' or type_db == 1:
        dialect = r'sqlite:///'

    elif type_db == 'MS SQL Server' or type_db == 2:
        dialect = 'mssql+pyodbc://'
        driver = '?driver=ODBC+Driver+11+for+SQL+Server'

    elif type_db == 'MongoDB' or type_db == 3:
        pass

    else:
        raise ValueError('Неизвестная СУБД: ' + str(type_db))

    return create_engine(dialect + path_db + driver)


def indentXML(elem, level=0):
    """
    Функция для создания отступов
            Принимает:
                elem - элемент XML файла
                level - уровень начального отступа
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
