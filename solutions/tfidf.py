import nltk
nltk.download('wordnet')

import math
import re
import heapq
from nltk.stem import WordNetLemmatizer

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

class tfidf():
    def __init__(self, *args):
        if len(args) == 3:
            self.filepath = args[0]
            self.start = args[1]
            self.end = args[2]
            self.pdf_text=""
            #setting flag to p to denote text has to be extracted from pdf
            self.flag = "p"
        else:
            self.pdf_text = args[0]
            #setting flag to h to denote text has already been extracted in extractHighlight.py
            self.flag="h"


    def convert_pdf_to_txt(self):
        resource_manager = PDFResourceManager()
        ret_str = StringIO()
        laparams = LAParams()
        text_converter = TextConverter(resource_manager, ret_str, laparams=laparams)
        interpreter = PDFPageInterpreter(resource_manager, text_converter)
        
        #opening file
        fp = open(self.filepath, 'rb')
        
        #extracting text from pages
        pglist = [i for i in range(self.start-1, self.end)]
        for page in PDFPage.get_pages(fp, pagenos=pglist):
            interpreter.process_page(page)
        self.pdf_text = ret_str.getvalue()
        
        #closing pointers
        fp.close()
        text_converter.close()
        ret_str.close()
        return


    def preprocess_text(self):
        '''
        args: text
        returns: text after removing new line characters
        '''
        count = self.pdf_text.count("\n")
        self.pdf_text = self.pdf_text.replace("\n", "", count)
        return

    def tokenize_sentence(self):
        '''
        arg: text to be summarized
        returns: list of sentences
        '''
        sentences = re.split('\. |\? ', self.pdf_text)
        return sentences

    def lemmatize_word(self, word):
        '''
        args: a word
        returns: lemmatized word (e.g. programs -> program)
        '''
        wordlemmatizer = WordNetLemmatizer()
        word = word.strip().lower()
        word = wordlemmatizer.lemmatize(word)
        return word

    def document_word_frequency_matrix(self, sentences, stopwords):
        '''
        args:sentences-list of sentences in text
        stopwords-a list of words that are not required to be included for the process of extractive summarization

        returns: document_word_freq contains frequency of each word in a sentence.
           It is of form {sentence_1 : {word1_in_sentence_1:freq, word2_in_sentence_1:freq, .....},
           sentence_2 : {word1_in_sentence_2:freq, word2_in_sentence_2:freq, .....},
           ....
           ....
           sentence_n : {word1_in_sentence_n:freq, word2_in_sentence_n:freq, .....}}
        '''
        document_word_frequency = dict()
        for sentence in sentences:
            term_freq = dict()
            words_list = sentence.split(" ")
            for word in words_list:
                word = self.lemmatize_word(word)
                if word in stopwords or len(word)<=1:
                    continue
                else:
                    term_freq[word] = term_freq.get(word, 0)+1
            #ignore sentences in document_word_frequency which does not contain any words other than stopwords and unwanted characters
            if(len(term_freq))>=1:
                document_word_frequency[sentence] = term_freq
        return document_word_frequency

    def generate_tf_matrix(self, doc_term_freq_matrix):
        '''
        args:doc_term_freq_matrix-is document_word_frequency dictionary

        returns: tf_matrix contains tf value (term frequency) of each word in a sentence.
           It is of form {sentence_1 : {word1_in_sentence_1:tf_value, word2_in_sentence_1:tf_value, .....},
           sentence_2 : {word1_in_sentence_2:tf_value, word2_in_sentence_2:tf_value, .....},
           ....
           ....
           sentence_n : {word1_in_sentence_n:tf_value, word2_in_sentence_n:tf_value, .....}}
        '''
        tf_matrix = dict()
        for sent, freq in doc_term_freq_matrix.items():
            tf_sentence = dict()
            count_words_in_sentence = len(freq.keys())
            for word, count in freq.items():
                tf_sentence[word] = count / count_words_in_sentence
            tf_matrix[sent] = tf_sentence
        return tf_matrix

    def generate_idf_matrix(self, doc_term_freq_matrix):
        '''
        args:doc_term_freq_matrix-is document_word_frequency dictionary

        returns: idf_matrix which contains idf value (inverse document frequency) of each word.
           It is of form {word1:idf_value1, word2:idf_value2, word3:idf_value3, ... ... ...}
        '''
        no_of_sentences = len(doc_term_freq_matrix.keys())
        idf_matrix = dict()
        for sent, freq in doc_term_freq_matrix.items():
            words_in_sent = set(freq.keys())
            for word in words_in_sent:
                idf_matrix[word] = idf_matrix.get(word,0)+1
        for word,occ in idf_matrix.items():
            idf_matrix[word] = math.log10(no_of_sentences/occ)
        return idf_matrix


    def sentence_importance(self, document_word_frequency, stopwords, tf_matrix, idf_matrix):
        '''
        args:doc_term_freq_matrix-is document_word_frequency dictionary
        stopwords-a list of words that are not required to be included for the process of extractive summarization
        tf_matrix contains tf value (term frequency) of each word in a sentence.
        idf_matrix contains idf value (inverse document frequency) of each word.

        returns:sentences_scores is a dictionary which contains scores (sum of tf_value * idf_value for each word in sentence) of each sentence - {sentence1:score1, sentence2:score2, ... ... ...}
        '''
        sentences_scores = dict()
        for sentence, word_dict in document_word_frequency.items():  
            score = 0
            sentence_words = list(word_dict.keys())
            for word in sentence_words:
                word = self.lemmatize_word(word)
                if word not in stopwords and len(word)>1: 
                    if sentence in tf_matrix.keys() and word in tf_matrix[sentence].keys() and word in idf_matrix.keys():
                        score +=  (tf_matrix[sentence][word] * idf_matrix[word])
            sentences_scores[sentence] = score/len(sentence_words)
        return sentences_scores


    def generate_summary(self,sentences_scores):
        '''
        args: sentences_scores is a dictionary of sentence and its score
        threshold is min. score required for a sentence to be added in summary
        returns: summary
        '''
        summary_sentences = heapq.nlargest((len(sentences_scores)*95)//100, sentences_scores, key=sentences_scores.get)
        summary = '. '.join(summary_sentences)
        return summary

    def extractive_summarization(self):
        stopwords = ['up','do','below','having','has',"you'd",'over','when','she','any','will','more','or','few','whom','other','not','this','then','it','who',"it's",'mustn','d','y','you','too','an','those',"won't","you're",'just','our','from','should','for','yourself','me',"she's",'have','had','most',"weren't",'we','how','such',"hasn't",'and','same','be',"wouldn't",'i','what','isn','your','only','down',"you'll","aren't",'hasn',"mightn't",'hers','ll','ma',"couldn't",'are','o','ourselves',"hadn't",'being','won',"don't",'haven','t','s','didn','yours',"didn't",'about','can','m','now','his','as','my','doesn','some',"shan't",'no','weren','these','couldn','so',"shouldn't",'the','until','with','above','he','hadn','than','off','while','ve',"you've",'during','re','shan','each','ours','after','wasn','if','itself','between','they','but','into','of','is','by','aren','at','its','own',"mustn't",'don','were','myself','here','in','that','herself','him','where',"haven't",'nor','mightn','against','doing','needn','again','wouldn',"isn't",'am','theirs','to','under','why','there','himself','ain','on','which',"doesn't",'because','out','very','been','does',"that'll","needn't",'through',"should've",'shouldn','their','a','both','her','themselves','before','was','them','all','once','further','did','yourselves',"wasn't"]

        summary = ""

        if self.flag == "p":
            self.convert_pdf_to_txt()
        
        self.preprocess_text()

        sentences = self.tokenize_sentence()

        document_word_frequency = self.document_word_frequency_matrix(sentences, stopwords)

        tf_matrix = self.generate_tf_matrix(document_word_frequency)

        idf_matrix = self.generate_idf_matrix(document_word_frequency)

        sentences_scores = self.sentence_importance(document_word_frequency, stopwords,  tf_matrix, idf_matrix)

        summary = self.generate_summary(sentences_scores)
        
        return summary