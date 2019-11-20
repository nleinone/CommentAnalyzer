from random import shuffle
from nltk import ngrams
from preprocessing import preprocessor

'''
REFERENCES:

Above link demonstrates the use of movie review data and nltk Naive Bayes classifier library:
http://blog.chapagain.com.np/python-nltk-sentiment-analysis-on-movie-reviews-natural-language-processing-nlp/

Documentation for nltk Naive Bayes:
https://www.nltk.org/_modules/nltk/classify/naivebayes.html

Chapter from book:
https://www.nltk.org/book/ch06.html

Using collocations:
https://streamhacker.com/2010/05/24/text-classification-sentiment-analysis-stopwords-collocations/

'''

from nltk.corpus import movie_reviews 
from nltk import FreqDist
from nltk import NaiveBayesClassifier
from nltk import classify 
from nltk.corpus import stopwords
from sys import exit
import string 

from nltk.metrics.scores import (precision, recall)


def print_statistics(probability_result, nb_classifier, normalized_comment_feature_set, comment, classifier_accuracy_values, cross_validate):
    
    prob_pos = probability_result.prob("pos")
    prob_neg = probability_result.prob("neg")
    #(user_name, time, bot_mood, bot_answer, user_answer):
    
    user_name = comment['user_name']
    post_time = comment['time'] 
    bot_mood = comment['bot_mood']
    bot_answer = comment['bot_answer']
    user_answer = comment['user_answer']
    
    
    print('\n******* SENTENCE STATISTICS *******\n')
    print("Classified comment: {}".format(user_answer))
    print("Classified comment word set: {}".format(normalized_comment_feature_set.keys()))
    print("Probability for negative sentiment: {}".format(prob_neg) )   
    print("Probability for positive sentiment: {}".format(prob_pos))

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
    
    #{'mean_accuracy': mean_nb_accuracy, 'mean_pos_mean_precision':mean_pos_mean_precision,'mean_pos_mean_recall':mean_pos_mean_recall,'mean_pos_mean_f_score':mean_pos_mean_f_score,'mean_neg_mean_precision':mean_neg_mean_precision,'mean_neg_mean_recall':mean_neg_mean_recall,'mean_neg_mean_f_score':mean_neg_mean_f_score}
        
    if cross_validate:
        print('Pos Avg Precision: {}'.format(classifier_accuracy_values['mean_pos_mean_precision'])) #High = Few false positives in pos
        print('Pos Avg Recall: {}'.format(classifier_accuracy_values['mean_pos_mean_recall'])) #High = Few false negatives in pos
        print('Pos Avg F-score: {}'.format(classifier_accuracy_values['mean_pos_mean_f_score']))

        print('Neg Avg Precision: {}'.format(classifier_accuracy_values['mean_neg_mean_precision']))
        print('Neg Avg Recall: {}'.format(classifier_accuracy_values['mean_neg_mean_recall']))
        print('Neg Avg F-Score: {}'.format(classifier_accuracy_values['mean_neg_mean_f_score']))
            
    #nb_classifier.show_most_informative_features(20)
    
    print('Classifier accuracy: {}\n'.format(classifier_accuracy_values['mean_accuracy']))
    
    print("\nClassification: {}\n".format(classification))
    
    
    
    print('************************************\n')
    
      
def divide_and_clean_reviews():
    """Filter stopwords from uni and bigram reviews, lower all cases, and remove punctuations. Optionally use stemming (commented)"""

    positive_reviews = []
    for id in movie_reviews.fileids('pos'):
        words = movie_reviews.words(id)
        positive_reviews.append(words)
    
    negative_reviews = []
    for id in movie_reviews.fileids('neg'):
        words = movie_reviews.words(id)
        negative_reviews.append(words)
    
    
    
    training_mode = True
    
    bigram = False
    filt_neg_revs = preprocessor.filter_stopwords(negative_reviews, training_mode, bigram)
    filt_pos_revs = preprocessor.filter_stopwords(positive_reviews, training_mode, bigram)
    
    bigram = True
    filt_pos_revs_bigram = preprocessor.filter_stopwords(negative_reviews, training_mode, bigram)
    filt_neg_revs_bigram = preprocessor.filter_stopwords(positive_reviews, training_mode, bigram)
    
    normalized_reviews_neg = preprocessor.normalize_and_clean_comment(filt_neg_revs)
    normalized_reviews_pos = preprocessor.normalize_and_clean_comment(filt_pos_revs)

    normalized_reviews_neg_bigram = preprocessor.normalize_and_clean_comment(filt_neg_revs_bigram)
    normalized_reviews_pos_bigram = preprocessor.normalize_and_clean_comment(filt_pos_revs_bigram)
    
    '''STEMMING'''
    #normalized_reviews_neg = preprocessor.stem_sentence(normalized_reviews_neg, training_mode)
    #normalized_reviews_pos = preprocessor.stem_sentence(normalized_reviews_pos, training_mode)
    #normalized_reviews_neg_bigram = preprocessor.stem_sentence(normalized_reviews_neg, training_mode)
    #normalized_reviews_pos_bigram = preprocessor.stem_sentence(normalized_reviews_pos, training_mode)
    
    '''LEMMITIZATION'''
    normalized_reviews_neg = preprocessor.lemmatization(normalized_reviews_neg, training_mode)
    normalized_reviews_pos = preprocessor.lemmatization(normalized_reviews_pos, training_mode)
    normalized_reviews_neg_bigram = preprocessor.lemmatization(normalized_reviews_neg, training_mode)
    normalized_reviews_pos_bigram = preprocessor.lemmatization(normalized_reviews_pos, training_mode)
    
    return normalized_reviews_pos, normalized_reviews_neg, normalized_reviews_neg_bigram, normalized_reviews_pos_bigram

