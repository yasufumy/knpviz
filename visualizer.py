from unittest.mock import patch

import camphr
import streamlit as st

from knpviz.pyknp_patch import Subprocess
from knpviz.utils import (bunsetsu_list_to_dependency_data,
                          bunsetsu_spans_to_dependency_data,
                          tag_spans_to_graph, visualize_dependency,
                          visualize_tokens)


@st.cache(allow_output_mutation=True, max_entries=1024)
def analyze(model_name, text):
    nlp = camphr.load(model_name)
    return nlp(text)


@patch('pyknp.juman.juman.Subprocess', Subprocess)
@patch('pyknp.knp.knp.Subprocess', Subprocess)
def main():
    st.title('KNP Visualizer')

    text = st.text_area(
        'Text to analyze',
        'クロールで泳いでいる少女を見た。',
        height=200
    )
    if not text:
        return

    doc = analyze('knp', text)

    # Sidebar
    st.sidebar.header('Token Attributes Options')
    disable_token_attrs = st.sidebar.checkbox(
        'Disable',
        key='disable_token_attrs'
    )

    st.sidebar.header('Dependency Tree Options')
    disable_dep_tree = st.sidebar.checkbox(
        'Disable',
        key='disable_dep_tree'
    )
    ud_tree = st.sidebar.checkbox(
        'Universal Dependency',
        value=True,
        key='disable_ud_tree'
    )
    compact = st.sidebar.checkbox('Compact')

    st.sidebar.header('PAS Options')
    disable_pas = st.sidebar.checkbox(
        'Disable',
        key='disable_pas'
    )
    bunsetsu_node = st.sidebar.checkbox('Bunsetsu Node', value=True)

    for sent in doc.sents:
        # Token Attributes

        if not disable_token_attrs:
            st.header('Token Attributes')
            visualize_tokens(sent)

        # Dependency Tree

        if not disable_dep_tree:
            st.header('Dependency Tree')

            options = {
                'compact': compact
            }

            st.subheader('Original')
            st.markdown(f"> {sent.text}")
            data = bunsetsu_list_to_dependency_data(list(sent._.knp_bunsetsu_list_))
            visualize_dependency(data, options)

            if ud_tree:
                st.subheader('Universal Dependency')
                st.markdown(f"> {sent.text}")
                data = bunsetsu_spans_to_dependency_data(list(sent._.knp_bunsetsu_spans))
                visualize_dependency(data, options)

        # Predicate-Argument Structure
        if not disable_pas:
            st.header('Predicate-Argument Structure (PAS)')
            st.markdown(f'> {sent.text}')
            graph = tag_spans_to_graph(list(sent._.knp_tag_spans), bunsetsu_node)
            st.graphviz_chart(graph)


if __name__ == '__main__':
    main()
