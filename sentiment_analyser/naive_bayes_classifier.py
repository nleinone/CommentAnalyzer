from random import shuffle

from preprocessing import preprocessor

'''
REFERENCES:

http://blog.chapagain.com.np/python-nltk-sentiment-analysis-on-movie-reviews-natural-language-processing-nlp/
Above link demonstrates the use of movie review data and nltk Naive Bayes classifier library.

Documentation for nltk Naive Bayes:
https://www.nltk.org/_modules/nltk/classify/naivebayes.html

Chapter from book:
https://www.nltk.org/book/ch06.html

'''

from nltk.corpus import movie_reviews 
from nltk import FreqDist
from nltk import NaiveBayesClassifier
from nltk import classify 
from nltk.corpus import stopwords
from sys import exit
import string 

def print_statistics(probability_result, nb_classifier, normalized_comment_feature_set, user_answer, classifier_accuracy):
    
    prob_pos = probability_result.prob("pos")
    prob_neg = probability_result.prob("neg")
    
    print('\n******* SENTENCE STATISTICS *******\n')
    print("Classified comment: {}".format(user_answer))
    print("Classified comment word set: {}".format(normalized_comment_feature_set.keys()))
    print("Probability for negative sentiment: {}".format(prob_pos) )   
    print("Probability for positive sentiment: {}".format(prob_neg))

    #Classification axis:'
    
    #By probability % of positive sentiment:
    #Positive          80%->
    #Somewhat Positive 60%-80%
    #Neutral           50%-60%
    
    #By probability % of negative sentiment:
    #Negative          80%->
    #Somewhat Negative 60%-80%
    #Neutral           50%-60%
    
    classifications = ['Positive', 'Somewhat positive', 'Neutral', 'Somewhat_negative', 'negative']
    
    if prob_pos >= 0.80:
        classification = 'Positive'
    elif prob_pos >= 0.60:
        classification = 'Somewhat positive'
    elif prob_pos >= 0.50:
        classification = 'Neutral'
    if prob_neg >= 0.80:
        classification = 'Negative'
    elif prob_neg >= 0.60:
        classification = 'Somewhat negative'
    elif prob_neg >= 0.50:
        classification = 'Neutral'
    
    print("\nClassification: {}\n".format(classification))
    print('Classifier accuracy: {}\n'.format(classifier_accuracy))
    
def test_classifier(classifier, validation_data_set):
    '''Return classifier accuracy'''
    
    classifier_accuracy = classify.accuracy(classifier, validation_data_set)
    
    return classifier_accuracy
    
def train_NB_Classifier(training_data_set):
    """Train Naive Bayes classifier with created training data set"""
    
    naive_bayes_classifier = NaiveBayesClassifier.train(training_data_set)
    return naive_bayes_classifier
      
def divide_and_clean_reviews():
    """Get word features of 10 words out of common_word_limit (2000) most common words"""

    #Collect positive reviews:
    positive_reviews = []
    for id in movie_reviews.fileids('pos'):
        words = movie_reviews.words(id)
        positive_reviews.append(words)
    
    #Collect negative reviews:
    negative_reviews = []
    for id in movie_reviews.fileids('neg'):
        words = movie_reviews.words(id)
        negative_reviews.append(words)  
    
    #Clean the reviews
    training_mode = True
    filt_neg_revs = preprocessor.filter_stopwords(negative_reviews, training_mode)
    filt_pos_revs = preprocessor.filter_stopwords(positive_reviews, training_mode)
    
    normalized_reviews_neg = preprocessor.normalize_and_clean_comment(filt_neg_revs)
    normalized_reviews_pos = preprocessor.normalize_and_clean_comment(filt_pos_revs)
    
    return normalized_reviews_pos, normalized_reviews_neg

def bag_of_words(words_clean, training_mode):
    '''Create bag of words'''
    words_dictionary = {}
    if training_mode:
        for word in words_clean:
            words_dictionary[word] = True
    else:
        for word in words_clean[0]:
            words_dictionary[word] = True

    return words_dictionary
    
def create_word_feature_sets():
    """Create word feature set to train the classifier"""
    
    positive_reviews, negative_reviews = divide_and_clean_reviews()
    
    training_mode = True
    
    feature_set_positive = []
    for words in positive_reviews:
        feature_set_positive.append((bag_of_words(words, training_mode), 'pos'))

    feature_set_negative = []
    for words in negative_reviews:
        feature_set_negative.append((bag_of_words(words, training_mode), 'neg'))                   

    return feature_set_positive, feature_set_negative
    
def configure_classifier():
    
    feature_set_positive, feature_set_negative = create_word_feature_sets()
    
    shuffle(feature_set_positive)
    shuffle(feature_set_negative)
    
    #TEST DATA SPLIT:
    test_set = feature_set_positive[:200] + feature_set_negative[:200]
    training_data_set = feature_set_positive[200:] + feature_set_negative[200:]
    
    #TRAINING:
    nb_classifier = train_NB_Classifier(training_data_set)
    
    #VALIDATION:
    classifier_accuracy = test_classifier(nb_classifier, test_set)
    
    return nb_classifier, classifier_accuracy