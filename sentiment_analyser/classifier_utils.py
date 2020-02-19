from random import shuffle
from nltk import ngrams
from preprocessing import preprocessor
import os.path
from colorama import Fore
'''
REFERENCES:

Above link demonstrates the use of movie review data and nltk Naive Bayes classifier library for sentiment analysis:
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
import time
import csv
#print("\n: " + str())
#REFERENCES:
#https://realpython.com/python-csv/
    
def collect_sentiment_score_from_dialogue_data(file, count_identity_amount, sum_of_values_positive, sum_of_values_negative, condition):
    '''Collect sentiment scores using given column location indicators'''
    
    csv_reader = csv.reader(file, delimiter='|')
    user_ids = []
    for row in csv_reader:
        #ingore headers
        try:
            #ID key position: user id, comment, neg, pos, class, condition
            if row[-1] == condition:
                
                user_ids.append(row[0])
                count_identity_amount += 1
                positive_prob = row[3]
                negative_prob = row[2]
                sum_of_values_positive = sum_of_values_positive + float(positive_prob)
                sum_of_values_negative = sum_of_values_negative + float(negative_prob)
               
        except ValueError:
            continue
            
    print("\nCollecting sentiment scores for condition: {}...Done!".format(condition))
    return [sum_of_values_negative / count_identity_amount, sum_of_values_positive / count_identity_amount, count_identity_amount, user_ids], count_identity_amount

def remove_previous_file(conc_fn_profilic):
    '''Check and remove previously created file'''
    #Remove previous file:
    if os.path.isfile(conc_fn_profilic):
        os.remove(conc_fn_profilic)

def calculate_average_age(ages):
    
    sum = 0
    for age in ages:
        try:
            sum = sum + int(age)
        except ValueError as e:
            print("Invalid file's age information!")
            continue
    
    try:
        average_age = sum / len(ages)
    except ZeroDivisionError:
        average_age = sum

    return average_age
    
def create_prolific_data_file(condition_averages_dict, file_name_prolific, prolific_column_numbers):
    '''Create results file from the qualtric data file'''
    #condition_averages_dict:
    #{IDENTITY: [avg_neg_prob, avg_pos_prob, count_identity_amount, question_points_average, user_ids]}

    user_id_index = prolific_column_numbers[0]
    age_index = prolific_column_numbers[1]
    sex_index = prolific_column_numbers[2]
    students_status_index = prolific_column_numbers[3]
    en_first_lang_index = prolific_column_numbers[4]
    
    conditions = condition_averages_dict.keys()
    
    row_info = []
    row_info.append('Condition')
    row_info.append('Average Age')
    row_info.append('Males')
    row_info.append('Females')
    row_info.append('Students')
    row_info.append('Users with First Language English')
    row_info.append('Total Number of Users (Consent given)')
    
    result_path_folder = './results/'
    results_file_name_prolific = 'results_' + file_name_prolific
    result_file_path = result_path_folder + results_file_name_prolific
    
    remove_previous_file(result_file_path)
    
    #Create headers:
    with open(result_path_file, 'a', newline='') as cfile:
        writer = csv.writer(cfile)
        writer.writerow(row_info)
    cfile.close()

    #Unpack information for each identity, and search corresponding information from the Qualtric file:
    for condition in conditions:
        row_info = []
        ages = []
        males = 0
        females = 0
        students = 0
        en_first_lang = 0
        total_number = 0
        
        condition_info = condition_averages_dict[condition]
        condition_user_ids = condition_info[4]
        
        print("\nCollecting user information data for condition: {}...".format(condition))
        
        prolific_file_path = './docs/prolific_docs/' + prolific_file_name
        
        for user_id in condition_user_ids:
        
            with open(prolific_file_path) as file:
                csv_reader = csv.reader(file, delimiter=',')
                for row in csv_reader:
                    try:
                        if row[user_id_index] == user_id:
                            ages.append(row[age_index])
                            print("\nsex" + str(sex_index))
                            print("\nstudent" + str(students_status_index))
                            print("\nlang" + str(en_first_lang_index))
                            if row[sex_index] == "Male":
                                print("\n1")
                                males += 1
                            
                            if row[sex_index] == "Female":
                                print("\n2")
                                females += 1
                            if row[students_status_index] == "Yes":
                                students += 1
                            if row[en_first_lang_index] == "English":
                                en_first_lang += 1
                            total_number += 1    

                    except IndexError:
                        continue
                        
        file.close()
        avg_age = calculate_average_age(ages)
    
        #Add collected data to the condition result file:
        row_info.append(identity)
        row_info.append(avg_age)
        row_info.append(males)
        row_info.append(females)
        row_info.append(students)
        row_info.append(en_first_lang)
        row_info.append(total_number)
        
        with open(result_file_path, 'a', newline='') as cfile2:
            writer = csv.writer(cfile2)
            writer.writerow(row_info)
            
    print("\nProlific data results saved in {}".format(result_file_path))
    
def create_qualtric_data_file(identity_averages_dict, conc_fn_profilic):
    '''Create results file from the prolific data file'''
    
    print("\nCreating Prolific results file...", end="\r")
    remove_previous_file(conc_fn_profilic)
    
    row_info = []
    row_info.append('Chatbot Condition')
    row_info.append('Average of Negative probability')
    row_info.append('Average of Positive probability')
    row_info.append('Sample size')
    row_info.append('Average Questionnaire Score')
    
    #Create headers:
    with open(conc_fn_profilic, 'a', newline='') as cfile:
        writer = csv.writer(cfile)
        writer.writerow(row_info)
    cfile.close()
    
    for key in identity_averages_dict.keys():
        row_info = []
        values_for_id = identity_averages_dict[key]
        avg_neg = values_for_id[0]
        avg_pos = values_for_id[1]
        sample_size = values_for_id[2]
        question_score_avg = values_for_id[3]
        
        row_info.append(key)
        row_info.append(avg_neg)
        row_info.append(avg_pos)
        row_info.append(sample_size)
        row_info.append(question_score_avg)

        with open(conc_fn_profilic, 'a', newline='') as cfile2:
            writer = csv.writer(cfile2)
            writer.writerow(row_info)
            
        cfile2.close()   
    print("\nCreating Prolific results file...Done!")

def create_dialogue_results_file(condition_averages_dict, file_name_dialogue, discovered_conditions):
    
    #{condition: [sum_of_values_negative / count_identity_amount, sum_of_values_positive / count_identity_amount, count_identity_amount, user_ids]}
    
    row_info = []
    row_info.append('Condition')
    row_info.append('Avg. Propability of Positive Sentiment')
    row_info.append('Avg. Propability of Negative Sentiment')
    row_info.append('Sample Size')
    
    
    result_path_folder = './results/'
    results_file_name_dialogue = 'results_' + file_name_dialogue
    result_file_path = result_path_folder + results_file_name_dialogue
    
    remove_previous_file(result_file_path)
    
    #Create headers:
    with open(result_file_path, 'a', newline='') as cfile:
        writer = csv.writer(cfile)
        writer.writerow(row_info)
    cfile.close()
    
    for condition in discovered_conditions:
        print("\ndiscovered_conditions: " + str(discovered_conditions))
        print("\ncondition: " + str(condition))
        values = []
        condition_specific_info_set = condition_averages_dict[condition]
        values.append(condition)
        values.append(condition_specific_info_set[1])
        values.append(condition_specific_info_set[0])
        values.append(condition_specific_info_set[2])
        
        with open(result_file_path, 'a', newline='') as cfile:
            writer = csv.writer(cfile)
            writer.writerow(values)
            
    cfile.close()
    
    print('\nDialogue data results saved in: {}'.format(result_file_path))
    
    
def create_result_files(number_of_file_chunks_processed, discovered_conditions, keys, file_name_prolific, prolific_column_numbers, file_name_dialogue):
    '''Create conclusive results from processed document'''
    
    condition_averages_dict = {}
    avg_values = []
    individual_dialogue_result_path = './results/individual_file_results/individual_results_' + file_name_dialogue 
    
    for condition in discovered_conditions:
        count_condition_amount = 0
        sum_of_values_positive = 0
        sum_of_values_negative = 0
        with open(individual_dialogue_result_path) as file:
            
            #Negative average, Positive average, amount of samples
            condition_averages_dict[condition], count_condition_amount = collect_sentiment_score_from_dialogue_data(file, count_condition_amount, sum_of_values_positive, sum_of_values_negative, condition)
    
    create_dialogue_results_file(condition_averages_dict, file_name_dialogue, discovered_conditions)
    
    #path__results_profilic = './results/Qualtric_Results_'
    #conc_fn_results_prolific = path_profilic + str(file_name_qualtric)
    #path_prolific_docs_folder = './docs/prolific_docs/'
    #prolific_file_path = path_prolific_docs_folder + str(file_name_prolific)
    
    #create_qualtric_data_file(identity_averages_dict, conc_fn_profilic)
    #create_prolific_data_file(condition_averages_dict, file_name_prolific, prolific_column_numbers)
    #print("\nProlific data results saved in {}".format(conc_fn_profilic))
    
def save_to_csv(condition, user_answer, user_id, keys, prob_neg, prob_pos, classification, save_counter, number_of_file_chunks_processed, file_name_dialogue):
    ''''''
    #Add other information:'
    individual_dialogue_result_path = './results/individual_file_results/individual_results_' + file_name_dialogue 
    
    if save_counter == 0:
        remove_previous_file(individual_dialogue_result_path)
        
        row_info = []
        #row_info = keys.copy()
        row_info.append('User ID')
        row_info.append('Comment')
        row_info.append('Negative probability')
        row_info.append('Positive probability')
        row_info.append('Classification')
        row_info.append('Condition')
        #print("row_info: " + str(row_info))
        with open(individual_dialogue_result_path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter="|")
            writer.writerow(row_info)
        file.close()
        
    #Add other values:
    values = []
    values.append(user_id)
    values.append(user_answer)
    values.append(prob_neg)
    values.append(prob_pos)
    values.append(classification)
    values.append(condition)

    with open(individual_dialogue_result_path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter="|")
        writer.writerow(values)

    file.close()
    save_counter = 1
    return save_counter
     
def print_statistics(condition, probability_result, nb_classifier, normalized_comment_feature_set, classifier_accuracy_values, cross_validate, save_counter, number_of_file_chunks_processed, keyes, file_name_dialogue, user_answer, user_id):
    '''Print various different statistics about the client response.'''

    prob_pos = probability_result.prob("pos")
    prob_neg = probability_result.prob("neg")
    #(user_name, time, bot_mood, bot_answer, user_answer):

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

    
    save_counter = save_to_csv(condition, user_answer, user_id, keyes, prob_neg, prob_pos, classification, save_counter, number_of_file_chunks_processed, file_name_dialogue)

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
