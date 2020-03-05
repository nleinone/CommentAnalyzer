#Add command line arguments with describtions:
from colorama import Fore, init, Style
#Add colours:
init()
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--cross_validate', help='Perform a cross validation to the classifier training data with 1/5 split. Input: 0 (Default) = False, 1 = True')
parser.add_argument('--analyzed_text_location_qualtric', help='The column number of the text which the sentiment analysis will be performed in the Qualtric CSV file. Default=41')
parser.add_argument('--user_id_location_qualtric', help='The column number of the user ID value in the Qualtric CSV file. Default=42')
parser.add_argument('--duration_qualtric', help='The column number of the duration value in the Qualtric CSV file. Default=6')
parser.add_argument('--user_id_location_prolific', help='The column number of the user ID value in the Prolific CSV file. Default=2')
parser.add_argument('--age_location_prolific', help='The column number of the user age value in the Prolific CSV file. Default=7')
parser.add_argument('--user_sex_location_prolific', help='The column number of the user sex value in the Prolific CSV file. Default=16')
parser.add_argument('--user_student_status_location_prolific', help='The column number of the user student status value in the Prolific CSV file. Default=14')
parser.add_argument('--user_first_language_location_prolific', help='The column number of the user\'s first language status value in the Prolific CSV file. Default=17')

args=parser.parse_args()

def check_cmd_arguments():
    '''Check the input values given via command line arguments.'''
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
        analyzed_text_location_qualtric = sys.argv[2].split("=")
        analyzed_text_location_qualtric = int(analyzed_text_location_qualtric[1]) - 1
        analyzed_text_location_qualtric = int(analyzed_text_location_qualtric)
        print("Analysed text column number in Qualtric CSV File: " + str(int(analyzed_text_location_qualtric) + 1))
    except Exception as e:
        print(Fore.YELLOW + "Analysed text column number in Qualtric CSV File: 41 (Default)")
        analyzed_text_location_qualtric = -3
    
    try:
        user_id_location_qualtric = sys.argv[3].split("=")
        user_id_location_qualtric = int(user_id_location_qualtric[1]) - 1
        print("User id column number in Qualtric CSV File: " + str(user_id_location_qualtric + 1))
    except Exception as e:
        print("User id column number in Qualtric CSV File: 42 (Default)")
        user_id_location_qualtric = 41
    
    max_line_count = 9999
    
    try:
        duration_qualtric = sys.argv[4].split("=")
        duration_qualtric = int(duration_qualtric[1]) - 1
        duration_qualtric = int(duration_qualtric)
        print("Duration column number in Qualtric CSV File: " + str(int(duration_qualtric) + 1))
    except Exception as e:
        print(Fore.YELLOW + "Duration column number in Qualtric CSV File: 6 (Default)")
        duration_qualtric = 5
    
    try:
        user_id_location_prolific = sys.argv[5].split("=")
        user_id_location_prolific = int(user_id_location_prolific[1]) - 1
        print("User id column number in Prolific CSV File: " + str(user_id_location_prolific + 1))
    except Exception as e:
        print("User id column number in Prolific CSV File: 2 (Default)")
        user_id_location_prolific = 1
    
    try:
        age_location_prolific = sys.argv[6].split("=")
        age_location_prolific = int(age_location_prolific[1]) - 1
        print("User age column number in Prolific CSV File: " + str(age_location_prolific + 1))
    except Exception as e:
        print("User age column number in Prolific CSV File: 7 (Default)")
        age_location_prolific = 6
    
    try:
        user_sex_location_prolific = sys.argv[7].split("=")
        user_sex_location_prolific = int(user_sex_location_prolific[1]) - 1
        print("User sex column number in Prolific CSV File: " + str(user_sex_location_prolific + 1))
    except Exception as e:
        print("User sex column number in Prolific CSV File: 16 (Default)")
        user_sex_location_prolific = 15
    
    try:
        user_student_status_location_prolific = sys.argv[8].split("=")
        user_student_status_location_prolific = int(user_student_status_location_prolific[1]) - 1
        print("User student status column number in Prolific CSV File: " + str(user_student_status_location_prolific + 1))
    except Exception as e:
        print("User student status column number in Prolific CSV File: 14 (Default)")
        user_student_status_location_prolific = 13
    
    try:
        user_first_language_location_prolific = sys.argv[9].split("=")
        user_first_language_location_prolific = int(user_first_language_location_prolific[1]) - 1
        print("User first language information column number in Prolific CSV File: " + str(user_first_language_location_prolific + 1))
    except Exception as e:
        print("User first language information column number in Prolific CSV File: 17 (Default)")
        user_first_language_location_prolific = 16
    
    print(Style.RESET_ALL)
    
    prolific_column_numbers = []
    prolific_column_numbers.append(age_location_prolific)
    prolific_column_numbers.append(user_sex_location_prolific)
    prolific_column_numbers.append(user_student_status_location_prolific)
    prolific_column_numbers.append(user_first_language_location_prolific)
    
    return cross_validate, analyzed_text_location_qualtric, user_id_location_qualtric, max_line_count, duration_qualtric, user_id_location_prolific, prolific_column_numbers
