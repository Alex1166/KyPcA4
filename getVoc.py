# -*- coding: utf-8 -*-
import sqlalchemy
import xml.etree.ElementTree as ET
import vsptd


# # для БД на mssql
# def trp_get_voc_mssql(prefix, name, path):
#     engine = sqlalchemy.create_engine('mssql+pyodbc://PC-ALEX/P3375_K_SBD_5_1_Ushakov?driver=ODBC+Driver+11+for+SQL+Server')
#     query = sqlalchemy.text('SELECT LINK FROM OSl_test_1 WHERE OBJ=:prefix and NAME=:name')
#     result = engine.execute(query,{"prefix": prefix, "name": name}).first()[0]
#     return vsptd.parse_triplex_string(result)
#
#
# # для БД на sqlite
# def trp_get_voc_sqlite(prefix, name, path):
#     engine = sqlalchemy.create_engine(r'sqlite:///' + t)
#     sql_query = 'SELECT LINK FROM OSl_test_1 WHERE OBJ=:prefix and NAME=:name'
#     result = engine.execute(sql_query, prefix=prefix, name=name).first()[0]
#     return vsptd.parse_triplex_string(result)


# для БД на sql
def trpGetOntVocSQL(prefix, name):
    """
    Получение словаря метаданных из базы данных, написанной на языке SQL
            Принимает:
                prefix - префикс реквизита
                name - имя реквизита
                path - путь к файлу, содержащему словари метаданных
            Возвращает:
                (TrpStr)
    """
    path = r'test_sql_db_1.sqlite'

    # подключение к базе данных
    engine = sqlalchemy.create_engine(r'sqlite:///' + path)
    metadata = sqlalchemy.MetaData(engine)
    # подключение к таблице
    q_table = sqlalchemy.Table('OSl_test_1', metadata, autoload=True)
    triplex_string = vsptd.TrpStr()
    for col in q_table.columns:
        # разделение названия таблицы и названия стобца по точке
        dot = str(col).split(".")
        col_prefix = dot[0]
        col_name = dot[1]
        # SQL-запрос для получения значения в ячейке
        sql_query = 'SELECT ' + col_name + ' FROM  ' + col_prefix + '  WHERE OBJ=:prefix and NAME=:name'
        result = engine.execute(sql_query, prefix=prefix, name=name).first()[0]
        if col_name != 'LINK':
            triplet = vsptd.Trp('Q', col_name, result)
            triplex_string += triplet
        else:
            triplex_string += vsptd.parse_trp_str(result)
    return triplex_string


# для БД на xml
def trpGetOntVocXML(prefix, name):
    """
        Получение словаря метаданных из базы данных, написанной на языке XML
                Принимает:
                    prefix - префикс реквизита
                    name - имя реквизита
                    path - путь к файлу, содержащему словари метаданных
                Возвращает:
                    (TrpStr)
    """
    path = r'test_sql_db_2.xml'

    # подключение к базе данных
    tree = ET.ElementTree(file=path)
    # получение структуры XML-базы
    root = tree.getroot()
    triplex_string = vsptd.TrpStr()
    triplex_string += vsptd.Trp('Q', 'OBJ', prefix)
    triplex_string += vsptd.Trp('Q', 'NAME', name)
    # перебор всех записей в БД
    for r in root.findall('Rec'):
        col_prefix = r.find('OBJ').text
        col_name = r.find('NAME').text
        # поиск совпадений имени и префикса
        if col_prefix == prefix and col_name == name:
            frmt = r.find('FRMT').text
            triplex_string += vsptd.Trp('Q', 'FRMT', frmt)
            nm = r.find('NM').text
            triplex_string += vsptd.Trp('Q', 'NM', nm)
            k = r.find('K').text
            triplex_string += vsptd.Trp('Q', 'K', int(k))
            link = r.find('LINK').text
            triplex_string += vsptd.parse_trp_str(link)
    return triplex_string
