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
    
def convert_file_to_list(file_count, file_name, number_of_lines_processed):
    '''Add lines in list and return that list. Cannot exceed the max_line_amount (100)'''
    lines_list = []
    counter = number_of_lines_processed
    
    with open('././docs/' + file_name) as file:
        file.seek(number_of_lines_processed)
        #data = file.readlines(file_count - number_of_lines_processed)
        for line in file:
            lines_list.append(line)
            if counter == file_count:
                print('Max counter limit exceeded ({})'.format(max_line_amount))
                break
            counter += 1
    file.close()
    
    return lines_list
        
def count_remaining_file_lines(file_name, number_of_lines_processed, max_line_count):
    '''Count, return, and print file lines'''

    counter = number_of_lines_processed
    
    #print("test start counting")
    #print("line count: {}".format(counter))
    
    with open('././docs/' + file_name) as file:
        file.seek(number_of_lines_processed)
        #data = file.readlines(max_line_amount)
        
        for line in file:
            #print(line)
            if counter == number_of_lines_processed + max_line_count:
                print('Max counter limit exceeded ({})'.format(max_line_count))
                break
            counter += 1
    file.close()
    
    #print("test end counting")
    #print("line count: {}".format(counter))
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
    