from colorama import Fore, init, Style
#Add colours:
init()

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
        analyzed_text_index_qualtric = sys.argv[12].split("=")
        analyzed_text_index_qualtric = int(analyzed_text_index_qualtric[1]) - 1
        analyzed_text_index_qualtric = int(analyzed_text_index_qualtric)
        print("Analysed text column number in Qualtric CSV File: " + str(int(analyzed_text_index_qualtric) + 1))
    except Exception as e:
        print(Fore.YELLOW + "Analysed text column number in Qualtric CSV File: -3 (3rd last) (Default)")
        analyzed_text_index_qualtric = -3
    
    max_line_count = 9999
    
    print(Style.RESET_ALL)
    
    prolific_column_numbers = []
    prolific_column_numbers.append(user_id_index_prolific)
    prolific_column_numbers.append(age_index_prolific)
    prolific_column_numbers.append(user_sex_index_prolific)
    prolific_column_numbers.append(user_student_status_index_prolific)
    prolific_column_numbers.append(user_first_language_index_prolific)
    
    return cross_validate, user_message_index_dialogue, condition_index_dialogue, user_id_index_dialogue, user_timestamp_index_dialogue, prolific_column_numbers, analyzed_text_index_qualtric, max_line_count
