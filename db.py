import sqlite3

def create_tables():
    # Criação das tabelas
    tables = {
        'vagas.db': """
            CREATE TABLE IF NOT EXISTS vagas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cargo TEXT,
                tarefas TEXT,
                requisitos TEXT
            )
        """,
        'dados_pessoais.db': """
            CREATE TABLE IF NOT EXISTS dados_pessoais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT,
                endereco TEXT,
                email TEXT,
                telefone TEXT
            )
        """,
        'experiencia.db': """
            CREATE TABLE IF NOT EXISTS experiencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empresa TEXT,
                cargo TEXT,
                data_inicio TEXT,
                data_fim TEXT,
                competencias TEXT,
                comentario TEXT
            )
        """,
        'educacao.db': """
            CREATE TABLE IF NOT EXISTS educacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instituicao TEXT,
                curso TEXT,
                data_inicio TEXT,
                status TEXT
            )
        """,
        'complementos.db': """
            CREATE TABLE IF NOT EXISTS complementos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                curso TEXT,
                descricao TEXT,
                data_inicio TEXT,
                status TEXT
            )
        """
    }

    for db_file, create_table_sql in tables.items():
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()

def save_responses(self):
    with sqlite3.connect('dados_pessoais.db') as conn:
        cursor = conn.cursor()
        # Recria a tabela com todas as colunas necessárias
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


if __name__ == "__main__":
    create_tables()
