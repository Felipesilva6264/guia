import tkinter as tk
from tkinter import ttk
import sqlite3

class FormWindow(tk.Toplevel):
    def __init__(self, master, title, fields, db_file, next_window):
        super().__init__(master)
        self.title(title)
        self.fields = fields
        self.db_file = db_file
        self.next_window = next_window
        self.entries = {}

        self.create_widgets()

    def create_widgets(self):
        row = 0
        for field in self.fields:
            ttk.Label(self, text=field).grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(self, width=40)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.entries[field] = entry
            row += 1

        ttk.Button(self, text="Continuar", command=self.save_and_next).grid(row=row, column=1, pady=10, sticky=tk.E)

    def save_and_next(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        self.save_to_db(data)
        self.destroy()
        if self.next_window:
            self.next_window()

    def save_to_db(self, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {self.get_table_name()} ({columns}) VALUES ({placeholders})", tuple(data.values()))
            conn.commit()

    def get_table_name(self):
        # Mapeia o arquivo do banco de dados para o nome da tabela
        mapping = {
            'vagas.db': 'vagas',
            'dados_pessoais.db': 'dados_pessoais',
            'experiencia.db': 'experiencia',
            'educacao.db': 'educacao',
            'complementos.db': 'complementos'
        }
        return mapping[self.db_file]

class ChatWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Chat com Guia")
        self.geometry("600x400")
        self.create_widgets()
        
        # Inicializar o estado do chat
        self.current_step = 0
        self.responses = {}
        self.steps = [
            ("Qual o seu nome completo?", "nome"),
            ("Qual seu endereço, incluindo rua, cidade, estado e país?", "endereco"),
            ("Você tem e-mail? Se sim, qual é o endereço?", "email"),
            ("Telefone para contato?", "telefone"),
            ("Qual o nome da última empresa que trabalhou?", "empresa"),
            ("Qual foi o seu cargo?", "cargo"),
            ("Quando começou (mês e ano)?", "data_inicio"),
            ("Ainda está nessa empresa? (S/N)", "emprego_atual"),
            ("Qual a data de término? (se aplicável)", "data_fim"),
            ("Quais eram suas responsabilidades?", "responsabilidades"),
            ("Gostaria de fazer um comentário sobre essa experiência?", "comentario"),
            ("Qual o nome da instituição da sua última formação?", "instituicao"),
            ("Qual o nome do curso?", "curso"),
            ("Quando começou?", "curso_inicio"),
            ("Já terminou? (S/N)", "curso_concluido"),
            ("Tem cursos complementares? Faça aqui uma breve descrição.", "cursos_complementares"),
            ("Qual a data de início dos cursos complementares?", "cursos_inicio"),
            ("Já terminou? (S/N)", "cursos_concluidos"),
            ("Gostaria de adicionar outra experiência?", "adicionar_outra_experiencia"),
            ("Gostaria de adicionar outra formação?", "adicionar_outra_formacao"),
            ("Forneça suas informações adicionais.", "informacoes_adicionais"),
        ]
        self.prompt_user()

    def create_widgets(self):
        self.chat_area = tk.Text(self, state='disabled', width=70, height=15)
        self.chat_area.pack(pady=10)
        self.user_input = ttk.Entry(self, width=70)
        self.user_input.pack(pady=5)
        self.send_button = ttk.Button(self, text="Enviar", command=self.handle_message)
        self.send_button.pack(pady=5)

    def prompt_user(self):
        if self.current_step < len(self.steps):
            question, field = self.steps[self.current_step]
            self.display_message(question)
        else:
            self.display_message("Obrigado! Todas as informações foram coletadas.")
            # Você pode adicionar um botão para gerar o PDF ou visualizar o resumo aqui

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"Guia: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def handle_message(self):
        user_message = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)
        self.responses[self.steps[self.current_step][1]] = user_message

        self.display_message(f"Você: {user_message}")
        self.current_step += 1

        if self.current_step == len(self.steps):
            self.save_responses()
            self.prompt_user()
        else:
            self.prompt_user()

    def save_responses(self):
        with sqlite3.connect('dados_pessoais.db') as conn:
            cursor = conn.cursor()
            # Cria a tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dados_pessoais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    endereco TEXT,
                    email TEXT,
                    telefone TEXT,
                    empresa TEXT,
                    cargo TEXT,
                    data_inicio TEXT,
                    emprego_atual TEXT,
                    data_fim TEXT,
                    responsabilidades TEXT,
                    comentario TEXT,
                    instituicao TEXT,
                    curso TEXT,
                    curso_inicio TEXT,
                    curso_concluido TEXT,
                    cursos_complementares TEXT,
                    cursos_inicio TEXT,
                    cursos_concluidos TEXT,
                    adicionar_outra_experiencia TEXT,
                    adicionar_outra_formacao TEXT,
                    informacoes_adicionais TEXT
                )
            ''')

            columns = ', '.join(self.responses.keys())
            placeholders = ', '.join(['?'] * len(self.responses))
            cursor.execute(f"INSERT INTO dados_pessoais ({columns}) VALUES ({placeholders})", tuple(self.responses.values()))
            conn.commit()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Currículo")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        # Configuração da Barra Superior
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Versões", command=self.show_versions)
        file_menu.add_command(label="Histórico de Alterações", command=self.show_history)

        # Botão para iniciar o formulário
        ttk.Button(self, text="Iniciar Formulário", command=self.start_form).pack(pady=20)

    def show_versions(self):
        # Implementar a exibição das versões
        pass

    def show_history(self):
        # Implementar a exibição do histórico de alterações
        pass

    def start_form(self):
        FormWindow(self, "Descrição da Vaga", ["Cargo", "Tarefas", "Requisitos"], "vagas.db", self.open_chat)

    def open_chat(self):
        ChatWindow(self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
