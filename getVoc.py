# -*- coding: utf-8 -*-
import sqlalchemy


# class TriplexString:
#     # def trp_get_voc_xml(self, prefix, name, path_voc):
def trp_get_voc_xml(prefix, name, path_voc):
    # engine = sqlalchemy.create_engine('mssql+pyodbc://PC-ALEX/P3375_K_SBD_5_1_Ushakov?driver={SQL+Server+Native+Client+11.0}')
    # # metadata = sqlalchemy.MetaData()
    #
    # # test_table = sqlalchemy.Table('OSl_test_1')
    # # select_stmt = sqlalchemy.select([user_table.c.username, user_table.c.fullname]).\
    # #     where(user_table.c.username == 'ed')
    # # result = conn.execute(select_stmt)
    # # for row in result:
    # #     print(row)
    # q = engine.execute('SHOW DATABASES')
    # available_tables = q.fetchall()
    # print(available_tables)

    engine = sqlalchemy.create_engine(r'sqlite:///' + path)
    sql_query = 'SELECT LINK FROM OSl_test_1 WHERE OBJ=:prefix and NAME=:name'

    result = engine.execute(sql_query, prefix=prefix, name=name).fetchall()[0]
    for row in result:
        print(row)

prefix = "E"
name = "D"
path = r'E:\Document\ИТМО\5 семестр\СБД\P3375_К_СБД_5_1_Ушаков\test_sql_db_1.db'
trp_get_voc_xml(prefix, name, path)