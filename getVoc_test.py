# -*- coding: utf-8 -*-
import getVoc
import putVoc
import vsptd

# prefix = "E"
# name = "D"
# trpVoc = "$Q.NM='Диаметр';$VERT.NAME='DIAMETR';$SPRUT.NAME='Diam';$Q.FRMT='999V99';$Q.NAME='D';$Q.K='1';$Q.OBJ='E';"

# prefix = "D"
# name = "DEPART"
# trpVoc = "$Q.FRMT='X(20)';$Q.NM='Отдел разработки';$Q.K='1';$VERT.NAME='department';$Sprut.NAME='BURO';"

# prefix = "D"
# name = "TECH"
# trpVoc = "$Q.FRMT='X(20)';$VERT.NAME='texnolog';$SPRUT.NAME='KodUserCreate';$Q.NM='Технолог';$Q.K='1';"

prefix = "E"
name = "L"
trpVoc = "$VERT.NAME='LEN';$SPRUT.NAME='Dlin';$Q.NAME='L';$Q.NM='Длина';$Q.FRMT='999V99';$Q.K='1';$Q.OBJ='E';"
# trpVoc = "$Q.NM='Длина';$Q.K='1';$VERT.NAME='LEN';$SPRUT.NAME='Dlin';$Q.FRMT='999V99';"

# ------------------XML----------------------------
# print(getVoc.trpGetOntVoc(prefix, name, type_db='XML', path_db='test_sql_db_2.xml'))
# print(getVoc.trpGetOntVoc(prefix, name, type_db='XML', path_db='test_sql_db_3.xml'))
print(putVoc.trpPutOntVoc(prefix, name, trpVoc, type_db='XML', path_db=r'test_sql_db_3.xml'))


# ------------------SQLite-------------------------
# print(getVoc.trpGetOntVoc(prefix, name, type_db='SQLite', path_db='test_sql_db_1.sqlite', table_name='OSl_test_1'))
# print(putVoc.trpPutOntVoc(prefix, name, trpVoc, type_db='SQLite', path_db=r'test_sql_db_1.sqlite', table_name='OSl_test_1'))


# ------------------MS SQL Server------------------
# print(getVoc.trpGetOntVoc(prefix, name, type_db='MS SQL Server', path_db='PC-ALEX/P3375_K_SBD_5_1_Ushakov', table_name='OSl_test_1'))
# print(putVoc.trpPutOntVoc(prefix, name, trpVoc, type_db='MS SQL Server', path_db='PC-ALEX/P3375_K_SBD_5_1_Ushakov', table_name='OSl_test_1'))