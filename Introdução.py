import streamlit as st
from scripts.configuracoes_gerais import config_pagina

config_pagina('Introdução')

# Título principal e subheader
st.header('Introdução às métricas')

# Texto explicativo
st.write("""
O conteúdo abaixo é uma breve explicação das métricas que serão observadas na página do 
Painel, por isso é de suma importância o entendimento do mesmo.

---
""")

# Subtítulo
st.subheader('Estrutura do Alagoas em Dados')
st.caption(
    '**Fonte**: [Medium - Explorando o CKAN](https://medium.com/@kauanrodrigoo25/explorando-o-ckan-a-plataforma-open'
    '-source-para-cataloga%C3%A7%C3%A3o-de-dados-2f707a4c56fa)')

# Descrição sobre a estrutura do portal
st.write("""
A estrutura de dados do portal **Alagoas em Dados** é organizada de forma hierárquica para garantir **facilidade no acesso e na gestão**. Abaixo estão os principais componentes dessa organização:

1. **Organizações**:  
   Entidades responsáveis pelo controle e gestão dos dados. Cada organização pode ter diversos pacotes e recursos.

2. **Pacotes**:  
   Grupos de conjuntos de dados relacionados. Pacotes podem conter vários recursos, sendo uma maneira de organizar dados em categorias mais amplas.

3. **Recursos**:  
   Os dados propriamente ditos, que podem ser armazenados como arquivos (CSV, JSON, etc.) ou links para APIs externas, proporcionando o acesso direto aos dados.

---
""")

# Subtítulo para métricas do Google Analytics
st.subheader("Métricas do Google Analytics 4")

st.caption(
    '**Fonte**: [AS 9 PRINCIPAIS MÉTRICAS do Google Analytics 4 (GA4)]('
    'https://www.youtube.com/watch?v=QUZwnK-rwoc&t=3s&ab_channel=M2up)')

# Descrição das métricas
st.write("""
A seguir, apresentamos algumas das métricas coletadas do **Google Analytics 4 (GA4)** e sua importância na análise de dados:

- **Usuários Ativos**:  
  Representa o número de usuários únicos que interagiram com o site durante o período analisado. Indica o engajamento geral da plataforma.

- **Novos Usuários**:  
  Número de usuários que acessaram o site pela primeira vez no período. Ajuda a avaliar o crescimento da audiência.

- **Sessões**:  
  Contagem de interações realizadas pelos usuários dentro de um intervalo de tempo. Se um usuário retornar após 30 minutos de inatividade, é contada uma nova sessão.

- **Sessões Engajadas**:  
  Sessões onde o usuário permaneceu por mais de 10 segundos, realizou um evento conversão ou visualizou pelo menos duas páginas.

- **Taxa de Engajamento**:  
  Percentual de sessões engajadas em relação ao total de sessões. Uma taxa alta indica que os usuários estão interagindo ativamente com o conteúdo.

- **Páginas Visualizadas**:  
  Quantidade total de páginas visitadas pelos usuários, contando acessos repetidos à mesma página.

- **Eventos**:  
  Número total de interações registradas, como cliques, downloads, rolagens de página e outras ações configuradas no GA4.
""")
