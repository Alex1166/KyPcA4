# -*- coding: utf-8 -*-
import re
from vsptd import Trp, TrpStr, parse_trp_str, RE_TRIPLET
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import NoSuchTableError
import xml.etree.ElementTree as ET


def sql_engine(type_db, path_db):
    dialect = ''
    driver = ''
    if type_db == 1:
        dialect = r'sqlite:///'
    if type_db == 2:
        # 'mssql+pyodbc://PC-ALEX/P3375_K_SBD_5_1_Ushakov?driver=ODBC+Driver+11+for+SQL+Server'
        dialect = 'mssql+pyodbc://'
        driver = '?driver=ODBC+Driver+11+for+SQL+Server'
    if type_db == 3:
        pass
    return create_engine(dialect + path_db + driver)


def trpGetOntVoc(prefix, name, type_db, path_db, table_name=''):
    """
    Получение словаря метаданных из базы данных
            Принимает:
                prefix - префикс реквизита
                name - имя реквизита
                type_db - язык, на котором написана БД: 0 - xml, 1 - sqlite, 2 - mssql
                path_db - путь к файлу, содержащему словари метаданных
                table_name - имя таблицы, содержащей словарь, в этой БД
            Возвращает:
                (TrpStr)
    """

    if type_db == 0:
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
                if attributes.get('Q.OBJ') == prefix and attributes.get('Q.NAME') == name:

                    # ВАРИАНТ С ЗАШИТЫМИ ИМЕНАМИ СТОЛБЦОВ
                    # columns = ['Q.OBJ', 'Q.NAME', 'Q.FRMT', 'Q.NM', 'Q.K', 'Q.LINK']
                    # triplex_string = TrpStr()
                    # for col in columns:
                    #     xml_prefix, xml_name = col.split('.')
                    #     xml_value = attributes.get(col)
                    #     if col != 'Q.LINK':
                    #         triplex_string += Trp(xml_prefix, xml_name, xml_value)
                    #     else:
                    #         triplex_string += parse_trp_str(xml_value)

                    # ВАРИАНТ С НЕИЗВЕСТНЫМИ ИМЕНАМИ СТОЛБЦОВ
                    for attr in attributes:
                        xml_value = attributes.get(attr)
                        if attr != 'RowState':
                            if re.match(RE_TRIPLET, xml_value) is None:
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
        col_list = []
        for col in q_table.columns:
            col_list.append(col)
        sql_query = q_table.select().where(col_list[0] == prefix and col_list[1] == name)
        result = engine.execute(sql_query).fetchone()
        triplex_string = TrpStr(Trp('Q', col_list[0].name, result[0]),
                                Trp('Q', col_list[1].name, result[1]),
                                Trp('Q', col_list[2].name, result[2]),
                                Trp('Q', col_list[3].name, result[3]),
                                Trp('Q', col_list[4].name, result[4]),
                                )
        triplex_string += parse_trp_str(result[5])
        return triplex_string
