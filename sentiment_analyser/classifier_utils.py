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
import sys
from nltk.metrics.scores import precision, recall, f_measure

import csv

#REFERENCES:
#https://realpython.com/python-csv/

def create_conclusive_results_file(number_of_file_chunks_processed, discovered_identities, keys):
    
    
    identity_averages_dict = {}
    avg_values = []
    
    
    
    
    
    for identity in discovered_identities:
        print("\nCurrent id: " + str(identity))
        count_identity_amount = 1
        sum_of_values_positive = 0
        sum_of_values_negative = 0
        
        with open('./results/individual_file_results/results_{}.csv'.format(number_of_file_chunks_processed)) as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                #ingore headers_
                try:
                    float(row[-2])
                except ValueError:
                    continue
                else:
                    #ID key position after added positive, negative, and classification column:
                    if row[-4] == identity:
                        
                        count_identity_amount += 1
                        positive_prob = row[-2]
                        print("\nPos: " + str(positive_prob))
                        negative_prob = row[-3]
                        print("\nNeg: " + str(negative_prob))
                        #print("\nRow:" + str(row))
                        sum_of_values_positive = sum_of_values_positive + float(positive_prob)
                        sum_of_values_negative = sum_of_values_negative + float(negative_prob)
                        
                        print("\nsum_of_values_positive: " + str(sum_of_values_positive))
                        print("\nsum_of_values_negative: " + str(sum_of_values_negative))
                        
                        print("\nRow[-4]: " + str(row[-4]))
                        
                line_count += 1
            print("\nLinecount: " + str(line_count))
            
            #Negative average, Positive average, amount of samples
            identity_averages_dict[identity] = [sum_of_values_negative / count_identity_amount, sum_of_values_positive / count_identity_amount, count_identity_amount]
        
    
    print("\nidentity_averages: " + str(identity_averages_dict))
    
                    
            

def save_to_csv(values, keys, prob_neg, prob_pos, classification, save_counter, number_of_file_chunks_processed):
    ''''''
    #Add other information:'
    row_info = keys.copy()
    row_info.append('Negative probability')
    row_info.append('Positive probability')
    row_info.append('Classification')
    #print("row_info: " + str(row_info))

    #Add other values:
    values.append(prob_neg)
    values.append(prob_pos)
    values.append(classification)
    #print("values: " + str(values))

    with open('./results/individual_file_results/results_{}.csv'.format(number_of_file_chunks_processed), 'a', newline='') as file:
        writer = csv.writer(file)
        if save_counter == 0:
            writer.writerow(row_info)
        else:
            writer.writerow(values)
    
    
    file.close()
    save_counter = 1
    return save_counter
     
def print_statistics(probability_result, nb_classifier, normalized_comment_feature_set, comment, classifier_accuracy_values, cross_validate, save_counter, number_of_file_chunks_processed, keyes):
    '''Print various different statistics about the client response.'''

    prob_pos = probability_result.prob("pos")
    prob_neg = probability_result.prob("neg")
    #(user_name, time, bot_mood, bot_answer, user_answer):

    values = list(comment.values())

    #print('\n******* SENTENCE STATISTICS *******\n')
    #print("Classified comment: {}".format(user_answer))
    #print("Classified comment word set: {}".format(normalized_comment_feature_set.keys()))
    #print("Probability for negative sentiment: {}".format(prob_neg) )   
    #print("Probability for positive sentiment: {}".format(prob_pos))

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
        #print('Pos Avg Precision: {}'.format(classifier_accuracy_values['mean_pos_mean_precision'])) #High = Few false positives in pos
        #print('Pos Avg Recall: {}'.format(classifier_accuracy_values['mean_pos_mean_recall'])) #High = Few false negatives in pos
        #print('Pos Avg F-score: {}'.format(classifier_accuracy_values['mean_pos_mean_f_score']))

        #print('Neg Avg Precision: {}'.format(classifier_accuracy_values['mean_neg_mean_precision']))
        #print('Neg Avg Recall: {}'.format(classifier_accuracy_values['mean_neg_mean_recall']))
        #print('Neg Avg F-Score: {}'.format(classifier_accuracy_values['mean_neg_mean_f_score']))
        pass

    #nb_classifier.show_most_informative_features(20)
    #print('Classifier accuracy: {}\n'.format(classifier_accuracy_values['mean_accuracy']))
    #print("\nClassification: {}\n".format(classification))
    #print('************************************\n')

    #SAVE RESULTS TO CSV FILE: /sentiment_analyzer/classification_results/results.txt
    save_counter = save_to_csv(values, keyes, prob_neg, prob_pos, classification, save_counter, number_of_file_chunks_processed)

    return save_counter

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
    filt_pos_revs_bigram = preprocessor.filter_stopwords(positive_reviews, training_mode, bigram)
    filt_neg_revs_bigram = preprocessor.filter_stopwords(negative_reviews, training_mode, bigram)

    normalized_reviews_neg = preprocessor.normalize_and_clean_comment(filt_neg_revs)
    normalized_reviews_pos = preprocessor.normalize_and_clean_comment(filt_pos_revs)

    normalized_reviews_neg_bigram = preprocessor.normalize_and_clean_comment(filt_neg_revs_bigram)
    normalized_reviews_pos_bigram = preprocessor.normalize_and_clean_comment(filt_pos_revs_bigram)
    
    '''STEMMING'''

    normalized_reviews_neg_stemmed = preprocessor.stem_sentence(normalized_reviews_neg, training_mode)
    normalized_reviews_pos_stemmed = preprocessor.stem_sentence(normalized_reviews_pos, training_mode)
    normalized_reviews_neg_bigram_stemmed = preprocessor.stem_sentence(normalized_reviews_neg_bigram, training_mode)
    normalized_reviews_pos_bigram_stemmed = preprocessor.stem_sentence(normalized_reviews_pos_bigram, training_mode)

    '''LEMMATIZATION'''
    #normalized_reviews_neg_lem = preprocessor.lemmatization(normalized_reviews_neg, training_mode)
    #normalized_reviews_pos_lem = preprocessor.lemmatization(normalized_reviews_pos, training_mode)
    #normalized_reviews_neg_bigram_lem = preprocessor.lemmatization(normalized_reviews_neg_bigram, training_mode)
    #normalized_reviews_pos_bigram_lem = preprocessor.lemmatization(normalized_reviews_pos_bigram, training_mode)

    #Lemmatized:
    #return normalized_reviews_pos_lem, normalized_reviews_neg_lem, normalized_reviews_neg_bigram_lem, normalized_reviews_pos_bigram_lem
    #Nothing:
    #return normalized_reviews_pos, normalized_reviews_neg, normalized_reviews_neg_bigram, normalized_reviews_pos_bigram
    #Stemming:
    return normalized_reviews_pos_stemmed, normalized_reviews_neg_stemmed, normalized_reviews_neg_bigram_stemmed, normalized_reviews_pos_bigram_stemmed

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
    '''Extract bigram word features'''

    words_bigram = []
    if training_mode:

        for i in iter(ngrams(words_clean, 2)):
            words_bigram.append(i)

    else:
        for i in iter(ngrams(words_clean[0], 2)):
            words_bigram.append(i)

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
    training_and_test_data, all_training_data = split_data(feature_set_positive, feature_set_negative, fold)

    return training_and_test_data, all_training_data