# cohmetrix
FROM ubuntu:jammy
# FROM ubuntu/python:3.10-22.04_stable

# ENV TZ=America/Sao_Paulo
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update
RUN apt install -y python3 python3-pip python3-numpy
RUN apt install -y default-jre
#RUN apt install -y python3 python3-pip locales libpq-dev libxml2-dev libxslt1-dev python3-dev python3-lxml
#RUN apt-get install -y python3-numpy python3-scipy python3-matplotlib ipython ipython-notebook python3-pandas python3-sympy python3-nose
#RUN apt-get install -y python3-sklearn default-jre

RUN pip3 install --upgrade pip~=24.1.2
RUN pip3 install --upgrade nltk~=3.9.1
RUN pip3 install --upgrade termcolor~=2.5.0
RUN pip3 install --upgrade setuptools~=75.2.0
RUN pip3 install --upgrade numpy~=1.23.5
RUN pip3 install --upgrade kenlm~=0.2.0
RUN pip3 install --upgrade gensim~=4.3.3
RUN pip3 install --upgrade spacy~=3.7.5
RUN pip3 install --upgrade lxml~=5.3.0
RUN pip3 install --upgrade scipy~=1.13.1
RUN pip3 install --upgrade SQLAlchemy~=2.0.36
RUN pip3 install --upgrade psycopg2-binary~=2.9.10

WORKDIR /opt/text_metrics

COPY . .

#RUN cd tools/nlpnet-py3 && python3 setup.py install  && cd ..
# RUN pip3 install psycopg2-binary --break-system-packages

# RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# RUN python3 -m nltk.downloader all
# RUN python3 -m spacy download pt_core_news_lg --break-system-packages

COPY tools/nltk_data /root/nltk_data

RUN pip3 install tools/spacy_models/pt_core_news_lg-3.8.0-py3-none-any.whl

RUN cd tools/idd3 && python3 setup.py install && cd ..

RUN cd tools/nlpnet_package && python3 setup.py install

WORKDIR /opt/text_metrics
