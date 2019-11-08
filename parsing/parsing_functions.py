import os


def separate_comments_by_bot_mood(information_collection):
    
    happy_bot_comments = []
    happysad_bot_comments = []
    sad_bot_comments = []
    neutral_bot_comments = []
    hello_bot_comments = []
    
    for comment in information_collection:
        if comment['bot_mood'] == 'happy':
            happy_bot_comments.append(comment)
        elif comment['bot_mood'] == 'happysad':
            happysad_bot_comments.append(comment)
        elif comment['bot_mood'] == 'sad':
            sad_bot_comments.append(comment)
        elif comment['bot_mood'] == 'neutral':
            neutral_bot_comments.append(comment)
        elif comment['bot_mood'] == 'neutral':
            hello_bot_comments.append(comment)
    return happy_bot_comments, happysad_bot_comments, sad_bot_comments, neutral_bot_comments, hello_bot_comments
    
def distinguish_information(file_line):
    '''Convert line to dictionary with following keys: user_name, time, bot_mood, bot_answer, user_answer'''

    file_line_splitted = file_line.split('"')
    file_line_splitted = file_line_splitted[1::2]
    
    keys = ['user_name', 'time', 'bot_mood', 'bot_answer', 'user_answer']
    dict = {}
    
    for index in range(len(keys)):
        dict[keys[index]] = file_line_splitted[index]
    
    return dict
    
def convert_file_to_list(file_count, file_name):
    '''Add lines in list and return that list. Cannot exceed the max_line_amount (100)'''
    lines_list = []
    counter = 0
    
    with open('././docs/' + file_name, 'r') as file:
        for line in file:
            lines_list.append(line)
            if counter == file_count:
                print('Max counter limit exceeded ({})'.format(max_line_amount))
                break
            counter += 1
    file.close()
    
    return lines_list
        
def count_file_lines(csv_file_names):
    '''Count, return, and print file lines'''
    max_line_amount = 100
    counter = 0
    for file_name in csv_file_names:
        with open('././docs/' + file_name, 'r') as file:
            for line in file:
                if counter == max_line_amount:
                    print('Max counter limit exceeded ({})'.format(max_line_amount))
                    break
                counter += 1
        file.close()
    
    return counter

def fetch_document_names():
    '''Fetch csv files from ./docs/'''
    
    file_location = './docs'
    csv_file_names = []
    file_names = os.listdir(file_location)
    for file_name in file_names:
        if file_name.endswith((".csv")):
            csv_file_names.append(file_name)
    
    return csv_file_names
    