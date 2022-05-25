import sqlite3

class DataBase():
    def __init__(self, table, db_location):
        self.__mycursor__ = None
        self.__mydb__ = None
        self.__table__ = table
        self.__db_location__ = db_location
        self.connect()

    def __del__(self):
        self.exit()
        
    def exit(self):
        try:
            self.commit()
            self.close()
        except:
            pass
        
    def connect(self):
        try:
            print("DB Connect...")
            self.__mydb__ = sqlite3.connect(self.__db_location__)
            self.__mycursor__ = self.__mydb__.cursor()
            print("Success connect!")
        except Exception as e:
            raise(e)
    
    def close(self):
        try:
            print("DB Closed...")
            self.__mydb__.close()
        except Exception as e:
            raise(e)
        
    def commit(self):
        try:
            print("Save...")
            self.__mydb__.commit()
        except Exception as e:
            raise(e)
        
    def rollback(self):
        try:
            print("Rollback...")
            self.__mydb__.rollback()
        except Exception as e:
            raise(e)
        
    
    def __asDic__(self, cursor, first=False):
        """Retorna o resultado do cursor como um dicionário"""
        try:
            descriptions = [x[0] for x in cursor.description]
            result = cursor.fetchone()
            data = []
            while result != None:
                dic = {}
                for i in range(len(descriptions)):
                    dic[descriptions[i]] = str(result[i] if result[i] != None else "")
                data.append(dic)
                result = cursor.fetchone()
            self.__mydb__.commit()
            if(first):
                return data[0]
            else:
                return data
        except Exception as e:
            return {}


    def select(self,staments="*", where=None, groupby=None, first=False, orderby=None, dic=True, limit=None, offset=None, table_as=None):
        """Executa select no banco de dados (table=tabela, staments=colunas, where=dados)"""

        try:
            # self.connect()
            tb = self.__table__
            if(table_as):
                tb += f" as {table_as}"
                
            sql = "SELECT %s FROM %s " % (staments, tb)
            if where:
                sql += '''WHERE %s''' % (where)
            if groupby != None:
                sql += " GROUP BY %s" % (groupby)
            if orderby != None:
                sql += " ORDER BY %s" % (orderby)
            if limit != None:
                sql += " LIMIT %s" % (limit)
            if offset != None:
                sql += f" OFFSET {offset}"
            print(sql)
            cur = self.__mydb__.cursor()
            cur.execute(sql)
            if dic:
                return self.__asDic__(cur, first)
            else:
                return cur.fetchall()
        except Exception as e:
            print(e)
            return {}

    def count(self, where=None):
        try:
            # self.connect()
            sql = f"SELECT COUNT(*) AS total FROM {self.__table__}"
            if where:
                sql+= f" WHERE {where}"
            # print(sql)
            cur = self.__mydb__.cursor()
            cur.execute(sql)
            return self.__asDic__(cur, True)['total']
        except Exception as e:
            raise(e)
        
    def insert(self, obj):
        """Insere dados em uma tabela (table=tabela, obj=dicionario de itens para inserir (key=column,value=value))"""
        try:
            # self.connect()
            sql = '''INSERT INTO %s (%s) VALUES("%s")''' % (
                self.__table__, ",".join([x for x in obj.keys() if obj[x]]), '''","'''.join(str(x).replace("'", "").replace("\"","") for x in obj.values() if x))
            sql = sql.replace("''", "NULL").replace("'None'", "NULL")
            # print(sql)
            self.__mycursor__.execute(sql)
            # self.__mydb.commit()
            if self.__mycursor__.rowcount > 0:
                return self.__mycursor__.lastrowid
            else:
                return None
        except Exception as e:
            print(e)
            raise(e)


    def update(self, obj, conditions, specialset=None):
        """Atualiza os dados em uma tabela (table=tabela, obj=dicionario de itens para inserir (key=column,value=value))"""
        try:
            # self.connect()
            sql = "UPDATE %s " % (self.__table__)
            staments = []
            if len(obj.keys())>0:
                sql+="SET "
            for i in obj.keys():
                if(obj[i]):
                    staments.append(i+"='"+str(obj[i])+"'")
            if(specialset):
                staments.append(f"{specialset}")
            
            sql += ",".join(staments)
            sql += " where %s" % (conditions)
            print(sql)
            self.__mycursor__.execute(sql)
            # self.__mydb.commit()
            return self.__mycursor__.rowcount > 0
        except Exception as e:
            raise(e)
        
    def delete(self, where):
        sql = "delete from %s where %s" % (self.__table__, where)
        # print(sql)
        try:
            # self.connect()
            self.__mycursor__.execute(sql)
            # self.__mydb.commit()
            return self.__mycursor__.rowcount > 0
        except Exception as e:
            raise(e)

    def executeMigration(self, file_sql_migrations):
        try:
            db_sql = []
            with open(file_sql_migrations, 'r') as f:
                txt = f.read()
                db_sql = txt.split(";")
            for sql in db_sql:
                if sql.strip():
                    try:
                        self.__mycursor__.execute(sql)
                    except Exception as e:
                        print(f"Error => {str(e)}\nSQL => {sql}")
        except Exception as e:
            print(f"Error => {str(e)}")


            
            