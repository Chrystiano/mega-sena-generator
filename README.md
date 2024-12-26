# Gerador de Jogos Mega-Sena 🎲

![Python](https://img.shields.io/badge/Python-100%25-14354C.svg?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![Versão](https://img.shields.io/badge/Versão-1.0.0--alpha-blue)
![Licença](https://img.shields.io/badge/Licença-MIT-green)

> Um gerador inteligente de combinações para a Mega-Sena que cria jogos baseados em referências fornecidas, seguindo regras específicas de distribuição e garantindo que não haja duplicações.

## 📚 Índice

- [Funcionalidades](#-funcionalidades)
- [Demonstração](#-demonstração)
- [Como Usar](#-como-usar)
- [Tecnologias](#-tecnologias)
- [Como Funciona](#-como-funciona)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Contato](#-contato)

## 🚀 Funcionalidades

- **Processamento Inteligente**: Analisa jogos de referência para gerar novas combinações
- **Validação Automática**: Segue as regras oficiais da Mega-Sena
- **Prevenção de Duplicatas**: Garante que cada combinação seja única
- **Interface Amigável**: Design intuitivo e responsivo
- **Distribuição Otimizada**: 
  - 2-4 números baixos (1-30)
  - 2-4 números altos (31-60)
  - Máximo 3 números por dezena
  - Máximo 2 números com mesma terminação
- **Exportação Simples**: Download de todas as combinações em formato texto

## 🎥 Demonstração

## 🎮 Como Usar

1. **Prepare seus Jogos de Referência**
   ```
   01 02 03 04 05 06 (Nome)
   07 08 09 10 11 12 (Outro Nome)
   ```

2. **Cole os Jogos**
   - Cole seus jogos no campo de texto
   - Clique em "Processar Dados"

3. **Escolha o Multiplicador**
   - Selecione de 1x a 5x para determinar quantos jogos serão gerados

4. **Veja os Resultados**
   - Jogos Tipo A: Seus jogos originais
   - Jogos Tipo B: Baseados nos seus números (75%)
   - Jogos Tipo C: Explorando novos números (25%)

5. **Baixe as Combinações**
   - Use o botão "Baixar Todos os Jogos"
   - Arquivo gerado em formato texto simples

## 💻 Tecnologias

- ![Python](https://img.shields.io/badge/-Python-14354C?style=flat&logo=python) **Python** - Linguagem principal
- ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white) **Streamlit** - Interface web
- **Bibliotecas Principais**:
  - `datetime`: Manipulação de datas
  - `random`: Geração de números aleatórios
  - `typing`: Tipagem estática
  - `collections`: Estruturas de dados avançadas

## 🔍 Como Funciona

### Tipos de Jogos

1. **Tipo A (Originais)**
   - Mantém seus jogos exatamente como fornecidos
   - Serve como base para análise de padrões

2. **Tipo B (75% dos Jogos)**
   - Usa apenas números que apareceram nos jogos originais
   - Mantém os padrões de distribuição encontrados

3. **Tipo C (25% dos Jogos)**
   - Explora números que não apareceram nos jogos originais
   - Combina 1-2 números dos jogos originais com números novos

### Sistema de Validação

- Verifica regras básicas da Mega-Sena
- Aplica regras de distribuição personalizadas
- Garante que não existam jogos duplicados
- Controla a proporção entre números baixos e altos

## 🤝 Contribuindo

1. Faça um Fork
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas alterações (`git commit -m 'Add: nova funcionalidade'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Requisitos para Pull Requests

- Código documentado
- Testes incluídos (quando aplicável)
- Descrição clara das alterações

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📫 Contato

Chrystiano - [@Chrystiano](https://github.com/Chrystiano)

Link do Projeto: [https://github.com/Chrystiano/mega-sena-generator](https://github.com/Chrystiano/mega-sena-generator)

---

⌨️ com 💙 por [Chrys](https://github.com/Chrystiano)
