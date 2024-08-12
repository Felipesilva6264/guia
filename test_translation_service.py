import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pdf_generator import generate_pdf
from translation_service import TranslationService

class CurriculumGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gerador de Currículos")

        self.language_var = tk.StringVar(value='en')  # Valor padrão para a língua

        self.create_widgets()

    def create_widgets(self):
        self.create_form()
        self.create_export_options()
        self.create_generate_button()

    def create_form(self):
        self.form_frame = ttk.Frame(self.root, padding="10")
        self.form_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.form_frame, text="Nome Completo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.form_frame, width=40)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.form_frame, text="Endereço:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.address_entry = ttk.Entry(self.form_frame, width=40)
        self.address_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.form_frame, text="Contato:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.contact_entry = ttk.Entry(self.form_frame, width=40)
        self.contact_entry.grid(row=2, column=1, pady=5)

    def create_export_options(self):
        self.export_frame = ttk.Frame(self.root, padding="10")
        self.export_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.export_frame, text="Escolha o idioma:").grid(row=0, column=0, sticky=tk.W, pady=5)

        languages = {'Inglês': 'en', 'Espanhol': 'es', 'Francês': 'fr', 'Alemão': 'de', 'Português': 'pt'}
        for idx, (text, value) in enumerate(languages.items()):
            ttk.Radiobutton(self.export_frame, text=text, variable=self.language_var, value=value).grid(row=1, column=idx, padx=5, pady=5)

    def create_generate_button(self):
        self.generate_button = ttk.Button(self.root, text="Gerar Currículo", command=self.generate_curriculum)
        self.generate_button.grid(row=2, column=0, pady=10)

    def generate_curriculum(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        contact = self.contact_entry.get()
        language = self.language_var.get()

        content_dict = {
            'nome_completo': name,
            'endereco': address,
            'contato': contact,
            'sections': {
                'COMPETÊNCIAS': 'Resumo das competências e habilidades.',
                'EXPERIÊNCIA PROFISSIONAL': 'Detalhes da experiência profissional.',
                'ESCOLARIDADE': 'Informações sobre a formação acadêmica.',
                'CURSOS COMPLEMENTARES': 'Cursos adicionais realizados.',
                'INFORMAÇÕES ADICIONAIS': 'Informações como habilitação e registro.'
            }
        }

        translator = TranslationService()
        translated_content = translator.translate_curriculum(content_dict, language)
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            generate_pdf(translated_content, file_path)
            tk.messagebox.showinfo("Sucesso", f"Currículo gerado com sucesso: {file_path}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CurriculumGenerator()
    app.run()

