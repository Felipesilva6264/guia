from pdf_generator import generate_pdf

def test_generate_pdf():
    content_dict = {
        'nome_completo': 'João da Silva',
        'endereco': 'Rua das Flores, 123, Cidade - Estado',
        'contato': 'Telefone: (11) 99999-9999',
        'sections': {
            'COMPETÊNCIAS': 'Experiência em Python, análise de dados e machine learning.',
            'EXPERIÊNCIA PROFISSIONAL': 'Desenvolvedor de Software na Empresa X (Jan 2020 - Presente).',
            'ESCOLARIDADE': 'Bacharel em Ciência da Computação pela Universidade Y.',
            'CURSOS COMPLEMENTARES': 'Certificação em Data Science pela Plataforma Z.',
            'INFORMAÇÕES ADICIONAIS': 'Carteira de Habilitação: Categoria B, Registro ativo no CRP.'
        }
    }

    file_path = 'teste_curriculo.pdf'
    generate_pdf(content_dict, file_path)
    print(f'PDF gerado com sucesso: {file_path}')

if __name__ == "__main__":
    test_generate_pdf()
