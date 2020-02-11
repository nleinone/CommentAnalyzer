import os
from datetime import datetime
import sys

from parsing import parsing_functions
from preprocessing import preprocessor
from sentiment_analyser import configure_classifiers
from sentiment_analyser import classifier_utils

if __name__ == '__main__':
    '''Main function for the script.
    Takes the following arguments as cmd line arguments (defaults declared):
    
    Cross_validate_classifier == 1
    max_line_count = 100
    
    '''
    
    try:
        cross_validate = sys.argv[1]
        
        if cross_validate == "1":
            print("Cross validate: True")
            cross_validate = True
        elif cross_validate == "0":
            print("Cross validate: False")
            cross_validate = False
        else:
            print("Cross validate: False")
            cross_validate == False
    except Exception as e:
        print("Cross validate: False")
        cross_validate = False 

    try:
        max_line_count = sys.argv[2]
        max_line_count = int(max_line_count)
        print("Maximum line process count: " + str(max_line_count))
    except Exception as e:
        print("Maximum line process count: 100")
        max_line_count = 100

    #Runtime stamp
    datetime_start = datetime.now()

    '''Variables'''
    number_of_lines_processed = 0
    
    cross_validations_fold_ratio = 200

    '''*** INITIAL CONFIGURATIONS ***'''
    print("Configuring classifiers...")

    training_and_test_data, all_training_data = classifier_utils.get_training_and_test_data(cross_validations_fold_ratio)
    nb_classifier, average_values = configure_classifiers.configure_all(training_and_test_data, all_training_data, cross_validate)

    classifier = nb_classifier
    classifier_accuracy_values = average_values

    '''*** INITIAL CONFIGURATIONS ENDS***'''

    '''**** FILE PARSING PROCESS STARTS HERE****'''
    csv_file_names = parsing_functions.fetch_document_names()
    number_of_file_chunks_processed = 0
    line_counter = 0
    lines_left_to_process = True
    keys = []

    for file_name in csv_file_names:    
        while(lines_left_to_process):
            #Variables
            information_collection = []

            '''BIG DATA PARSING'''
            #Count file lines
            line_count = parsing_functions.count_remaining_file_lines(file_name, number_of_lines_processed, max_line_count)

            #Convert file lines to list (Max 100)
            file_lines_list = parsing_functions.convert_file_to_list(line_count, file_name, number_of_lines_processed, max_line_count)
            number_of_lines_processed += line_count
            
            #Distinguish information from file line (For example user_name, time, bot_mood, bot_answer, user_answer):
            for file_line in file_lines_list:
                #is_header = 1, is_descriptive_header = 2, is_not_header = 3
                if number_of_file_chunks_processed == 0 and line_counter == 0:
                    is_header = 1
                elif number_of_file_chunks_processed == 0 and line_counter == 1:
                    is_header = 2
                else:
                    is_header = 3

                information_dictionary, keys = parsing_functions.distinguish_information(file_line, is_header, keys)
                
                
                if (len(information_dictionary) == len(keys)):
                    information_collection.append(information_dictionary)
                line_counter = line_counter + 1
            
            all_comments = parsing_functions.separate_comments_by_bot_identity(information_collection, keys)
            save_counter = 0
            
            sum = 0

            for comment_set in all_comments:
            
                try:
                    #Bot identity and free text location
                    first_comment = comment_set[1]
                    identity = first_comment[keys[2]]
                    print('Processing {} bot answer data...'.format(identity))

                except:
                    continue

                '''*** PARSING ENDS HERE ***'''

                '''*** NATURAL LANGUAGE PREPROCESSING STARTS HERE***'''
                #Preprocess user comments one bot mood data set at time:
                for comment in comment_set[1:]:
                    training_mode = False
                    user_answer = comment[keys[4]]

                    #Tokenize comment
                    tokenized_comment = preprocessor.tokenize_comment(user_answer)

                    #Filter stopwords for unigram
                    bigram = False
                    stopword_filtered_comment_unigram = preprocessor.filter_stopwords(tokenized_comment, training_mode, bigram)

                    #Filter stopwords for bigram
                    bigram = True
                    stopword_filtered_comment_bigram = preprocessor.filter_stopwords(tokenized_comment, training_mode, bigram)

                    #Clean the user answer unigram
                    normalized_comment_unigram = preprocessor.normalize_and_clean_comment(stopword_filtered_comment_unigram)

                    #Clean the user answer bigram
                    normalized_comment_bigram = preprocessor.normalize_and_clean_comment(stopword_filtered_comment_bigram)

                    '''*** NATURAL LANGUAGE PREPROCESSING STOPS HERE***'''

                    '''*** SENTIMENT ANALYSIS WITH NAIVE BAYES STARTS HERE***'''

                    normalized_comment_feature_set_unigram = classifier_utils.extract_feature_unigram(normalized_comment_unigram, training_mode)
                    normalized_comment_feature_set_bigram = classifier_utils.extract_features_bigram(normalized_comment_bigram, training_mode)
                    normalized_comment_feature_set = classifier_utils.extract_features(normalized_comment_unigram, normalized_comment_bigram, training_mode)

                    '''
                    DEBUG PRINTS:

                    print("normalized comment unigram: ")
                    print(normalized_comment_unigram)
                    print("normalized comment bigram: ")
                    print(normalized_comment_bigram)
                    print("normalized_comment_feature_set_unigram: ")
                    print(normalized_comment_feature_set_unigram)
                    print("normalized_comment_feature_set_bigram: ")
                    print(normalized_comment_feature_set_bigram)
                    print("extract_features: ")
                    print(normalized_comment_feature_set)
                    exit()
                    '''

                    probability_result = classifier.prob_classify(normalized_comment_feature_set)

                    save_counter = classifier_utils.print_statistics(probability_result, classifier, normalized_comment_feature_set, comment, classifier_accuracy_values, cross_validate, save_counter, number_of_file_chunks_processed, keys)

            number_of_file_chunks_processed += 1

            if line_count < max_line_count:
                save_counter = 0
                break

    #Runtime stamp
    print("Runtime: {}\n".format(datetime.now() - datetime_start))
