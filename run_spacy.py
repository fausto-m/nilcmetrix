# -*- coding: utf-8 -*-
import text_metrics
import sys

from text_metrics.base import (
    Text,
    Category,
    Metric,
    MetricsSet,
    ResultSet,
)

from text_metrics.metrics import *

# text = sys.argv[1]
text = "Alguns dos sites que estão no ar foram criados na última sexta-feira (11), mesmo dia em que a agência divulgou a lista. A estratégia para burlar a proibição foi inserir, após o nome original da página, uma sequência de caracteres, como os números 11 e 22, por exemplo.\nO g1 encontrou 134 sites de 18 bets irregulares. Desses, 51 foram criados na sexta-feira (11), 19 no sábado (12), 5 nesta terça-feira (15) e 59 endereços foram criados antes. Uma mesma plataforma pode ter vários sites.\nProcurada, a Anatel disse que seu papel é encaminhar às operadoras a lista de sites indicada pelo Ministério da Fazenda.\nO ministério também foi procurado, mas não se manifestou. No último dia 10 de outubro, o ministro Fernando Haddad afirmou que o trabalho para identificar sites irregulares será contínuo. \"Evidentemente, tem um trabalho a ser feito pela secretaria [de Apostas] que é permanente. Qualquer tentativa de burla, a Anatel é informada e o procedimento é o mesmo\", declarou."

raw = text.replace('{{quotes}}', '"')
raw = raw.replace('{{exclamation}}', '!')
raw = raw.replace('{{enter}}', '\n')
raw = raw.replace('{{sharp}}', '#')
raw = raw.replace('{{ampersand}}', '&')
raw = raw.replace('{{percent}}', '%')
raw = raw.replace('{{dollar}}', '$')

#print(raw)
raw = raw.encode("utf-8", "surrogateescape").decode("utf-8")
t = text_metrics.Text(raw)
# ret = text_metrics.nilc_metrics_w_spacy.values_for_text(t).as_json()
metrics = MetricsSet([BasicCounts(),Ambiguity(), SpacyAIC()])
ret = metrics.values_for_text(t).as_json()
print(ret)

# result = '' 
# for f in ret:
#     m = "%s:%s," % (f, ret[f])
#     #print(m)
#     result += m
# print("++", result, "++")
