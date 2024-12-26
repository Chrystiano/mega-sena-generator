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
"""

import streamlit as st
import random
from datetime import datetime
from typing import List, Dict, Optional, Set
from collections import Counter
import re


class Jogo:
    """
    Classe que representa um jogo da Mega-Sena.

    Esta classe mantém as informações de um jogo individual, incluindo os números
    escolhidos, identificador único, nome do apostador e metadados adicionais.
    Implementa as funções necessárias para comparação e uso em estruturas de dados.

    Atributos:
        id (str): Identificador único do jogo (timestamp + número aleatório)
        nome (str): Nome do apostador (limitado a 50 caracteres)
        numeros (List[int]): Lista ordenada com os 6 números do jogo
        timestamp (datetime): Data e hora da criação do jogo
        metadata (Dict): Dicionário com metadados adicionais do jogo
        metricas (Dict): Dicionário com métricas calculadas do jogo
    """

    def __init__(self, numeros: List[int], nome: str = "", metadata: Dict = None):
        self.id = f"{datetime.now().timestamp()}-{random.randint(1000, 9999)}"
        self.nome = nome[:50].strip()
        self.numeros = sorted(numeros)
        self.timestamp = datetime.now()
        self.metadata = metadata or {}
        self.metricas = {}

    def __hash__(self):
        """Permite uso do objeto em sets e como chave em dicionários."""
        return hash(tuple(self.numeros))

    def __eq__(self, other):
        """Define quando dois jogos são considerados iguais."""
        if not isinstance(other, Jogo):
            return False
        return set(self.numeros) == set(other.numeros)

    def validar(self):
        """
        Valida se o jogo está de acordo com as regras básicas da Mega-Sena.

        Raises:
            ValueError: Se alguma regra básica for violada
        """
        if len(self.numeros) != 6:
            raise ValueError("Um jogo deve conter exatamente 6 números.")
        if not all(1 <= n <= 60 for n in self.numeros):
            raise ValueError("Todos os números devem estar no intervalo de 1 a 60.")
        if len(set(self.numeros)) != 6:
            raise ValueError("Os números de um jogo não podem se repetir.")


class GeradorJogos:
    """
    Classe para gerenciar a geração de jogos únicos.

    Esta classe mantém controle de todos os jogos gerados e fornece métodos
    para garantir a unicidade das combinações.

    Attributes:
        jogos_gerados (Set[Jogo]): Conjunto de todos os jogos já gerados
    """

    def __init__(self):
        self.jogos_gerados: Set[Jogo] = set()

    def adicionar_jogo(self, jogo: Jogo) -> bool:
        """
        Adiciona um jogo ao conjunto de jogos gerados se ele não existir.
        
        Args:
            jogo (Jogo): O jogo a ser adicionado

        Returns:
            bool: True se o jogo foi adicionado, False se já existia
        """
        if jogo in self.jogos_gerados:
            return False
        self.jogos_gerados.add(jogo)
        return True

    def gerar_combinacao_unica(
        self, 
        numeros_disponiveis: List[int], 
        tamanho: int = 6, 
        max_tentativas: int = 1000
    ) -> Optional[Jogo]:
        """
        Gera uma combinação única de números.
        
        Args:
            numeros_disponiveis (List[int]): Lista de números disponíveis para sorteio
            tamanho (int): Quantidade de números em cada combinação
            max_tentativas (int): Número máximo de tentativas antes de desistir

        Returns:
            Optional[Jogo]: Novo jogo único ou None se não for possível gerar
        """
        tentativas = 0
        while tentativas < max_tentativas:
            combinacao = sorted(random.sample(numeros_disponiveis, tamanho))
            jogo = Jogo(numeros=combinacao)
            try:
                validar_distribuicao(jogo)
                if self.adicionar_jogo(jogo):
                    return jogo
            except ValueError:
                pass
            tentativas += 1
        return None


def validar_distribuicao(jogo: Jogo):
    """
    Valida a distribuição dos números em um jogo seguindo regras específicas.

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


def gerar_combinacoes_tipo_a(jogos_referencia: List[Jogo], gerador: GeradorJogos) -> List[Jogo]:
    """
    Retorna os jogos de referência originais, registrando-os no gerador.

    Args:
        jogos_referencia (List[Jogo]): Lista de jogos originais
        gerador (GeradorJogos): Instância do gerador para controle de unicidade

    Returns:
        List[Jogo]: Os mesmos jogos de referência fornecidos
    """
    for jogo in jogos_referencia:
        gerador.adicionar_jogo(jogo)
    return jogos_referencia


