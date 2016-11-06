# -*- coding: utf-8 -*-
from vsptd import Trp, TrpStr, parse_trp_str
from sqlalchemy import create_engine, MetaData, Table
import xml.etree.ElementTree as ET


# # для БД на mssql
# def trp_get_voc_mssql(prefix, name, path):
#     engine = sqlalchemy.create_engine('mssql+pyodbc://PC-ALEX/P3375_K_SBD_5_1_Ushakov?driver=ODBC+Driver+11+for+SQL+Server')
#     query = sqlalchemy.text('SELECT LINK FROM OSl_test_1 WHERE OBJ=:prefix and NAME=:name')
#     result = engine.execute(query,{"prefix": prefix, "name": name}).first()[0]
#     return vsptd.parse_triplex_string(result)


# для БД на sql
def trpGetOntVocSQL(prefix, name, path=r'test_sql_db_1.sqlite'):
    """
    Получение словаря метаданных из базы данных, написанной на языке SQL
            Принимает:
                prefix - префикс реквизита
                name - имя реквизита
                path - путь к файлу, содержащему словари метаданных
            Возвращает:
                (TrpStr)
    """

    # подключение к базе данных
    engine = create_engine(r'sqlite:///' + path)
    metadata = MetaData(engine)
    # подключение к таблице
    q_table = Table('OSl_test_1', metadata, autoload=True)
    triplex_string = TrpStr()
    for col in q_table.columns:
        # разделение названия таблицы и названия стобца по точке
        col_prefix, col_name = str(col).split(".")
        # SQL-запрос для получения значения в ячейке
        sql_query = 'SELECT ' + col_name + ' FROM  ' + col_prefix + '  WHERE OBJ=:prefix and NAME=:name'
        result = engine.execute(sql_query, prefix=prefix, name=name).first()[0]
        if col_name != 'LINK':
            triplet = Trp('Q', col_name, result)
            triplex_string += triplet
        else:
            triplex_string += parse_trp_str(result)
    return triplex_string


# для БД на xml
def trpGetOntVocXML(prefix, name, path=r'test_sql_db_2.xml'):
    """
        Получение словаря метаданных из базы данных, написанной на языке XML
                Принимает:
                    prefix - префикс реквизита
                    name - имя реквизита
                    path - путь к файлу, содержащему словари метаданных
                Возвращает:
                    (TrpStr)
    """

    # подключение к базе данных
    tree = ET.ElementTree(file=path)
    # получение структуры XML-базы
    root = tree.getroot()
    triplex_string = TrpStr()
    triplex_string += Trp('Q', 'OBJ', prefix)
    triplex_string += Trp('Q', 'NAME', name)
    # перебор всех записей в БД
    for r in root.findall('Rec'):
        col_prefix = r.find('OBJ').text
        col_name = r.find('NAME').text
        # поиск совпадений имени и префикса
        if col_prefix == prefix and col_name == name:
            frmt = r.find('FRMT').text
            triplex_string += Trp('Q', 'FRMT', frmt)
            nm = r.find('NM').text
            triplex_string += Trp('Q', 'NM', nm)
            k = r.find('K').text
            triplex_string += Trp('Q', 'K', int(k))
            link = r.find('LINK').text
            triplex_string += parse_trp_str(link)
    return triplex_string
