# -*- coding: utf-8 -*-
import sys
import ontVoc
from time import time
# sys.path.append('..\\')
t = time()

prefix = ""
name = ""

prefix = "E"
name = "D"
trpVoc = "$Q.NM='Диаметр';$VERT.NAME='DIAMETR';$SPRUT.NAME='Diam';$Q.FRMT='999V99';$Q.NAME='D';$Q.K='1';$Q.OBJ='E';"

prefix = "D"
name = "DEPART"
trpVoc = "$Q.FRMT='X(20)';$Q.NM='Отдел разработки';$Q.K='1';$VERT.NAME='department';$Sprut.NAME='BURO';"

prefix = "D"
name = "TECH"
trpVoc = "$Q.FRMT='X(20)';$VERT.NAME='texnolog';$SPRUT.NAME='KodUserCreate';$Q.NM='Технолог';$Q.K='1';"

prefix = "E"
name = "L"
trpVoc = "$VERT.NAME='LEN';$SPRUT.NAME='Dlin';$Q.NAME='L';$Q.NM='Длина';$Q.FRMT='999V99';$Q.K='1';$Q.OBJ='E';"
# trpVoc = "$Q.NM='Длина';$Q.K='1';$VERT.NAME='LEN';$SPRUT.NAME='Dlin';$Q.FRMT='999V99';"

# # ------------------XML----------------------------
# print(ontVoc.trpGetOntVoc(prefix, name, path_db='db/test_sql_db_3.xml', type_db='XML'))
print(ontVoc.trpPutOntVoc(prefix, name, trpVoc, path_db='db/test_sql_db_4.xml', type_db='XML'))
#
#
# # ------------------SQLite-------------------------
# print(ontVoc.trpGetOntVoc(prefix, name, path_db='tests/db/test_sql_db_1.sqlite', type_db='SQLite', table_name='OSl_test_1'))
# print(ontVoc.trpPutOntVoc(prefix, name, trpVoc, path_db='tests/db/test_sql_db_1.sqlite', type_db='SQLite', table_name='OSl_test_1'))
#
#
# # ------------------MS SQL Server------------------
# print(ontVoc.trpGetOntVoc(prefix, name, path_db='PC-ALEX/P3375_K_SBD_5_1_Ushakov', type_db='MS SQL Server', table_name='OSl_test_1'))
# print(ontVoc.trpPutOntVoc(prefix, name, trpVoc, path_db='PC-ALEX/P3375_K_SBD_5_1_Ushakov', type_db='MS SQL Server', table_name='OSl_test_1'))


# # ------------------XML----------------------------
# ontVoc.trpGetOntVoc(prefix,
#                     name,
#                     path_db='tests/db/test_sql_db_3.xml',
#                     type_db='XML'
#                     )
# ontVoc.trpPutOntVoc(prefix,
#                     name,
#                     trpVoc,
#                     path_db='tests/db/test_sql_db_3.xml',
#                     type_db='XML'
#                     )
#
#
# # --------------SQLite-------------------------
# ontVoc.trpGetOntVoc(prefix,
#                     name,
#                     path_db='tests/db/test_sql_db_1.sqlite',
#                     type_db='SQLite',
#                     table_name='OSl_test_1'
#                     )
# ontVoc.trpPutOntVoc(prefix,
#                     name,
#                     trpVoc,
#                     path_db='tests/db/test_sql_db_1.sqlite',
#                     type_db='SQLite',
#                     table_name='OSl_test_1'
#                     )
#
#
# # --------------MS SQL Server------------------
# ontVoc.trpGetOntVoc(prefix,
#                     name,
#                     path_db='PC-ALEX/P3375_K_SBD_5_1_Ushakov',
#                     type_db='MS SQL Server',
#                     table_name='OSl_test_1'
#                     )
# ontVoc.trpPutOntVoc(prefix,
#                     name,
#                     trpVoc,
#                     path_db='PC-ALEX/P3375_K_SBD_5_1_Ushakov',
#                     type_db='MS SQL Server',
#                     table_name='OSl_test_1'
#                     )

print(time() - t)
