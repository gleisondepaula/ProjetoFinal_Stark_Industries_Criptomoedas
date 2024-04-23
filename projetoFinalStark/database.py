import mysql.connector

class Database:
    def __init__(self, host="localhost", user="gleisondepaula", password="864225mg.", database="stark_tasks"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def adicionar_tarefa(self, descricao, data_inicio, data_termino, status):
        sql = "INSERT INTO tarefas (descricao, data_inicio, data_termino, status) VALUES (%s, %s, %s, %s)"
        values = (descricao, data_inicio, data_termino, status)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def listar_tarefas(self):
        sql = "SELECT * FROM tarefas"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def editar_tarefa(self, id_tarefa, descricao, data_inicio, data_termino):
        sql = "UPDATE tarefas SET descricao = %s, data_inicio = %s, data_termino = %s WHERE id = %s"
        values = (descricao, data_inicio, data_termino, id_tarefa)  # Corrigido o nome da variável para id_tarefa
        self.cursor.execute(sql, values)
        self.conn.commit()

    def remover_tarefa(self, id_tarefa):
        sql = "DELETE FROM tarefas WHERE id = %s"
        self.cursor.execute(sql, (id_tarefa,))  # Corrigido o nome da variável para id_tarefa
        self.conn.commit()

    def marcar_tarefa_como_realizada(self, tarefa_id):
        sql = "UPDATE tarefas SET status = 'Realizada' WHERE id = %s"
        self.cursor.execute(sql, (tarefa_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
