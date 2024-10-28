# -*- coding: utf-8 -*-
# Coh-Metrix-Dementia - Automatic text analysis and classification for dementia.
# Copyright (C) 2014  Andre Luiz Verucci da Cunha
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, print_function, division
import spacy
from text_metrics.utils import is_valid_id, ilen
# from text_metrics.tools.tag.api import Tagger
# from text_metrics.tools.tag.spacymorpho import SpacyMorphoTagSet
# from text_metrics.conf import config

_model = "pt_core_news_lg"
# _model = "pt_core_news_sm"

class SpacyTagger():

    """textstring for SpacyTagger. """

    def __init__(self):
        self._tagger = None
        # self.tagset = SpacyMorphoTagSet()

    def load_tagger(self, text):
        if not self._tagger or text != self._source:
            try:
                self._tagger = spacy.load(_model)
                self._source = text
                self._text = self._tagger(text.raw_content)
            except:
                self._tagger = None
                self._source = None
                self._text = None

    def _get_ents(self, text):
        return text.ents
    
    def _get_verbs(self, text):
        """Return the number of verbs in a text, mitigating the incorrect tagging of verbs
        as auxiliary verbs

        Why: Spacy classifies certain verbs as AUX, like in "Ele foi para casa".
        Resolution: This function relies on spacy's dependency classification,
        which flags auxiliary verbs as "aux" or "aux:pass". So any AUX verb
        without such flags is counted as a verb.
            
        :returns: a list of spacy tokens.
        """
        verbs = [w for w in text if 
                    ( 
                        w.pos_ == "VERB" and
                        ( ( w.i+1 < len(self._text))  and self._text[w.i+1].pos_ != "VERB" and self._text[w.i+1].pos_ != "AUX")
                        and w.dep_ != "amod" #ignore VERB tokens categorized as adjectival clauses
                    ) or 
                    (
                        w.pos_ == "AUX" and 
                        (
                            w.dep_ != "aux:pass" and w.dep_ != "aux" #include AUX tokens not categorized as auxiliary clauses
                        )
                    )
        ]
        return verbs
    
    def _get_words(self, text):
        words = [ w for w in text if w.pos_ != "PUNCT" and w.pos_ != "SPACE" ]
        return words

    def sents(self, text):
        self.load_tagger(text)
        return self._text.sents
    
    def text(self, text):
        self.load_tagger(text)
        return self._text
    
    def ents(self, text):
        self.load_tagger(text)
        return self._get_ents(self._text)
    
    def ents_by_sentence(self, text):
        ent_list = []
        self.load_tagger(text)
        sentences = list(self._text.sents)
        for sentence in sentences:
            ents = self._get_ents(sentence)
            ent_list.append(ents)
        return ent_list
    
    def verbs(self, text):
        self.load_tagger(text)
        return self._get_verbs(self._text)

    def verbs_by_sentence(self, text):
        verb_list = []
        self.load_tagger(text)
        sentences = list(self._text.sents)
        for sentence in sentences:
            verbs = self._get_verbs(sentence)
            verb_list.append(verbs)
        return verb_list
    
    def tagged_words_in_sents(self, text):
        self.load_tagger(text)
        sentences_complete = list(self._text.sents)
        sentences = []
        for sentence in sentences_complete:
            words = self._get_words(sentence)
            sentences.insert(sentence.id, words)
        return sentences
    
    def count_verb_tenses(self, text):
        self.load_tagger(text)
        ind = self.word_by_feat_value(text,"Mood","Ind")
        ind_present = [ w for w in ind if w.morph.to_dict().get("Tense") == "Pres" ]
        ind_imperfect = [ w for w in ind if w.morph.to_dict().get("Tense") == "Imp" ]
        ind_perfect = [ w for w in ind if w.morph.to_dict().get("Tense") == "Past" ]
        ind_pluperfect = [ w for w in ind if w.morph.to_dict().get("Tense") == "Pqp" ]
        ind_future = [ w for w in ind if w.morph.to_dict().get("Tense") == "Fut" ]
        ind_conditional = self.word_by_feat_value(text,"Mood","Cnd")

        sub = self.word_by_feat_value(text,"Mood","Sub")
        subj_present = [ w for w in sub if w.morph.to_dict().get("Tense") == "Pres" ]
        subj_imperfect = [ w for w in sub if w.morph.to_dict().get("Tense") == "Imp" ]
        subj_future = [ w for w in sub if w.morph.to_dict().get("Tense") == "Fut" ]

        imperative = self.word_by_feat_value(text,"Mood","Imp")

        tenses = [
            ind_present, ind_imperfect, ind_perfect, ind_pluperfect, ind_future, ind_conditional,
            subj_present, subj_imperfect, subj_future,
            imperative
        ]

        verbs = self.verbs(text)
        verbno = len(verbs)
        tenseno = []
        
        for t in tenses:
            try:
                result = len(t) / verbno
            except ZeroDivisionError:
                result = 0
            tenseno.append(result)
        
        return tenseno

    def num_clauses(self, text):
        """
        Return the number of clauses found on text, relying on a spacy function.

        """

        self.load_tagger(text)
        verbs = self.verbs(text)
        return len(verbs)
    
    def sentence_lengths(self, text):
        """Return a list with the lengths, in words, of each sentence of the text.
        """
        self.load_tagger(text)
        sentences = self.tagged_words_in_sents(text)
        
        return [ilen(s) for s in sentences]

    def words(self, text):
        self.load_tagger(text)
        return self._get_words(self._text)
    
    def words_by_sentence(self, text):
        word_list = []
        self.load_tagger(text)
        sentences = list(self._text.sents)
        for sentence in sentences:
            words = self._get_words(sentence)
            word_list.append(words)
        return word_list

    def word_by_attribute(self, text, attribute, value):
        self.load_tagger(text)
        items = [w for w in self._text if w.__getattribute__(attribute) == value]
        return items
    
    def word_by_feat_value(self, text, feat, value):
        self.load_tagger(text)
        items = [w for w in self._text if w.morph.to_dict().get(feat) == value]
        return items