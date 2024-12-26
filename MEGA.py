"""
Mega-Sena Generator - Gerador Inteligente de Combinações para Mega-Sena
=======================================================================

Este módulo implementa um gerador inteligente de combinações para a Mega-Sena usando
o framework Streamlit. O sistema gera combinações baseadas em jogos de referência,
seguindo regras específicas de distribuição de números.

Desenvolvido por Chrystiano (https://github.com/Chrystiano)
Versão: 1.0.0-alpha
Repositório: https://github.com/Chrystiano/mega-sena-generator

Funcionalidades principais:
    - Processamento de jogos de referência em formato texto
    - Geração de novas combinações usando algoritmos inteligentes
    - Validação automática seguindo regras oficiais da Mega-Sena
    - Interface web amigável e responsiva
    - Cálculo automático do custo total da aposta

Requerimentos:
    - Python 3.11 ou superior
    - Streamlit >= 1.28.0
    - python-dateutil >= 2.8.2
    - typing >= 3.7.4
"""

import streamlit as st
import random
from datetime import datetime
from typing import List, Dict
from collections import Counter
import re


class Jogo:
    """
    Classe que representa um jogo da Mega-Sena.

    Esta classe mantém as informações de um jogo individual, incluindo os números
    escolhidos, identificador único, nome do apostador e metadados adicionais.

    Atributos:
        id (str): Identificador único do jogo (timestamp + número aleatório)
        nome (str): Nome do apostador (limitado a 50 caracteres)
        numeros (List[int]): Lista ordenada com os 6 números do jogo
        timestamp (datetime): Data e hora da criação do jogo
        metadata (Dict): Dicionário com metadados adicionais do jogo
        metricas (Dict): Dicionário com métricas calculadas do jogo

    Args:
        numeros (List[int]): Lista com os 6 números escolhidos
        nome (str, opcional): Nome do apostador. Padrão é string vazia
        metadata (Dict, opcional): Metadados adicionais. Padrão é None
    """

    def __init__(self, numeros: List[int], nome: str = "", metadata: Dict = None):
        self.id = f"{datetime.now().timestamp()}-{random.randint(1000, 9999)}"
        self.nome = nome[:50].strip()
        self.numeros = sorted(numeros)
        self.timestamp = datetime.now()
        self.metadata = metadata or {}
        self.metricas = {}

    def validar(self):
        """
        Valida se o jogo está de acordo com as regras básicas da Mega-Sena.

        Verifica:
            - Se possui exatamente 6 números
            - Se todos os números estão entre 1 e 60
            - Se não há números repetidos

        Raises:
            ValueError: Se alguma das regras for violada
        """
        if len(self.numeros) != 6:
            raise ValueError("Um jogo deve conter exatamente 6 números.")
        if not all(1 <= n <= 60 for n in self.numeros):
            raise ValueError("Todos os números devem estar no intervalo de 1 a 60.")
        if len(set(self.numeros)) != 6:
            raise ValueError("Os números de um jogo não podem se repetir.")


