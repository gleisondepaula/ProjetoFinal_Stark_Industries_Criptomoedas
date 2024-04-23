import tkinter as tk
from tkinter import messagebox
from database import Database

class AplicativoGerenciadorTarefas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas Stark")
        self.db = Database(host="localhost", user="gleisondepaula", password="864225mg.", database="stark_tasks")

        self.criar_widgets()
        self.carregar_tarefas()

    def criar_widgets(self):
        self.lista_tarefas = tk.Listbox(self.root, width=50, height=15)
        self.lista_tarefas.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.lista_tarefas.yview)
        self.scrollbar.grid(row=0, column=4, sticky="ns")

        self.lista_tarefas.config(yscrollcommand=self.scrollbar.set)

        self.rotulo_descricao = tk.Label(self.root, text="Descrição:")
        self.rotulo_descricao.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entrada_descricao = tk.Entry(self.root, width=40)
        self.entrada_descricao.grid(row=1, column=1, columnspan=3, padx=10, pady=5)

        self.rotulo_data_inicio = tk.Label(self.root, text="Data de Início (AAAA-MM-DD):")
        self.rotulo_data_inicio.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entrada_data_inicio = tk.Entry(self.root, width=15)
        self.entrada_data_inicio.grid(row=2, column=1, padx=10, pady=5)

        self.rotulo_data_termino = tk.Label(self.root, text="Data de Término (AAAA-MM-DD):")
        self.rotulo_data_termino.grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.entrada_data_termino = tk.Entry(self.root, width=15)
        self.entrada_data_termino.grid(row=2, column=3, padx=10, pady=5)

        self.botao_adicionar = tk.Button(self.root, text="Adicionar Tarefa", command=self.adicionar_tarefa)
        self.botao_adicionar.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.botao_editar = tk.Button(self.root, text="Editar Tarefa", command=self.editar_tarefa)
        self.botao_editar.grid(row=3, column=2, columnspan=2, padx=10, pady=5)

        self.botao_excluir = tk.Button(self.root, text="Excluir Tarefa", command=self.excluir_tarefa)
        self.botao_excluir.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.botao_atualizar = tk.Button(self.root, text="Atualizar", command=self.carregar_tarefas)
        self.botao_atualizar.grid(row=4, column=2, columnspan=2, padx=10, pady=5)
        # Botão para marcar uma tarefa como realizada
        self.botao_marcar_realizada = tk.Button(self.root, text="Marcar como Realizada",
                                                command=self.marcar_tarefa_como_realizada)
        self.botao_marcar_realizada.grid(row=4, column=2, columnspan=2, padx=10, pady=5)
    def carregar_tarefas(self):
        self.lista_tarefas.delete(0, tk.END)
        for tarefa in self.db.listar_tarefas():
            self.lista_tarefas.insert(tk.END, f"{tarefa[0]} - {tarefa[1]} - {tarefa[2]} até {tarefa[3]} ({tarefa[4]})")

    def adicionar_tarefa(self):
        descricao = self.entrada_descricao.get()
        data_inicio = self.entrada_data_inicio.get()
        data_termino = self.entrada_data_termino.get()
        status = "A fazer"
        self.db.adicionar_tarefa(descricao, data_inicio, data_termino, status)
        self.limpar_entradas()
        self.carregar_tarefas()

    # No arquivo main.py, na função editar_tarefa
    def editar_tarefa(self):
        try:
            selected_task_index = self.lista_tarefas.curselection()[0]
            selected_task = self.lista_tarefas.get(selected_task_index)
            task_id = selected_task.split("-")[0].strip()
            new_descricao = self.entrada_descricao.get()
            new_data_inicio = self.entrada_data_inicio.get()
            new_data_termino = self.entrada_data_termino.get()

            # Verificar se as datas não estão vazias
            if new_data_inicio and new_data_termino:
                self.db.editar_tarefa(task_id, new_descricao, new_data_inicio, new_data_termino)
                self.limpar_entradas()
                self.carregar_tarefas()
            else:
                messagebox.showwarning("Aviso", "Por favor, preencha as datas de início e término.")
        except IndexError:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para editar.")

    def excluir_tarefa(self):
        try:
            selected_task_index = self.lista_tarefas.curselection()[0]
            selected_task = self.lista_tarefas.get(selected_task_index)
            task_id = selected_task.split("-")[0].strip()
            self.db.remover_tarefa(task_id)
            self.limpar_entradas()
            self.carregar_tarefas()
        except IndexError:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para excluir.")

    def limpar_entradas(self):
        self.entrada_descricao.delete(0, tk.END)
        self.entrada_data_inicio.delete(0, tk.END)
        self.entrada_data_termino.delete(0, tk.END)

    def marcar_tarefa_como_realizada(self):
        try:
            # Obter o ID da tarefa selecionada na lista de tarefas
            selected_task_index = self.lista_tarefas.curselection()[0]
            selected_task = self.lista_tarefas.get(selected_task_index)
            task_id = selected_task.split("-")[0].strip()
            # Chamar o método correspondente no objeto Database para marcar a tarefa como realizada
            self.db.marcar_tarefa_como_realizada(task_id)
            # Atualizar a lista de tarefas na interface do usuário após marcar a tarefa como realizada
            self.carregar_tarefas()
        except IndexError:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para marcar como realizada.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoGerenciadorTarefas(root)
    root.mainloop()
