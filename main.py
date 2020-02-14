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
parser.add_argument('--analyzed_text_location', help='The column number (CSV file from the Prolific) of the text which the sentiment analysis will be performed. Default=-3')
parser.add_argument('--bottom_range', help='The lowest column number (CSV file from the Prolific) of the Prolific questionnaire with an answer with numeric value. Default=17')
parser.add_argument('--top_range', help='The highest column number (CSV file from the Prolific) of the Prolific questionnaire with an answer with numeric value. Default=40')
parser.add_argument('--user_id_location', help='The column number (CSV file from the Prolific) of the Prolific user ID value. Default=42')
parser.add_argument('--user_id_qualtr_location', help='The column number (CSV file from the Qualtric) of the Qualtric user ID value. Default=2')
parser.add_argument('--age_location_qualtr', help='The column number (CSV file from the Qualtric) of the Qualtric user age value. Default=7')
parser.add_argument('--user_sex_location_qualtr', help='The column number (CSV file from the Qualtric) of the Qualtric user sex value. Default=16')
parser.add_argument('--user_student_sts_location_qualtr', help='The column number (CSV file from the Qualtric) of the Qualtric user student status value. Default=14')
parser.add_argument('--user_first_language_location_qualtr', help='The column number (CSV file from the Qualtric) of the Qualtric user first language information value. Default=17')

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
        Analysed_text_column_location = sys.argv[2].split("=")
        Analysed_text_column_location = int(Analysed_text_column_location[1]) - 1
        Analysed_text_column_location = int(Analysed_text_column_location)
        print("Analysed text column number in Prolific CSV File: " + str(int(Analysed_text_column_location) + 1))
    except Exception as e:
        print(Fore.YELLOW + "Analysed text column number in Prolific CSV File: -3 (3rd last) (Default)")
        Analysed_text_column_location = -3
    
    try:
        bottom_range = sys.argv[3].split("=")
        top_range = sys.argv[4].split("=")
        bottom_range = int(bottom_range[3]) - 1
        top_range = int(top_range[4]) - 1

        print("Bottom column number for question values in Prolific CSV File: " + str(bottom_range + 1))
        print("Top column number for question values in Prolific CSV File: " + str(top_range + 1))
    except Exception as e:
        bottom_range = 17
        top_range = 39
        print("Bottom column number for question values in Prolific CSV File: Column 18 (R) (Default)")
        print("Top column number for question values in Prolific CSV File: Column 40 (AN) (Default)")
    
    try:
        user_id_location = sys.argv[5].split("=")
        user_id_location = int(user_id_location[1]) - 1
        print("User id column number in Prolific CSV File: " + str(user_id_location + 1))
    except Exception as e:
        print("User id column number in Prolific CSV File: 42 (Default)")
        user_id_location = 41
    
    #In case of big data processing is needed:    
    #try:
    #    max_line_count = sys.argv[3]
    #    max_line_count = int(max_line_count)
    #    print("Maximum line process count: " + str(max_line_count))
    #except Exception as e:
    #    print("Maximum line process count: 100")
    #    max_line_count = 100
    max_line_count = 9999
    
    try:
        user_id_qualtric_location = sys.argv[6].split("=")
        user_id_qualtric_location = int(user_id_location[1]) - 1
        print("User id column number Qualtric CSV File: " + str(user_id_qualtric_location + 1))
    except Exception as e:
        print("User id column number Qualtric CSV File: 2 (Default)")
        user_id_qualtric_location = 1
    
    try:
        age_location = sys.argv[7].split("=")
        age_location = int(age_location[1]) - 1
        print("User age column number Qualtric CSV File: " + str(age_location + 1))
    except Exception as e:
        print("User age column number Qualtric CSV File: 7 (Default)")
        age_location = 6
    
    try:
        sex_location = sys.argv[8].split("=")
        sex_location = int(sex_location[1]) - 1
        print("User sex column number Qualtric CSV File: " + str(sex_location + 1))
    except Exception as e:
        print("User sex column number Qualtric CSV File: 16 (Default)")
        sex_location = 15
    
    try:
        students_location = sys.argv[9].split("=")
        students_location = int(students_location[1]) - 1
        print("User student status column number Qualtric CSV File: " + str(students_location + 1))
    except Exception as e:
        print("User student status column number Qualtric CSV File: 14 (Default)")
        students_location = 13
    
    try:
        en_first_lang_location = sys.argv[10].split("=")
        en_first_lang_location = int(en_first_lang_location[1]) - 1
        print("User first language information column number Qualtric CSV File: " + str(en_first_lang_location + 1))
    except Exception as e:
        print("User first language information column number Qualtric CSV File: 17 (Default)")
        en_first_lang_location = 16
    
    
    print(Style.RESET_ALL)
    
    #qualtric_column_numbers:
    #qualtric_column_numbers[0] = age_location 7
    #qualtric_column_numbers[1] = sex_location 16
    #qualtric_column_numbers[3] = students_location 14
    #qualtric_column_numbers[4] = en_first_lang_location 17
    qualtric_column_numbers = []
    qualtric_column_numbers.append(age_location)
    qualtric_column_numbers.append(sex_location)
    qualtric_column_numbers.append(students_location)
    qualtric_column_numbers.append(en_first_lang_location)
    
    return cross_validate, Analysed_text_column_location, bottom_range, top_range, user_id_location, max_line_count, user_id_qualtric_location, qualtric_column_numbers

