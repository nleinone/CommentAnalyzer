import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 

'''
REFERENCES:

Pointwise mutual information:
   https://towardsdatascience.com/feature-engineering-with-nltk-for-nlp-and-python-82f493a937a0 

Information and examples about sentiment analysis, bigrams and collocations:
https://streamhacker.com/2010/05/24/text-classification-sentiment-analysis-stopwords-collocations/
   
Nltk Book chapter about collocations:
http://www.nltk.org/howto/collocations.html

'''

from nltk.collocations import *
import string

def normalize_and_clean_comment(stopword_filtered_comment):
    """Make all words lowercase and clean words which are not alphabetic"""

    cleaned_comment = []

    for comment in stopword_filtered_comment:
        single_comment = []
        for word in comment:
            if word.isalpha() and word.lower() not in string.punctuation:
                single_comment.append(word.lower())
        if len(single_comment) != 0:
            cleaned_comment.append(single_comment)

    return cleaned_comment

def filter_stopwords(tokenized_answer, training_mode, bigram):
    '''Filter stopwords'''

    #not_filtered = ['above', 'below', 'off', 'over', 'under', 'more', 'most', 'such', 'no', 'nor', 'not', 'only', 'so', 'than', 'too', 'very', 'just', 'but']
    not_filtered = ["not", "nor", "no"]
    #not_filtered = []

    stop_words = stopwords.words('english')

    if bigram:

        stop_words = set(stopwords.words('english')) - set(not_filtered)   

    stopword_filtered_answer = []

    if training_mode:
        for comment in tokenized_answer:
            single_comment = []
            for word in comment:
                if word.lower() not in stop_words and word.lower() not in string.punctuation:
                    single_comment.append(word)
            if len(single_comment) != 0:
                stopword_filtered_answer.append(single_comment)

    else:
        single_comment = []
        for word in tokenized_answer:
            if word.lower() not in stop_words and word.lower() not in string.punctuation:
                single_comment.append(word)
        if len(single_comment) != 0:
            stopword_filtered_answer.append(single_comment)

    #normalized_filtered_answer = stopword_filtered_answer

    '''
    if training_mode and bigram:
        print("len comment:{}".format(len(normalized_filtered_answer)))
        bigram_measures = nltk.collocations.BigramAssocMeasures()

        all_words = []
        normalized_filtered_bigrams = []
        
        for word_set in normalized_filtered_answer:
            for word in word_set:
                all_words.append(word)
        
        print("len all comment:{}".format(len(all_words)))
        
        finder = BigramCollocationFinder.from_words(all_words)

        scored_list = finder.score_ngrams(bigram_measures.raw_freq)
        
        new_all_words = []
        
        for scored_bigram in scored_list:
            
            new_all_words.append(scored_bigram[0])
        
        print("len scored:{}".format(len(scored_list)))
        print("len new_all_words:{}".format(len(new_all_words)))
        counter = 0
        for word_set in normalized_filtered_answer:
            single_comment = []
            for word in word_set:
                print(word)
                if word in new_all_words:
                    print(counter)
                    single_comment.append(word)
                    counter += 1
            #if len(single_comment) != 0:
            normalized_filtered_bigrams.append(single_comment)
        
        
        #print(len(all_words))
        print("len comment 2: {}".format(len(normalized_filtered_bigrams)))
        finder = BigramCollocationFinder.from_words(all_words)
        
    

        finder = BigramCollocationFinder.from_words(all_words)
        #finder.apply_freq_filter(3)
        scores = finder.score_ngrams(bigram_measures.raw_freq)
        #print(len(scores))
        #print(scores)
        
        #Only include bigrams that appear more than 5 times:
        if len(scores) > 0:
            for index in range(len(scores)):
                bigram_word = scores[index][0]
                normalized_filtered_answer_bigram.append(bigram_word)
        #print(normalized_filtered_answer_bigram)    
        return normalized_filtered_answer_bigram
    '''    

    return stopword_filtered_answer

def tokenize_comment(user_answer):
    '''Tokenize user answer'''

    #TreewordBankTokenizer
    tokenized_answer = nltk.word_tokenize(user_answer.lower())

    #tokenized_answer = nltk.wordpunct_tokenize(user_answer)
    return tokenized_answer

def stem_sentence(sentences, training_mode):
    '''Remove suffixes (and other end components) from the words, returning only the root part of the word'''

    stemmed_sentences = []
    stemmer = PorterStemmer() 

    if training_mode:
        for comment in sentences:
            single_comment = []
            for word in comment:

                stemmed_word = stemmer.stem(word)
                single_comment.append(stemmed_word)

            if len(single_comment) != 0:
                stemmed_sentences.append(single_comment)

    else:
        single_comment = []
        for word in sentences:
            stemmed_word = PorterStemmer.stem(word)
            single_comment.append(stemmed_word)
            
        if len(single_comment) != 0:
            stemmed_sentences.append(single_comment)

    return stemmed_sentences

def lemmatization(sentences, training_mode):
    '''Remove suffixes (and other end components) from the words, returning only the root part of the word'''

    lemmed_sentences = []
    lemmer = WordNetLemmatizer() 

    if training_mode:
        for comment in sentences:
            single_comment = []
            for word in comment:

                lemmed_word = lemmer.lemmatize(word)
                single_comment.append(lemmed_word)

            if len(single_comment) != 0:
                lemmed_sentences.append(single_comment)

    else:
        single_comment = []
        for word in sentences:
            lemmed_word = lemmer.lemmatize(word)
            single_comment.append(lemmed_word)

        if len(single_comment) != 0:
            lemmed_sentences.append(single_comment)

    return lemmed_sentences