def extract_feature_unigram(words_clean, training_mode):
    '''Extract unigram word features'''
    
    words_dictionary = {}
    
    if training_mode:
        
        for word in words_clean:
            words_dictionary[word] = True
    else:
    
        for word in words_clean[0]:
            words_dictionary[word] = True
    
    return words_dictionary
    
def extract_features_bigram(words_clean, training_mode):
    '''
    words_ng = []
    for item in iter(ngrams(words, n)):
        words_ng.append(item)
    words_dictionary = dict([word, True] for word in words_ng)    
    return words_dictionary
    '''
    '''Extract bigram word features'''
    words_bigram = []
    #print("bigram 1")
    if training_mode:
        
        for i in iter(ngrams(words_clean, 2)):
            words_bigram.append(i)
    else:
    #    print("bigram 2")
        for i in iter(ngrams(words_clean[0], 2)):
    #        print("bigram 3: {}".format(i))
            words_bigram.append(i)
    
    #print("bigram words: ")
    #print(words_bigram)
    words_dictionary = {}
    
    try:
        if training_mode:
            
            for word in words_bigram:
                words_dictionary[word] = True
        
        else:
            for word in words_bigram:
                words_dictionary[word] = True

    except:
        return words_bigram
    
    return words_dictionary
    
def extract_features(clean_words_uni, clean_words_bigram, training_mode):
    '''Combine unigram features and bigram features'''
    
    uni_features = extract_feature_unigram(clean_words_uni, training_mode)
    bigram_features = extract_features_bigram(clean_words_bigram, training_mode)
    features = uni_features.copy()
    features.update(bigram_features)
    
    return features
    
def create_word_feature_sets():
    """Create word feature set to train the classifier"""
    
    positive_reviews_uni, negative_reviews_uni, positive_reviews_bigram, negative_reviews_bigram = divide_and_clean_reviews()
    training_mode = True
    
    feature_set_positive = []
    
    for clean_words_uni, clean_words_bigram in zip(positive_reviews_uni, positive_reviews_bigram):
        feature_set_positive.append((extract_features(clean_words_uni, clean_words_bigram, training_mode), 'pos'))

    feature_set_negative = []
    
    for clean_words_uni, clean_words_bigram in zip(negative_reviews_uni, negative_reviews_bigram):
        feature_set_negative.append((extract_features(clean_words_uni, clean_words_bigram, training_mode), 'neg'))
    
    
    
    return feature_set_positive, feature_set_negative
     
def split_data(feature_set_positive, feature_set_negative, fold):
    '''Split data for cross validation.'''

    training_and_test_data = []
    
    test = feature_set_positive[:fold] + feature_set_negative[:fold]
    training = feature_set_positive[fold:] + feature_set_negative[fold:]
    all_training_data = feature_set_positive + feature_set_negative
    
    training_and_test_data.append([test, training])
    
    for index in range(4):    
        test = feature_set_positive[fold * (index + 1):fold + (index + 1) * fold] + feature_set_negative[fold * (index + 1):fold + (index + 1) * fold]
        bottom_train_section = feature_set_positive[:fold * (index + 1)] + feature_set_negative[:fold * (index + 1)]
        
        if index == 3:
            top_train_section = []
        
        else:
            top_train_section = feature_set_positive[fold + ((index + 1) * fold):] + feature_set_negative[fold + ((index + 1) * fold):]
        
        training = bottom_train_section + top_train_section
        training_and_test_data.append([test, training])
        
    return training_and_test_data, all_training_data
    
def get_training_and_test_data(fold):
    '''Top function for training and test data parsing, shuffling and splitting'''
    
    feature_set_positive, feature_set_negative = create_word_feature_sets()
    shuffle(feature_set_positive)
    shuffle(feature_set_negative)
    
    #TEST DATA SPLIT:
    #print("Len pos features: {}".format(len(feature_set_positive)))
    #print("Len neg features: {}".format(len(feature_set_negative)))
    
    training_and_test_data, all_training_data = split_data(feature_set_positive, feature_set_negative, fold)
    
    return training_and_test_data, all_training_data