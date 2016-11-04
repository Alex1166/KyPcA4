# -*- coding: utf-8 -*-
import getVoc

prefix = "E"
name = "D"
db_path = r'test_sql_db_1.db'
xml_path = r'test_sql_db_2.xml'

print(getVoc.trpGetOntVocSQL(prefix, name, db_path))
print(getVoc.trpGetOntVocXML(prefix, name, xml_path))
