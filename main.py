import os
import time
import sys
from colorama import Fore, init, Style
#Add colours:
init()

from parsing import parsing_functions
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

#Add command line arguments with describtions:
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--cross_validate', help='Perform a cross validation to the classifier training data with 1/5 split. Input: 0 (Default) = False, 1 = True')
parser.add_argument('--condition_index_dialogue', help='The column number (CSV file from the Dialogue data) of the Dialogue data condition column index. Default=3')
parser.add_argument('--user_message_index_dialogue', help='The column number (CSV file from the Dialogue data) of the Dialogue user message column index. Default=5')
parser.add_argument('--user_id_index_dialogue', help='The column number (CSV file from the Dialogue data) of the Dialogue user id column index. Default=1')
parser.add_argument('--user_timestamp_index_dialogue', help='The column number (CSV file from the Dialogue data) of the Dialogue user datetime column index. Default=2')
parser.add_argument('--user_id_index_prolific', help='The column number (CSV file from the Prolific) of the Prolific user ID value. Default=2')
parser.add_argument('--age_index_prolific', help='The column number (CSV file from the Prolific) of the Prolific user age value. Default=7')
parser.add_argument('--user_sex_index_prolific', help='The column number (CSV file from the Prolific) of the Prolific user sex value. Default=16')
parser.add_argument('--user_student_status_index_prolific', help='The column number (CSV file from the Prolific) of the Prolific user student status value. Default=14')
parser.add_argument('--user_first_language_index_prolific', help='The column number (CSV file from the Prolific) of the Prolific user first language information value. Default=17')
parser.add_argument('--user_id_index_qualtric', help='The column number (CSV file from the Qualtric) of the Prolific user ID value. Default=42')
parser.add_argument('--analyzed_text_index_qualtric', help='The column number (CSV file from the Qualtric) of the text which the sentiment analysis will be performed in pilot study. Default=-3')
#parser.add_argument('--bottom_range', help='The lowest column number (CSV file from the Prolific) of the Prolific questionnaire with an answer with numeric value. Default=17')
#parser.add_argument('--top_range', help='The highest column number (CSV file from the Prolific) of the Prolific questionnaire with an answer with numeric value. Default=40')

args=parser.parse_args()