def validar_distribuicao(jogo: Jogo):
    """
    Valida a distribuição dos números em um jogo seguindo regras específicas.

    Regras verificadas:
        - Entre 2 e 4 números baixos (1-30)
        - Entre 2 e 4 números altos (31-60)
        - Máximo de 3 números na mesma dezena
        - Máximo de 2 números com a mesma terminação

    Args:
        jogo (Jogo): Objeto Jogo a ser validado

    Raises:
        ValueError: Se alguma regra de distribuição for violada
    """
    baixos = [n for n in jogo.numeros if 1 <= n <= 30]
    altos = [n for n in jogo.numeros if 31 <= n <= 60]

    if not (2 <= len(baixos) <= 4 and 2 <= len(altos) <= 4):
        raise ValueError("Jogo deve conter entre 2-4 números baixos e 2-4 números altos.")

    dezenas = Counter(n // 10 for n in jogo.numeros)
    if max(dezenas.values()) > 3:
        raise ValueError("Jogo não pode ter mais de 3 números da mesma dezena.")

    terminacoes = Counter(n % 10 for n in jogo.numeros)
    if max(terminacoes.values()) > 2:
        raise ValueError("Jogo não pode ter mais de 2 números com a mesma terminação.")


def gerar_combinacoes_tipo_a(jogos_referencia: List[Jogo]) -> List[Jogo]:
    """
    Retorna os jogos de referência originais sem modificações.

    Args:
        jogos_referencia (List[Jogo]): Lista de jogos originais

    Returns:
        List[Jogo]: Os mesmos jogos de referência fornecidos
    """
    return jogos_referencia


def gerar_combinacoes_tipo_b(jogos_referencia: List[Jogo], num_combinacoes: int) -> List[Jogo]:
    """
    Gera novas combinações usando apenas números dos jogos de referência.

    Esta função representa 75% dos jogos gerados automaticamente, mantendo
    padrões de distribuição dos jogos originais.

    Args:
        jogos_referencia (List[Jogo]): Lista de jogos originais
        num_combinacoes (int): Quantidade de novas combinações a serem geradas

    Returns:
        List[Jogo]: Lista com as novas combinações geradas
    """
    combinacoes = []
    numeros_referencia = [n for jogo in jogos_referencia for n in jogo.numeros]
    frequencias = Counter(numeros_referencia)

    while len(combinacoes) < num_combinacoes:
        combinacao = sorted(random.sample(numeros_referencia, 6))
        jogo = Jogo(numeros=combinacao)
        try:
            validar_distribuicao(jogo)
            combinacoes.append(jogo)
        except ValueError:
            continue

    return combinacoes


def gerar_combinacoes_tipo_c(jogos_referencia: List[Jogo], num_combinacoes: int) -> List[Jogo]:
    """
    Gera combinações explorando números que não aparecem nos jogos de referência.

    Esta função representa 25% dos jogos gerados automaticamente, combinando
    1-2 números dos jogos originais com números novos.

    Args:
        jogos_referencia (List[Jogo]): Lista de jogos originais
        num_combinacoes (int): Quantidade de novas combinações a serem geradas

    Returns:
        List[Jogo]: Lista com as novas combinações geradas
    """
    combinacoes = []
    numeros_referencia = [n for jogo in jogos_referencia for n in jogo.numeros]
    todos_numeros = set(range(1, 61))
    numeros_novos = list(todos_numeros - set(numeros_referencia))

    while len(combinacoes) < num_combinacoes:
        base = sorted(random.sample(numeros_referencia, random.randint(1, 2)))
        novos = sorted(random.sample(numeros_novos, 6 - len(base)))
        combinacao = sorted(base + novos)
        jogo = Jogo(numeros=combinacao)
        try:
            validar_distribuicao(jogo)
            combinacoes.append(jogo)
        except ValueError:
            continue

    return combinacoes


def processar_dados_entrada(conteudo: str) -> List[Jogo]:
    """
    Processa dados de entrada em formato texto para criar objetos Jogo.

    O formato esperado é:
    01 02 03 04 05 06 (Nome)
    07 08 09 10 11 12 (Outro Nome)

    Args:
        conteudo (str): Texto contendo os jogos no formato especificado

    Returns:
        List[Jogo]: Lista de objetos Jogo criados a partir do texto

    Raises:
        ValueError: Se algum jogo não estiver no formato correto
    """
    jogos = []
    linhas = conteudo.strip().split("\n")
    for linha in linhas:
        match = re.match(r"((?:\d{2}\s){5}\d{2})\s*\((.*?)\)", linha)
        if match:
            numeros = list(map(int, match.group(1).split()))
            nome = match.group(2)
            jogo = Jogo(numeros=numeros, nome=nome)
            jogo.validar()
            jogos.append(jogo)
    return jogos


# Configuração da Interface Streamlit
st.set_page_config(page_title="Gerador Mega-Sena", page_icon="🎲")
st.title("🎲 Gerador de Combinações Mega-Sena")

# Estilização CSS personalizada
st.markdown(
    """
    <style>
    .stTextArea {
        border-radius: 10px;
        border: 2px solid #4CAF50;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px 20px;
    }
    .stAlert {
        background-color: #f9f9f9;
        border-left: 5px solid #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Inicialização do estado da aplicação
if "jogos_referencia" not in st.session_state:
    st.session_state["jogos_referencia"] = []
if "multiplicador" not in st.session_state:
    st.session_state["multiplicador"] = None
if "mensagem_sucesso" not in st.session_state:
    st.session_state["mensagem_sucesso"] = False
if "reset_multiplicador" not in st.session_state:
    st.session_state["reset_multiplicador"] = False

# Campo para entrada de dados
conteudo_colado = st.text_area(
    "📋 Cole os dados no formato abaixo:",
    height=200,
    placeholder="03 08 11 14 16 29 (Janine)\n06 30 32 33 40 60 (Giselle)",
)

# Processamento dos dados
if st.button("🔄 Processar Dados"):
    try:
        jogos_referencia = processar_dados_entrada(conteudo_colado)
        st.session_state.jogos_referencia = jogos_referencia
        st.session_state.mensagem_sucesso = False
        st.success(f"✅ {len(jogos_referencia)} jogos processados com sucesso!")
    except ValueError as e:
        st.error(f"❌ Erro ao processar dados: {e}")

# Seleção do multiplicador
if st.session_state.jogos_referencia:
    st.subheader("Selecione o multiplicador de jogos:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("1x", key="mult_1x"):
            st.session_state["multiplicador"] = 1
    with col2:
        if st.button("2x", key="mult_2x"):
            st.session_state["multiplicador"] = 2
    with col3:
        if st.button("3x", key="mult_3x"):
            st.session_state["multiplicador"] = 3
    with col4:
        if st.button("4x", key="mult_4x"):
            st.session_state["multiplicador"] = 4
    with col5:
        if st.button("5x", key="mult_5x"):
            st.session_state["multiplicador"] = 5

    # Indicador visual do multiplicador selecionado
    if st.session_state["multiplicador"]:
        st.write(f"Multiplicador selecionado: {st.session_state['multiplicador']}x")
        if st.button("Resetar Multiplicador", key="reset_mult"):
            st.session_state["multiplicador"] = None
            st.experimental_rerun()

# Geração e exibição das combinações
if st.session_state.jogos_referencia and st.session_state["multiplicador"]:
    multiplicador_valor = st.session_state["multiplicador"]
    jogos_referencia = st.session_state.jogos_referencia

    total_jogos = len(jogos_referencia) * multiplicador_valor
    num_jogos_b = int(total_jogos * 0.75) - len(jogos_referencia)
    num_jogos_c = total_jogos - len(jogos_referencia) - num_jogos_b

    # Gera as combinações
    combinacoes_a = gerar_combinacoes_tipo_a(jogos_referencia)
    combinacoes_b = gerar_combinacoes_tipo_b(jogos_referencia, num_jogos_b)
    combinacoes_c = gerar_combinacoes_tipo_c(jogos_referencia, num_jogos_c)

    # Exibe as combinações do Tipo A
    st.subheader("🎯 Jogos Tipo A (Originais)")
    st.markdown("Jogos fornecidos diretamente pelos participantes.")
    col1, col2, col3 = st.columns(3)
    for i, jogo in enumerate(combinacoes_a):
        with [col1, col2, col3][i % 3]:
            st.write(f"{jogo.nome}: " + " ".join(map(lambda x: f"{x:02}", jogo.numeros)))

    # Exibe as combinações do Tipo B
    st.subheader("🎯 Jogos Tipo B (75%)")
    st.markdown("Combinações geradas com base nos jogos de referência.")
    col1, col2, col3 = st.columns(3)
    for i, jogo in enumerate(combinacoes_b):
        with [col1, col2, col3][i % 3]:
            st.write(" ".join(map(lambda x: f"{x:02}", jogo.numeros)))

    # Exibe as combinações do Tipo C
    st.subheader("🎯 Jogos Tipo C (25%)")
    st.markdown("Combinações exploratórias com novos números.")
    col1, col2, col3 = st.columns(3)
    for i, jogo in enumerate(combinacoes_c):
        with [col1, col2, col3][i % 3]:
            st.write(" ".join(map(lambda x: f"{x:02}", jogo.numeros)))

    # Exibe o custo total
    total_custo = total_jogos * 5
    st.markdown(f"**💰 Custo Total da Aposta: R$ {total_custo},00**")

    # Gera arquivo com todos os jogos
    all_games = []
    
    # Adiciona jogos tipo A com nomes
    for jogo in combinacoes_a:
        all_games.append(f"{' '.join(map(lambda x: f'{x:02}', jogo.numeros))} ({jogo.nome})")
    
    # Adiciona jogos tipo B
    for jogo in combinacoes_b:
        all_games.append(f"{' '.join(map(lambda x: f'{x:02}', jogo.numeros))}")
    
    # Adiciona jogos tipo C
    for jogo in combinacoes_c:
        all_games.append(f"{' '.join(map(lambda x: f'{x:02}', jogo.numeros))}")

    # Cria o conteúdo do arquivo
    file_content = "\n".join(all_games)

    # Botão de download
    st.download_button(
        label="📥 Baixar Todos os Jogos",
        data=file_content,
        file_name="mega_sena_jogos.txt",
        mime="text/plain",
        key="download_button"
    )

    if st.session_state.mensagem_sucesso:
        st.success("✅ Arquivo gerado com sucesso! Boa sorte e que os números estejam ao seu favor! 🍀🎉")
