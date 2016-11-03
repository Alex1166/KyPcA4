# -*- coding: utf-8 -*-
import sqlalchemy
import xml.etree.ElementTree as ET


def trp_get_voc_db(p, n, t):

    # для БД на mssql
    engine = sqlalchemy.create_engine('mssql+pyodbc://PC-ALEX/P3375_K_SBD_5_1_Ushakov?driver=ODBC+Driver+11+for+SQL+Server')
    query = sqlalchemy.text('SELECT LINK FROM OSl_test_1 WHERE OBJ=:prefix and NAME=:name')
    # print(query)
    result = engine.execute(query,{"prefix": p, "name": n}).fetchall()[0]
    for row in result:
        print(row)

    # для БД на sqlite
    engine = sqlalchemy.create_engine(r'sqlite:///' + t)
    sql_query = 'SELECT LINK FROM OSl_test_1 WHERE OBJ=:prefix and NAME=:name'

    result = engine.execute(sql_query, prefix=p, name=n).fetchall()[0]
    for row in result:
        print(row)


def trp_get_voc_xml(p, n, t):
    tree = ET.ElementTree(file=t)
    root = tree.getroot()
    for r in root.findall('Rec'):
        pre = r.find("OBJ").text
        nam = r.find("NAME").text
        if pre == p and nam == n:
            link = r.find("LINK").text
            print(link)

prefix = "E"
name = "D"
db_path = r'E:\Document\ИТМО\5 семестр\СБД\P3375_К_СБД_5_1_Ушаков\SBDcourse5sem\test_sql_db_1.db'
xml_path = r'E:\Document\ИТМО\5 семестр\СБД\P3375_К_СБД_5_1_Ушаков\SBDcourse5sem\test_sql_db_2.xml'
trp_get_voc_db(prefix, name, db_path)
trp_get_voc_xml(prefix, name, xml_path)