def check_cmd_arguments():
    '''Check the input values given via command line arguments
    Cross_validate_classifier == 0
    Analysed_text_column_location = -3 (3rd last by default)
    Range of question values to be collected:
    bottom_range = 18 (Default)
    top_range = 40 (Default)
    User-id column number = 8
    '''
    print(Fore.YELLOW)
    try:
        cross_validate = sys.argv[1].split("=")
        cross_validate = cross_validate[1]
        if cross_validate == "1":
            print("Cross validate: True")
            cross_validate = True
        elif cross_validate == "0":
            print("Cross validate: False")
            cross_validate = False
        else:
            print("Cross validate: False (Default)")
            cross_validate == False
    except Exception as e:
        print("Cross validate: False (Default)")
        cross_validate = False 
    
    try:
        condition_index_dialogue = sys.argv[2].split("=")
        condition_index_dialogue = int(condition_index_dialogue[1]) - 1
        print("Bot condition column index: " + str(condition_index_dialogue + 1))
    except Exception as e:
        print("Bot condition column index: 3 (Default)")
        condition_index_dialogue = 2
    
    try:
        user_message_index_dialogue = sys.argv[3].split("=")
        user_message_index_dialogue = int(user_message_index_dialogue[1]) - 1
        print("User message column index: " + str(user_message_index_dialogue + 1))
    except Exception as e:
        print("User message column index: 5 (Default)")
        user_message_index_dialogue = 4
    
    try:
        user_id_index_dialogue = sys.argv[4].split("=")
        user_id_index_dialogue = int(user_id_index_dialogue[1]) - 1
        print("User id column index in dialogue data: " + str(user_id_index_dialogue + 1))
    except Exception as e:
        print("User id column index in dialogue data: 1 (Default)")
        user_id_index_dialogue = 0
    
    try:
        user_timestamp_index_dialogue = sys.argv[5].split("=")
        user_timestamp_index_dialogue = int(user_timestamp_index_dialogue[1]) - 1
        print("User datetime column index in dialogue data: " + str(user_timestamp_index_dialogue + 1))
    except Exception as e:
        print("User datetime column index in dialogue data: 2 (Default)")
        user_timestamp_index_dialogue = 1
    
    
    try:
        user_id_index_prolific = sys.argv[6].split("=")
        user_id_index_prolific = int(user_id_index_prolific[1]) - 1
        print("User id column number Prolific CSV File: " + str(user_id_index_prolific + 1))
    except Exception as e:
        print("User id column number Prolific CSV File: 2 (Default)")
        user_id_index_prolific = 1
    
    try:
        age_index_prolific = sys.argv[7].split("=")
        age_index_prolific = int(age_index_prolific[1]) - 1
        print("User age column number Prolific CSV File: " + str(age_index_prolific + 1))
    except Exception as e:
        print("User age column number Prolific CSV File: 7 (Default)")
        age_index_prolific = 6
    
    try:
        user_sex_index_prolific = sys.argv[8].split("=")
        user_sex_index_prolific = int(user_sex_index_prolific[1]) - 1
        print("User sex column number Qualtric CSV File: " + str(user_sex_index_prolific + 1))
    except Exception as e:
        print("User sex column number Qualtric CSV File: 16 (Default)")
        user_sex_index_prolific = 15
    
    try:
        user_student_status_index_prolific = sys.argv[9].split("=")
        user_student_status_index_prolific = int(user_student_status_index_prolific[1]) - 1
        print("User student status column number Qualtric CSV File: " + str(user_student_status_index_prolific + 1))
    except Exception as e:
        print("User student status column number Qualtric CSV File: 14 (Default)")
        user_student_status_index_prolific = 13
    
    try:
        user_first_language_index_prolific = sys.argv[10].split("=")
        user_first_language_index_prolific = int(user_first_language_index_prolific[1]) - 1
        print("User first language information column number Qualtric CSV File: " + str(user_first_language_index_prolific + 1))
    except Exception as e:
        print("User first language information column number Qualtric CSV File: 17 (Default)")
        user_first_language_index_prolific = 16
    
    try:
        user_id_index_qualtric = sys.argv[11].split("=")
        user_id_index_qualtric = int(user_id_index_qualtric[1]) - 1
        print("User id column number in Prolific CSV File: " + str(user_id_index_qualtric + 1))
    except Exception as e:
        print("User id column number in Prolific CSV File: 42 (Default)")
        user_id_index_qualtric = 41
    
    try:
        analyzed_text_index_qualtric = sys.argv[12].split("=")
        analyzed_text_index_qualtric = int(analyzed_text_index_qualtric[1]) - 1
        analyzed_text_index_qualtric = int(analyzed_text_index_qualtric)
        print("Analysed text column number in Qualtric CSV File: " + str(int(analyzed_text_index_qualtric) + 1))
    except Exception as e:
        print(Fore.YELLOW + "Analysed text column number in Qualtric CSV File: -3 (3rd last) (Default)")
        analyzed_text_index_qualtric = -3
    
    #try:
    #    bottom_range = sys.argv[3].split("=")
    #    top_range = sys.argv[4].split("=")
    #    bottom_range = int(bottom_range[3]) - 1
    #    top_range = int(top_range[4]) - 1

    #    print("Bottom column number for question values in Prolific CSV File: " + str(bottom_range + 1))
    #    print("Top column number for question values in Prolific CSV File: " + str(top_range + 1))
    #except Exception as e:
    #    bottom_range = 17
    #    top_range = 39
    #    print("Bottom column number for question values in Prolific CSV File: Column 18 (R) (Default)")
    #    print("Top column number for question values in Prolific CSV File: Column 40 (AN) (Default)")
    
    max_line_count = 9999
    
    print(Style.RESET_ALL)
    
    prolific_column_numbers = []
    prolific_column_numbers.append(user_id_index_prolific)
    prolific_column_numbers.append(age_index_prolific)
    prolific_column_numbers.append(user_sex_index_prolific)
    prolific_column_numbers.append(user_student_status_index_prolific)
    prolific_column_numbers.append(user_first_language_index_prolific)
    
    return cross_validate, user_message_index_dialogue, condition_index_dialogue, user_id_index_dialogue, user_timestamp_index_dialogue, prolific_column_numbers, user_id_index_qualtric, analyzed_text_index_qualtric, max_line_count

if __name__ == '__main__':
    '''Main function for the script.
    Takes the following arguments as cmd line arguments (defaults declared):
    '''

    cross_validate, user_message_index_dialogue, condition_index_dialogue, user_id_index_dialogue, user_timestamp_index_dialogue, prolific_column_numbers, user_id_index_qualtric, analyzed_text_index_qualtric, max_line_count = check_cmd_arguments()
 
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
            
            print("\n len all_comments: " + str(len(all_comments)))
            #print("\n discovered_conditions: " + str(discovered_conditions))
            
            sum = 0

            for comment_set in all_comments:
                print("\ncomment " + str(comment_set))
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
                    
                    print("\nuser_answer " + str(user_answer))
                    #print("\nkeys: " + str(keys))
                    #print("\n user_answer: " + str(user_answer))
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
                    save_counter = classifier_utils.print_statistics(condition, probability_result, classifier, normalized_comment_feature_set, classifier_accuracy_values, cross_validate, save_counter, number_of_file_chunks_processed, keys, file_name_dialogue, user_answer, user_id)
                    
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
