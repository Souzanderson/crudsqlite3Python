from datetime import datetime
from library.sqlitecrud import DataBase


db = DataBase("logtable", "database.db");


''' Esse método executa um arquivo sql separado 
    por ; (ponto e vírgula) que cria as tabelas no banco '''
db.executeMigration("migrations.sql")

'''Inserindo dados'''
obj = [
        {
            "dtupdate": datetime.now().strftime("%y-%m-%d %H:%M:%S"),
            "iduser": "1531515106608",
            "observation": "c://teste//value.zip"
        },
        {
            "dtupdate": datetime.now().strftime("%y-%m-%d %H:%M:%S"),
            "iduser": "12345888",
            "observation": "c://teste//value2.zip"
        },
        {
            "dtupdate": datetime.now().strftime("%y-%m-%d %H:%M:%S"),
            "iduser": "123458885496",
            "observation": "c://teste//value3.zip"
        },
    ]

[db.insert(o) for o in obj]

'''Editando dados'''
db.update({"iduser":"teste"}, "id=2")

'''Deletando dados'''
db.delete("id=3")

'''Buscando no banco'''
res = db.select()
print(res)

'''Buscando no banco (apenas algumas colunas)'''
res = db.select(staments="iduser, id")
print(res)

'''Buscando no banco (com condições especificas)'''
res = db.select(staments="iduser, id", where="id=1")
print(res)