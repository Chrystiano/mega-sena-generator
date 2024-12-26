import streamlit as st
import random
from datetime import datetime
from typing import List, Dict
from collections import Counter
import re

# Estruturas de Dados
class Jogo:
    def __init__(self, numeros: List[int], nome: str = "", metadata: Dict = None):
        self.id = f"{datetime.now().timestamp()}-{random.randint(1000, 9999)}"
        self.nome = nome[:50].strip()
        self.numeros = sorted(numeros)
        self.timestamp = datetime.now()
        self.metadata = metadata or {}
        self.metricas = {}

    def validar(self):
        if len(self.numeros) != 6:
            raise ValueError("Um jogo deve conter exatamente 6 números.")
        if not all(1 <= n <= 60 for n in self.numeros):
            raise ValueError("Todos os números devem estar no intervalo de 1 a 60.")
        if len(set(self.numeros)) != 6:
            raise ValueError("Os números de um jogo não podem se repetir.")

# Funções de Validação Auxiliares

def validar_distribuicao(jogo: Jogo):
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

# Funções de Geração

def gerar_combinacoes_tipo_a(jogos_referencia: List[Jogo]):
    return jogos_referencia

def gerar_combinacoes_tipo_b(jogos_referencia: List[Jogo], num_combinacoes: int):
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

def gerar_combinacoes_tipo_c(jogos_referencia: List[Jogo], num_combinacoes: int):
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

# Função para processar dados de entrada

def processar_dados_entrada(conteudo: str) -> List[Jogo]:
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

# Interface Streamlit
st.set_page_config(page_title="Gerador Mega-Sena", page_icon="🎲")
st.title("🎲 Gerador de Combinações Mega-Sena")

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

# Resetar estado ao iniciar
if "jogos_referencia" not in st.session_state:
    st.session_state["jogos_referencia"] = []
if "multiplicador" not in st.session_state:
    st.session_state["multiplicador"] = None
if "mensagem_sucesso" not in st.session_state:
    st.session_state["mensagem_sucesso"] = False

conteudo_colado = st.text_area(
    "📋 Cole os dados no formato abaixo:",
    height=200,
    placeholder="03 08 11 14 16 29 (Janine)\n06 30 32 33 40 60 (Giselle)",
)

if st.button("🔄 Processar Dados"):
    try:
        jogos_referencia = processar_dados_entrada(conteudo_colado)
        st.session_state.jogos_referencia = jogos_referencia
        st.session_state.mensagem_sucesso = False
        st.success(f"✅ {len(jogos_referencia)} jogos processados com sucesso!")
    except ValueError as e:
        st.error(f"❌ Erro ao processar dados: {e}")

if st.session_state.jogos_referencia:
    st.subheader("Selecione o multiplicador de jogos:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("1x"):
            st.session_state["multiplicador"] = 1
    with col2:
        if st.button("2x"):
            st.session_state["multiplicador"] = 2
    with col3:
        if st.button("3x"):
            st.session_state["multiplicador"] = 3
    with col4:
        if st.button("4x"):
            st.session_state["multiplicador"] = 4
    with col5:
        if st.button("5x"):
            st.session_state["multiplicador"] = 5

if st.session_state.jogos_referencia and st.session_state["multiplicador"]:
    multiplicador_valor = st.session_state["multiplicador"]
    jogos_referencia = st.session_state.jogos_referencia

    total_jogos = len(jogos_referencia) * multiplicador_valor
    num_jogos_b = int(total_jogos * 0.75) - len(jogos_referencia)
    num_jogos_c = total_jogos - len(jogos_referencia) - num_jogos_b

    combinacoes_a = gerar_combinacoes_tipo_a(jogos_referencia)
    combinacoes_b = gerar_combinacoes_tipo_b(jogos_referencia, num_jogos_b)
    combinacoes_c = gerar_combinacoes_tipo_c(jogos_referencia, num_jogos_c)

    st.subheader("🎯 Jogos Tipo A (Originais)")
    st.markdown("Jogos fornecidos diretamente pelos participantes.")
    col1, col2, col3 = st.columns(3)
    for i, jogo in enumerate(combinacoes_a):
        with [col1, col2, col3][i % 3]:
            st.write(" ".join(map(lambda x: f"{x:02}", jogo.numeros)))

    st.subheader("🎯 Jogos Tipo B (75%)")
    st.markdown("Combinações geradas com base nos jogos de referência.")
    col1, col2, col3 = st.columns(3)
    for i, jogo in enumerate(combinacoes_b):
        with [col1, col2, col3][i % 3]:
            st.write(" ".join(map(lambda x: f"{x:02}", jogo.numeros)))

    st.subheader("🎯 Jogos Tipo C (25%)")
    st.markdown("Combinações exploratórias com novos números.")
    col1, col2, col3 = st.columns(3)
    for i, jogo in enumerate(combinacoes_c):
        with [col1, col2, col3][i % 3]:
            st.write(" ".join(map(lambda x: f"{x:02}", jogo.numeros)))

    all_games = "\n".join(" ".join(map(lambda x: f"{x:02}", jogo.numeros)) for jogo in combinacoes_a + combinacoes_b + combinacoes_c)

    download_button = st.download_button(
        label="📥 Baixar Todos os Jogos",
        data=all_games,
        file_name="todos_os_jogos.txt",
        mime="text/plain"
    )

    if download_button:
        st.session_state.mensagem_sucesso = True

if st.session_state.mensagem_sucesso:
    st.success("✅ Arquivo gerado com sucesso! Obrigado por utilizar nossa solução! 🎉")
