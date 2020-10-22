from __future__ import annotations

from typing import Optional

import graphviz
import pandas as pd
import streamlit as st
from spacy import displacy
from spacy.tokens import Doc, Span
from spacy_streamlit.util import get_svg


def bunsetsu_list_to_dependency_data(bunsetsu_list: list) -> dict[str, dict]:
    words = []
    arcs = []
    for i, chunk in enumerate(bunsetsu_list):
        words.append({
            'text': chunk.midasi, 'tag': '',
        })
        j = chunk.parent_id
        if j == -1:
            continue
        elif i > j:
            i, j = j, i
            direction = 'right'
        else:
            direction = 'left'
        arcs.append({
            'start': i, 'end': j, 'label': '', 'dir': direction
        })
    return {'words': words, 'arcs': arcs}


def bunsetsu_spans_to_dependency_data(spans: list[Span]) -> dict[str, dict]:
    words = []
    arcs = []
    token_to_span = {token.i: i for i, span in enumerate(spans) for token in span}
    for i, span in enumerate(spans):
        words.append({
            'text': span.text, 'tag': span.label_
        })
        parent = span.root.head
        j = token_to_span[parent.i]
        if i == j:
            continue
        elif i > j:
            i, j = j, i
            direction = 'right'
        else:
            direction = 'left'
        arcs.append({
            'start': i,
            'end': j,
            'label': span.root.dep_,
            'dir': direction
        })
    return {'words': words, 'arcs': arcs}


def tag_spans_to_graph(spans: list, bunsetsu_node: bool = False) -> graphviz.Digraph:
    graph = graphviz.Digraph()
    for span in spans:
        if span._.knp_tag_element.pas:
            for case, arguments in span._.knp_tag_element.pas.arguments.items():
                for argument in arguments:
                    if bunsetsu_node:
                        source = span.root._.knp_morph_bunsetsu.text
                        target = spans[argument.tid].root._.knp_morph_bunsetsu.text
                    else:
                        source = span.text
                        target = argument.midasi
                    graph.edge(source, target, label=case)
    return graph


def visualize_dependency(data: dict, options: Optional[dict] = None) -> None:
    options = options or {}
    html = displacy.render(
        data,
        style='dep',
        manual=True,
        options=options
    ).replace('\n\n', '\n')
    st.write(get_svg(html), unsafe_allow_html=True)


def visualize_tokens(
    doc: Doc,
    attrs: list[str] = ['text', 'lemma_', 'pos_', 'tag_']
) -> None:
    data = [[getattr(token, attr) for attr in attrs]for token in doc]
    st.table(pd.DataFrame(data, columns=attrs))
