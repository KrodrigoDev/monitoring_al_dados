import streamlit as st


def config_pagina(titulo_pagina, layout_pagina='wide', estado_menu='expanded'):
    """

    :param estado_menu: Estado inicial da sidebar ('auto', 'expanded', 'collapsed')
    :param layout_pagina: Define o layout ('centered' ou 'wide')
    :param titulo_pagina: Define o título da aba do navegador
    :return:
    """
    st.set_page_config(
        page_title=titulo_pagina,
        layout=layout_pagina,
        initial_sidebar_state=estado_menu,
        menu_items={  # Personaliza o menu superior direito
            'Get Help': 'https://docs.streamlit.io/',
            'Report a bug': 'https://github.com/streamlit/streamlit/issues',
            'About': 'Minha Aplicação - Versão 1.0'
        }
    )
