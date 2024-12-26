# 🎲 Mega-Sena Generator

[English](README-en.md) | Português

![Python Package](https://img.shields.io/badge/python-100%25-blue)
![Version](https://img.shields.io/badge/version-1.0.0--alpha-green)
![Status](https://img.shields.io/badge/status-development-orange)

## Sobre o Projeto

> ⚠️ **Status**: Versão 1.0.0alpha - Em desenvolvimento

Um aplicativo web desenvolvido com Streamlit para gerar combinações inteligentes de apostas na Mega-Sena, baseado em jogos de referência fornecidos pelos usuários.

## 📋 Funcionalidades

- Processamento de jogos de referência em formato texto
- Geração de novas combinações usando algoritmos inteligentes
- Validação automática seguindo regras oficiais da Mega-Sena
- Interface web amigável e responsiva
- Download das combinações geradas em arquivo texto
- Cálculo automático do custo total da aposta

## 🚀 Começando

### Pré-requisitos

- Python 3.6 ou superior
- pip (gerenciador de pacotes Python)

### 🔧 Instalação

1. Clone este repositório:
```bash
git clone https://github.com/Chrystiano/mega-sena-generator.git
cd mega-sena-generator
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
streamlit run MEGA.py
```

## 📖 Como Usar

1. Acesse a aplicação pelo navegador (geralmente em http://localhost:8501)

2. Cole seus jogos de referência no formato:
```
01 02 03 04 05 06 (Nome)
07 08 09 10 11 12 (Outro Nome)
```

3. Clique em "Processar Dados"

4. Escolha um multiplicador (1x a 5x)

5. Visualize as combinações geradas:
   - Tipo A: Jogos originais
   - Tipo B: Combinações baseadas nos números existentes
   - Tipo C: Combinações com números novos

6. Faça download do arquivo com todos os jogos

## 🎯 Regras de Distribuição

O sistema gera combinações seguindo regras específicas para aumentar as chances:

- Entre 2 e 4 números baixos (1-30)
- Entre 2 e 4 números altos (31-60)
- Máximo de 3 números na mesma dezena
- Máximo de 2 números com a mesma terminação

## 💻 Tecnologias Utilizadas

- [Python](https://www.python.org/) - Linguagem de programação
- [Streamlit](https://streamlit.io/) - Framework web
- [Datetime](https://docs.python.org/3/library/datetime.html) - Manipulação de datas
- [Random](https://docs.python.org/3/library/random.html) - Geração de números aleatórios
- [Collections](https://docs.python.org/3/library/collections.html) - Estruturas de dados avançadas

## 📊 Estrutura do Projeto

```
mega-sena-generator/
├── MEGA.py              # Aplicação principal
├── requirements.txt      # Dependências do projeto
├── README.md            # Este arquivo
└── .gitignore           # Arquivos ignorados pelo git
```

## 🔍 Como Funciona

O sistema divide a geração de jogos em três categorias:

1. **Tipo A (Originais)**
   - Mantém os jogos fornecidos pelos usuários

2. **Tipo B (75% dos jogos gerados)**
   - Gera novas combinações usando apenas números dos jogos de referência
   - Mantém padrões de distribuição dos jogos originais

3. **Tipo C (25% dos jogos gerados)**
   - Explora números que não aparecem nos jogos de referência
   - Combina 1-2 números dos jogos originais com números novos

## ⚠️ Limitações

- Aceita apenas o formato específico de entrada
- Não persiste dados entre sessões
- Não verifica duplicação entre jogos gerados
- Interface limitada às funcionalidades do Streamlit

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## ✨ Agradecimentos

- Aos usuários que ajudaram a testar e melhorar o sistema
- À comunidade Python e Streamlit por ferramentas incríveis
- A todos que contribuíram com sugestões e melhorias

---
⌨️ com ❤️ por [Chrys](https://github.com/Chrystiano) 😊
