import os
import time
import sys
from colorama import Fore, init, Style
#Add colours:
init()

from parsing import parsing_functions, command_arguments
from preprocessing import preprocessor
from sentiment_analyser import configure_classifiers
from sentiment_analyser import classifier_utils

'''
REFERENCES:
Using Python zip():
https://realpython.com/python-zip-function/

Using argparser for command line inputs:
https://docs.python.org/2/library/argparse.html

Using colorama to create colorful commandline outputs:
https://pypi.org/project/colorama/

'''

if __name__ == '__main__':
    '''Main function for the script.
    Takes the following arguments as cmd line arguments (defaults declared):
    '''

    cross_validate, user_message_index_dialogue, condition_index_dialogue, user_id_index_dialogue, user_timestamp_index_dialogue, prolific_column_numbers, analyzed_text_index_qualtric, max_line_count = command_arguments.check_cmd_arguments()
 
    start = time.time()
 
    '''Variables'''
    number_of_lines_processed = 0
    cross_validations_fold_ratio = 200

    '''*** INITIAL CONFIGURATIONS ***'''
    print("Configuring classifiers...")

    training_and_test_data, all_training_data = classifier_utils.get_training_and_test_data(cross_validations_fold_ratio)
    nb_classifier, average_values = configure_classifiers.configure_all(training_and_test_data, all_training_data, cross_validate)
    
    #classifier = ''
    #classifier_accuracy_values = 0
    classifier = nb_classifier
    classifier_accuracy_values = average_values

    '''**** FILE PARSING PROCESS STARTS HERE****'''
    csv_qualtric_files, csv_file_names_prolific, csv_dialogue_files = parsing_functions.fetch_document_names()
    
    
    keys = []

    for file_name_qualtric, file_name_prolific, file_name_dialogue in zip(csv_qualtric_files, csv_file_names_prolific, csv_dialogue_files):    
        lines_left_to_process = True
        number_of_file_chunks_processed = 0

        dialogue_result_file_name = './results/individual_file_results/results_' + str(file_name_dialogue) + "_" + str(number_of_file_chunks_processed) + '.csv'
        if os.path.isfile(dialogue_result_file_name):
            os.remove(dialogue_result_file_name)

        line_counter = 0
        while(lines_left_to_process):
            #Variables
            information_collection = []

            #Count file lines, should be either max_line_count (9999) or all remaining lines which is < 9999
            line_count = parsing_functions.count_remaining_file_lines(file_name_dialogue, number_of_lines_processed, max_line_count)
            
            #print("\n line count: " + str(line_count))
            
            #Convert file lines to list (Max 100)
            file_lines_list = parsing_functions.convert_file_to_list(line_count, file_name_dialogue, number_of_lines_processed)
            number_of_lines_processed += line_count
            
            #print("\nfile_lines_list" + str(len(file_lines_list)))
            
            #Distinguish information from file line (For example user_name, time, bot_mood, bot_answer, user_answer):
            for file_line in file_lines_list:
                #is_header = 1, is_descriptive_header = 2, is_not_header = 3
                if number_of_file_chunks_processed == 0 and line_counter == 0:
                    is_header = 1
                else:
                    is_header = 0
                
                
                #print("\n file_line: " + str(file_line))
                
                information_dictionary, keys = parsing_functions.distinguish_information(file_line, is_header, keys)
                
                #print("\n information_collection0: " + str(len(information_collection)))
                #print("\n information_collection element: " + str(information_dictionary))
                #print("\n keys: " + str(keys))
                #if (len(information_dictionary) == len(keys)):
                information_collection.append(information_dictionary)
                line_counter = line_counter + 1
                
                
            #print("\information_collection0 " + str(information_collection[:5]))
            #sys.exit()
            all_comments, discovered_conditions = parsing_functions.separate_comments_by_condition(information_collection, keys, condition_index_dialogue, user_id_index_dialogue, user_timestamp_index_dialogue)
            save_counter = 0
            
            sum = 0

            for comment_set in all_comments:
                '''*** NATURAL LANGUAGE PREPROCESSING STARTS HERE***'''
                #Preprocess user comments one bot mood data set at time:
                for comment in comment_set:
                    #Document structure:
                    #From last column [-1]: Chatbot Identity:
                    #                 [-2]: Prolific ID
                    #                 [-3]: Free description question (Default location)

                    training_mode = False
                    user_answer = comment[keys[user_message_index_dialogue]]
                    user_id = comment[keys[user_id_index_dialogue]]
                    condition = comment[keys[condition_index_dialogue]]
                    
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

                    '''*** SENTIMENT ANALYSIS WITH NAIVE BAYES STARTS HERE***'''
                    normalized_comment_feature_set_unigram = classifier_utils.extract_feature_unigram(normalized_comment_unigram, training_mode)
                    normalized_comment_feature_set_bigram = classifier_utils.extract_features_bigram(normalized_comment_bigram, training_mode)
                    normalized_comment_feature_set = classifier_utils.extract_features(normalized_comment_unigram, normalized_comment_bigram, training_mode)

                    probability_result = classifier.prob_classify(normalized_comment_feature_set)
                    
                    #Create results file:
                    
                    #Comment info to be saved:
                    cleaned_comment_len = len(normalized_comment_unigram[0])
                    print("clean comment: " + str(cleaned_comment_len))
                    pos_tag_counts = preprocessor.get_pos_tag_counts(normalized_comment_unigram[0])
                    
                    
                    save_counter = classifier_utils.print_statistics(condition, probability_result, classifier, normalized_comment_feature_set, classifier_accuracy_values, cross_validate, save_counter, number_of_file_chunks_processed, keys, file_name_dialogue, user_answer, user_id, cleaned_comment_len, pos_tag_counts)
                    
                    #Create conclusive results from previously created results file:                                        #user_id_index_prolific, age_index_prolific, user_sex_index_prolific, user_student_status_index_prolific, user_first_language_index_prolific
            classifier_utils.create_result_files(number_of_file_chunks_processed, discovered_conditions, keys, file_name_prolific, prolific_column_numbers, file_name_dialogue)
            number_of_file_chunks_processed += 1
            #sys.exit()
            #For possible file chunking operations in case of big data.
            if line_count < max_line_count:
                lines_left_to_process = False
                line_count = 0
                save_counter = 0
                break
            else:
                line_count = 0

    #Runtime stamp
    end = time.time()
    print("Runtime: {} seconds.\n".format(end - start))
