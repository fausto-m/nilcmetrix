import pytest
import text_metrics

from text_metrics.base import (
    MetricsSet,
)

# from text_metrics.resource_pool import (
#     DefaultResourcePool,
#     rp,
# )

from text_metrics.metrics import *
from text_metrics.tools import *
from text_metrics.conf import config

def process_text(t):
    raw = t.replace('{{quotes}}', '"')
    raw = raw.replace('{{exclamation}}', '!')
    raw = raw.replace('{{enter}}', '\n')
    raw = raw.replace('{{sharp}}', '#')
    raw = raw.replace('{{ampersand}}', '&')
    raw = raw.replace('{{percent}}', '%')
    raw = raw.replace('{{dollar}}', '$')
    raw = raw.encode("utf-8", "surrogateescape").decode("utf-8")
    return text_metrics.Text(raw)

metrics = MetricsSet([SpacyConstituents()])
# rp = DefaultResourcePool()
  

class TestWordsBeforeMainVerb:
    def test_words_before_main_verb(self):
        text = "O acessório polêmico entrou no projeto, de autoria do senador Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão de Educação do Senado em outubro."
        expect = 3
        t = process_text(text)
        ret = metrics.values_for_text(t).as_flat_dict()  
        assert (expect == ret["words_before_main_verb"])
        
        text = "Se a ideia for aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e camiseta."
        expect = 8
        t = process_text(text)
        ret = metrics.values_for_text(t).as_flat_dict()  
        assert (expect == ret["words_before_main_verb"])

        text = "Nas inserções que já circulam, o PMDB ataca as denúncias feitas pela Procuradoria Geral da República (PGR) contra o presidente Michel Temer, por conta da Operação Lava Jato, e faz comparações entre a situação econômica de hoje e a do governo Dilma Rousseff."
        expect = 8
        t = process_text(text)
        ret = metrics.values_for_text(t).as_flat_dict()  
        assert (expect == ret["words_before_main_verb"])