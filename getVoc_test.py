# -*- coding: utf-8 -*-
import getVoc
import putVoc
import vsptd

prefix = "E"
name = "D"

# prefix = "D"
# name = "DEPART"
# trpVoc = "$Q.FRMT='X(20)';$Q.NM='Отдел разработки';$Q.K='1';$VERT.NAME='department';$Sprut.NAME='BURO';"

# trpVoc = "$Q.OBJ='D';$Q.NAME='DEPART';$Q.FRMT='X(20)';$Q.NM='Отдел разработки';$Q.K='1';$VERT.NAME='department';$SPRUT.NAME='BURO';"

# prefix = "D"
# name = "TECH"
# trpVoc = "$Q.FRMT='X(20)';$VERT.NAME='texnolog';$SPRUT.NAME='KodUserCreate';$Q.NM='Технолог';$Q.K='1';"

# print(getVoc.trpGetOntVocSQL(prefix, name, db_path))
# print(getVoc.trpGetOntVocXML(prefix, name, xml_path))

print(getVoc.trpGetOntVoc(prefix, name, type_db=1, path_db='test_sql_db_1.sqlite', table_name='OSl_test_1'))
# print(getVoc.trpGetOntVoc(prefix, name, type_db=0, path_db='test_sql_db_2.xml'))

# print(putVoc.trpPutOntVoc(prefix, name, trpVoc, type_db=0, path_db=r'test_sql_db_3.xml'))
# print(getVoc.trpGetOntVoc(prefix, name, type_db=0, path_db='test_sql_db_3.xml'))

# print(putVoc.trpPutOntVoc(prefix, name, trpVoc, type_db=1, path_db=r'test_sql_db_1.sqlite', table_name='OSl_test_1'))
