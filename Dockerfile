FROM yusanish/jumanpp_knp:latest

WORKDIR /app

COPY . /app/

RUN pip install -U pip \
    && pip install camphr[juman] \
    && pip install streamlit \
    && pip install graphviz \
    && pip install spacy-streamlit

CMD streamlit run visualizer.py
