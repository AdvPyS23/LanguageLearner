# -------------------------------------------------
# Quinn Alexander Coxon & Santiago Marin Martinez
# Language Learner App
# Advanced Python FS2023
# -------------------------------------------------

#%% - Setup

# Import Libraries
import pandas as pd
from os import listdir, getcwd
import PySimpleGUI as sg

# Define vocabulary class
class vocabulary:
    #Data structure
    def __init__(self):
        self.data = pd.DataFrame(columns=['word', 'translation', 'pronunciation', 'example', 'topic', 'part of speech', 'attempts', 'successes'])

    #Data manipulation functions
    def add_word(self, word, translation, pronunciation, example, topic, pos, attempts = 0, successes = 0):
        new_row = {'word': word, 'translation': translation, 'pronunciation': pronunciation, 'example': example, 'topic': topic, 'part of speech': pos, 'attempts': attempts, 'successes': successes}
        self.data = pd.concat([self.data,pd.DataFrame([new_row])], ignore_index=True)

    def save_data(self, filename):
        self.data.to_csv(filename, index=False)

    def load_data(self, filename):
        self.data = pd.read_csv(filename)

    def reset(self):
        self.data[['attempts','successes']] = 0

    #Quiz setup functions
    def new_attempt(self, word: str, success: bool):
        self.data.loc[self.data['word'] == word, 'attempts'] += 1
        if success:
            self.data.loc[self.data['word'] == word, 'successes'] += 1

    def get_familiarity(self,word):
        row = self.data.loc[self.data['word'] == word]
        attempts = row.at[row.index[0], 'attempts']
        successes = row.at[row.index[0], 'successes']
        familiarity = successes/attempts
        return(familiarity)

    def get_topics(self):
        topics = list(self.data['topic'].unique())
        return(topics)

    def get_pos(self):
        pos = list(self.data['part of speech'].unique())
        return(pos)

    #Identifier functions (Retrieves words from identifier)
    def get_words_topic(self, topic=None):
        if topic:
            return self.data[self.data['topic'] == topic]

        else:
            return self.data

    def get_words_pos(self, pos=None):
        if pos:
            return self.data[self.data['part of speech'] == pos]
        else:
            return self.data

    def get_words_familiar(self, familiar=None):
        #Takes float as percentage of correct attempts and threshold filters vocabulary
        if familiar:
            return self.data[self.data['successes'] <= familiar]
        else:
            return self.data

# Find languages already stored
path = getcwd()
allfiles = listdir(path)
languages = [filename for filename in allfiles if filename.endswith("csv")]
languages = [filename.replace('.csv', '') for filename in languages]




#%% - GUI