def gerar_combinacoes_tipo_b(
    jogos_referencia: List[Jogo], 
    num_combinacoes: int, 
    gerador: GeradorJogos
) -> List[Jogo]:
    """
    Gera combinações tipo B garantindo unicidade.

    Args:
        jogos_referencia (List[Jogo]): Lista de jogos originais
        num_combinacoes (int): Quantidade de novas combinações a serem geradas
        gerador (GeradorJogos): Instância do gerador para controle de unicidade

    Returns:
        List[Jogo]: Lista com as novas combinações geradas
    """
    combinacoes = []
    numeros_referencia = [n for jogo in jogos_referencia for n in jogo.numeros]
    
    while len(combinacoes) < num_combinacoes:
        jogo = gerador.gerar_combinacao_unica(numeros_referencia)
        if jogo:
            combinacoes.append(jogo)
        else:
            st.warning(f"⚠️ Não foi possível gerar mais combinações únicas do tipo B. Geradas {len(combinacoes)} de {num_combinacoes}.")
            break
    
    return combinacoes


def gerar_combinacoes_tipo_c(
    jogos_referencia: List[Jogo], 
    num_combinacoes: int, 
    gerador: GeradorJogos
) -> List[Jogo]:
    """
    Gera combinações tipo C garantindo unicidade.

    Args:
        jogos_referencia (List[Jogo]): Lista de jogos originais
        num_combinacoes (int): Quantidade de novas combinações a serem geradas
        gerador (GeradorJogos): Instância do gerador para controle de unicidade

    Returns:
        List[Jogo]: Lista com as novas combinações geradas
    """
    combinacoes = []
    numeros_referencia = [n for jogo in jogos_referencia for n in jogo.numeros]
    todos_numeros = set(range(1, 61))
    numeros_novos = list(todos_numeros - set(numeros_referencia))
    
    while len(combinacoes) < num_combinacoes:
        base = random.sample(numeros_referencia, random.randint(1, 2))
        novos = random.sample(numeros_novos, 6 - len(base))
        jogo = Jogo(numeros=sorted(base + novos))
        
        try:
            validar_distribuicao(jogo)
            if gerador.adicionar_jogo(jogo):
                combinacoes.append(jogo)
        except ValueError:
            continue
            
        if len(combinacoes) < num_combinacoes and not novos:
            st.warning(f"⚠️ Não foi possível gerar mais combinações únicas do tipo C. Geradas {len(combinacoes)} de {num_combinacoes}.")
            break
    
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

# Geração e exibição das combinações
if st.session_state.jogos_referencia and st.session_state["multiplicador"]:
    multiplicador_valor = st.session_state["multiplicador"]
    jogos_referencia = st.session_state.jogos_referencia
    gerador = GeradorJogos()  # Cria instância única do gerador

    total_jogos = len(jogos_referencia) * multiplicador_valor
    num_jogos_b = int(total_jogos * 0.75) - len(jogos_referencia)
    num_jogos_c = total_jogos - len(jogos_referencia) - num_jogos_b

    # Gera as combinações usando o mesmo gerador para garantir unicidade global
    combinacoes_a = gerar_combinacoes_tipo_a(jogos_referencia, gerador)
    combinacoes_b = gerar_combinacoes_tipo_b(jogos_referencia, num_jogos_b, gerador)
    combinacoes_c = gerar_combinacoes_tipo_c(jogos_referencia, num_jogos_c, gerador)

    # Verifica o total de jogos gerados
    todos_jogos = combinacoes_a + combinacoes_b + combinacoes_c
    
    if len(todos_jogos) < total_jogos:
        st.warning(f"⚠️ Foram gerados {len(todos_jogos)} jogos únicos dos {total_jogos} solicitados.")
    
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
    total_custo = len(todos_jogos) * 5
    st.markdown(f"**💰 Custo Total da Aposta: R$ {total_custo},00**")

    # Gera arquivo com todos os jogos
    all_games = []
    for jogo in todos_jogos:
        all_games.append(" ".join(map(lambda x: f"{x:02}", jogo.numeros)))

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
        st.success("✅ Arquivo gerado com sucesso! Boa sorte! 🍀🎉")
