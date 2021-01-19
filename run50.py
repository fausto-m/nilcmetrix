# -*- coding: utf-8 -*-
import text_metrics
import sys

feat_list = ["brunet", "simple_word_ratio", "log_pos_conn_ratio", "flesch", "punctuation_ratio", "idade_aquisicao_std", "dep_distance", "third_person_pronouns", "dalechall adapted", "content_word max", "punctuation_diversity", "sentences_with_one_clause", "familiaridade_std", "content_words_ambiguity", "logic_operators", "syllables_per_content_word", "passive_ratio", "adjunct_per_clause", "aux_plus_PCP_per_sentence", "content_word min", "verbs min", "familiaridade_mean", "nouns_ambiguity", "cau_neg_conn_ratio", "ratio_function_to_content_words", "ratio_coordinate_conjunctions", "adverbs_before_main_verb_ratio", "verbs_max", "sentence_length_min", "indicative_pluperfect_ratio", "sentences_with_four_clauses", "adverbs_diversity_ratio", "sentences_with_three_clauses", "idade_aquisicao_4_55_ratio", "words_per_sentence", "frazier", "easy_conjunctions_ratio", "idade_aquisicao_25_4_ratio", "sentences_with_five_clauses", "honore", "apposition_per_clause", "non_svo_ratio", "adjectives_ambiguity", "participle_verbs", "cau_pos_conn_ratio", "max_noun_phrase", "words", "adjective_diversity_ratio", "sentences_with_six_clauses", "verbs"]

text = sys.argv[1]
raw = text.replace('\n', '').replace('\r', '')
print(raw)
raw = raw.encode("utf-8", "surrogateescape").decode("utf-8")
t = text_metrics.Text(raw)
#ret = text_metrics.all_metrics.values_for_text(t).as_flat_dict()
ret = text_metrics.sentence_metrics.values_for_text(t).as_flat_dict()
result_array = []
for f in feat_list:
    print("%s:%s" % (f, round(ret[f],4)))
    result_array.append(round(ret[f],4))
result = str(result_array)
result = result.replace(" ", "")
print(result)