# Startup Window
def startup_window():

    startup_layout = [[sg.Text('Welcome! Select the language you want to practice, or start a new one.')],
                [sg.Button(lang) for lang in languages],
                [sg.Button('New Language...')],
                [sg.Button('Quit')]]


    startup_window = sg.Window('Window Title', startup_layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = startup_window.read()
        if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks Quit
            break

        if event == 'New Language...':
            start_newlanguage()

        if event != 'New Language...' and event != 'Quit':
            globals()['current_language_name'] = event
            globals()['current_language'] = vocabulary()
            current_language.load_data(current_language_name + '.csv')
            language_home()

    startup_window.close()


# New Language Start Up
def start_newlanguage():
    layout = [
        [sg.Text('Enter the name of the language:',justification='center')],
        [sg.Input(justification='center')],
        [sg.Button('Enter'),sg.Button('Cancel')]]
    window = sg.Window("Start a new language", layout)
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Enter":
            languages.append(values[0])
            new_language_name = values[0]
            globals()[new_language_name] = vocabulary()
            globals()[new_language_name].save_data(new_language_name + '.csv')
            break
    window.close()
    startup_window()


# Language Home
def language_home():
    layout = [
        [sg.Text(f"Let's get ready to learn some {current_language_name}!",justification='center')],
        [sg.Button('Input'),sg.Button('Quiz')],
        [sg.Button('View Progress'),sg.Button('Go Back')]]
    window = sg.Window(current_language_name,layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Go Back':
            break

        if event == 'Input':
            add_vocabulary()

        if event == 'Quiz':
            quiz_menu()

    window.close()


# Quizzes setup
def quiz_menu():
    topics_list = current_language.get_topics()
    pos_list = current_language.get_pos()

    layout = [
            [sg.Text(f'Setup your quiz - Leave empty for random', justification='center')],
            [sg.Text(f'Number of words'), sg.Input(key='n_words')],
            [sg.Text('By topic:'), sg.DropDown(topics_list, key='topic_dropdown')],
            [sg.Text('By part of speech:'), sg.DropDown(pos_list, key='pos_dropdown')],
            [sg.Button("Let's go!"), sg.Button('Go back')]]
    window = sg.Window(current_language_name + "Quiz", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "Let's go!":
            test_set = current_language.get_words_topic(topic = values['topic_dropdown'])
            test_set = pd.merge(test_set,current_language.get_words_pos(pos = values['pos_dropdown']))
            #Check that number of words has been given
            if values['n_words']:
                #Check that Number of words are numbers or empty
                if values['n_words'][-1] not in ('0123456789'):
                    sg.popup("Only digits for 'Number of words' allowed")
                    window.close()
                    quiz_menu()
                else:
                    n_words = int(values['n_words'])
            else:
                n_words = 10
            #Check that it is smaller than full test set
            if n_words <= test_set.shape[0]:
                test_set = test_set[["word", "translation"]].sample(n=n_words, replace = True).reset_index(drop=True)
            #Else full test set
            else:
                test_set = test_set[["word", "translation"]].sample(n=test_set.shape[0], replace = True).reset_index(drop=True)
            #Set test_set as global variable
            globals()['test_set'] = test_set
            quiz_input_window()


        if event == "Go back":
            break

    window.close()

# Quiz input window
def quiz_input_window():
    layout =  [[sg.Text('Enter the translation next to each word.')]]
    layout += [[sg.Text(test_set['word'][i]), sg.InputText()] for i in range(test_set.shape[0])]
    layout += [[sg.Button('Submit'), sg.Button('Quit')]]
    window = sg.Window("Quiz", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

        if event == 'Submit':
            quiz_output_window(values)
            break

    window.close()




# Quiz output window
def quiz_output_window(values):
    #Calculate and save score (also change answers from dictionary to list)
    score = 0
    answers = []
    for i in range(test_set.shape[0]):
        answers.append(values[i])
        if values[i].lower() == test_set['translation'][i].lower():
            correct = True
            score += 1
        else:
            correct = False
        current_language.new_attempt(word=test_set['word'][i], success=correct)
    current_language.save_data(current_language_name + '.csv')

    #Setup table
    answers = pd.DataFrame({'answers': answers})
    table = pd.concat([test_set[['word', 'translation']], answers], axis = 1)
    table = table.values.tolist()
    heading = ['Word', 'Translation', 'Answer']

    #Setup window
    layout =  [[sg.Text('Here are your results:')]]
    layout += [[sg.Table(values=table, headings= heading,
                         auto_size_columns=True,
                         display_row_numbers=False,
                         justification='center', key='TABLE',
                         )]]
    layout += [[sg.Text(f'Your score was {score} / {test_set.shape[0]}')]]
    layout += [[sg.Button('Back')]]
    window = sg.Window("Results", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Back':
            break
    window.close()


# Vocabulary Input Window
def add_vocabulary():
    #Layout
    word_input_layout = [
        [sg.Text('Add a new word to the language')],
        [sg.Text('Word:'), sg.InputText(key='word')],
        [sg.Text('Translation:'), sg.InputText(key='translation')],
        [sg.Text('Pronunciation:'), sg.InputText(key='pronunciation')],
        [sg.Text('Example:'), sg.InputText(key='example')],
        [sg.Text('Topic:'), sg.InputText(key='topic')],
        [sg.Text('Part of Speech:'), sg.InputText(key='part of speech')],
        [sg.Button('Add Word'), sg.Button('Cancel'), sg.Button('Done')]
    ]

    window = sg.Window('Add Word', word_input_layout)

    #Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        if event == 'Add Word':
            # Add the new word to the current language
            word = values['word']
            translation = values['translation']
            pronunciation = values['pronunciation']
            example = values['example']
            topic = values['topic']
            pos = values['part of speech']
            current_language.add_word(word, translation, pronunciation, example, topic, pos)

            sg.popup('Word added successfully!')

        if event == 'Done':
            current_language.save_data(current_language_name + '.csv')
            break

    word_input_window.close()



#%% - RUN

startup_window()


#%% - Testing
if 1 == 0:
    Esperanto = vocabulary()
    Esperanto.load_data("Esperanto.csv")
    topics_list = Esperanto.get_topics()
    pos_list = Esperanto.get_pos()
    #print(topics_list)
    print(pos_list)
    Esperanto.reset()
    Esperanto.save_data("Esperanto.csv")