if __name__ == '__main__':
    '''Main function for the script.
    Takes the following arguments as cmd line arguments (defaults declared):
    '''

    cross_validate, Analysed_text_column_location, bottom_range, top_range, user_id_location, max_line_count, user_id_qualtric_location, qualtric_column_numbers = check_cmd_arguments()
 
    start = time.time()
 
    '''Variables'''
    number_of_lines_processed = 0
    cross_validations_fold_ratio = 200

    '''*** INITIAL CONFIGURATIONS ***'''
    print("Configuring classifiers...")

    training_and_test_data, all_training_data = classifier_utils.get_training_and_test_data(cross_validations_fold_ratio)
    nb_classifier, average_values = configure_classifiers.configure_all(training_and_test_data, all_training_data, cross_validate)

    classifier = nb_classifier
    classifier_accuracy_values = average_values

    '''**** FILE PARSING PROCESS STARTS HERE****'''
    csv_file_names_prolific, csv_qualtric_files = parsing_functions.fetch_document_names()
    
    
    keys = []

    for file_name_prolific, file_name_qualtric in zip(csv_file_names_prolific, csv_qualtric_files):    
        lines_left_to_process = True
        number_of_file_chunks_processed = 0

        file_name = './results/individual_file_results/results_' + str(file_name_prolific) + "_" + str(number_of_file_chunks_processed) + '.csv'
        if os.path.isfile(file_name):
            os.remove(file_name)

        line_counter = 0
        while(lines_left_to_process):
            #Variables
            information_collection = []

            #Count file lines, should be either max_line_count (9999) or all remaining lines which is < 9999
            line_count = parsing_functions.count_remaining_file_lines(file_name_prolific, number_of_lines_processed, max_line_count)

            #Convert file lines to list (Max 100)
            file_lines_list = parsing_functions.convert_file_to_list(line_count, file_name_prolific, number_of_lines_processed)
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

            all_comments, discovered_identities = parsing_functions.separate_comments_by_bot_identity(information_collection, keys)
            save_counter = 0

            sum = 0

            for comment_set in all_comments:
                '''*** NATURAL LANGUAGE PREPROCESSING STARTS HERE***'''
                #Preprocess user comments one bot mood data set at time:
                for comment in comment_set[1:]:
                    #Document structure:
                    #From last column [-1]: Chatbot Identity:
                    #                 [-2]: Prolific ID
                    #                 [-3]: Free description question (Default location)

                    training_mode = False
                    user_answer = comment[keys[Analysed_text_column_location]]
                    
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
                    save_counter = classifier_utils.print_statistics(probability_result, classifier, normalized_comment_feature_set, comment, classifier_accuracy_values, cross_validate, save_counter, number_of_file_chunks_processed, keys, file_name)
                    
                    #Create conclusive results from previously created results file:
            classifier_utils.create_conclusive_results_file(number_of_file_chunks_processed, discovered_identities, keys, file_name, file_name_prolific, file_name_qualtric, bottom_range, top_range, user_id_location, user_id_qualtric_location, qualtric_column_numbers)
            number_of_file_chunks_processed += 1

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
