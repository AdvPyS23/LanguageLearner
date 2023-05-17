# Set Up (import modules)
import pandas as pd
from os import listdir, getcwd
import PySimpleGUI as sg

# Define vocabulary class
class vocabulary:
    def __init__(self):
        self.data = pd.DataFrame(columns=['word', 'translation', 'pronunciation', 'example', 'topic', 'part of speech','attempts','successes'])

    def add_word(self, word, translation, pronunciation, example, topic, pos, attempts = 0, successes = 0):
        new_row = {'word': word, 'translation': translation, 'pronunciation': pronunciation, 'example': example, 'topic': topic, 'part of speech': pos, 'attempts': attempts, 'successes': successes}
        self.data = pd.concat([self.data,pd.DataFrame([new_row])], ignore_index=True)
    
    # functions for quiz attempts
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
    
# functions to retrieve words based on different identifiers
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
        
    #NB. this function takes a float (between 0.0 and 1.0) and returns words with a successes score below that threshold.
    # successes scores will be set as a percentage of correct attempts in quizes 1 = 100%, 0 = 0% etc.
    def get_words_familiar(self, familiar=None):
        if familiar:
            return self.data[self.data['successes'] <= familiar]       
        else:
            return self.data

    def save_data(self, filename):
        self.data.to_csv(filename, index=False)

    def load_data(self, filename):
        self.data = pd.read_csv(filename)

# Example usage (test case)
    # we dont want to run this every time so nest it in an if statement 
if 1 == 0:
    French = vocabulary()
    French.add_word('apple', 'une pomme', 'æpl', 'I ate an apple for breakfast.', 'fruits','noun')
    French.add_word('book', 'un livre', 'bʊk', 'I like to read books in my free time.', 'education','noun')
    French.add_word('cat', 'un chat', 'kæt', 'My cat likes to play with string.', 'animals','noun')
    French.save_data('French.csv')
    French.load_data('French.csv')
    French.get_words('fruits')


# Find languages already stored 
path = getcwd()
allfiles = listdir(path)
languages = [filename for filename in allfiles if filename.endswith("csv")]
languages = [filename.replace('.csv', '') for filename in languages]

#------------- Create different menus for the UI ---------------
# NB. when creating windows, the 'first' to appear to the user should be the last defined in the code and vice versa.
## since a home menu will need to call on the functions defined for its sub menus, etc. 

# # Start a new language 
def start_newlanguage():
    layout = [ 
        [sg.Text('Enter the name of the language',justification='center')],
        [sg.Input(justification='center')],
        [sg.Button('Enter'),sg.Button('Cancel')]]
    window = sg.Window("Start a new language",layout)
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

## Quiz stuff

def quiz_menu():

    layout = [
        [sg.Text(f"What would you like to test today?",justification='center')],
        [sg.Button('At random'),sg.Button('By Topic')],
        [sg.Button('By familiarity'),sg.Button('By part of speech')],
        [sg.Button('Go back')]]
    window = sg.Window(current_language_name + "quiz",layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'At random':
            test_set = current_language.get_words_topic(topic = None)
            test_set = test_set[["word","translation"]].sample(n=10, replace = True).reset_index(drop=True)
            globals()['test_set'] = test_set
            quiz_input_window()
            break
        
    window.close()

def quiz_input_window():
    layout =  [[sg.Text('Enter the translation next to each word.')] ]
    layout += [[sg.Text(test_set['word'][i]), sg.InputText()] for i in range(10)]
    layout += [[sg.Button('Submit'), sg.Button('Quit')]]
    window = sg.Window("Quiz", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Submit':
            score = 0
            for i in range(10):
                if values[i].lower() == test_set['translation'][i].lower():
                    correct = True
                    score += 1
                else:
                    correct = False
                current_language.new_attempt(word = test_set['word'][i], success = correct)
            current_language.save_data(current_language_name + '.csv')
            print(f"Your score is: {score}/10")



    window.close()

    # other stuff
def language_home():
    layout = [
        [sg.Text(f"Let's get ready to learn some {current_language_name}!",justification='center')],
        [sg.Button('Input'),sg.Button('Quiz')],
        [sg.Button('View Progress'),sg.Button('Go Back')]]
    window = sg.Window(current_language_name,layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Go Back':
            startup_window()
            break
        if event == 'Input':
            add_vocabulary()
            break
        if event == 'Quiz':
            quiz_menu()
            break
    window.close()
            
            
# Startup Window
def startup_window():

    startup_layout = [  [sg.Text('Welcome! Select the language you want to practice, or start a new one :)')],
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
            break
        if event != 'New Language...' and event != 'Quit':
            globals()['current_language_name'] = event 
            globals()['current_language'] = vocabulary()
            current_language.load_data(current_language_name + '.csv')
            language_home()
            break
    startup_window.close()

# Add vocabulary 

# Define the layout for the word input window
def add_vocabulary():
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

    # Create the word input window
    word_input_window = sg.Window('Add Word', word_input_layout)

    # Event loop to process "Add Word" and "Cancel" button clicks
    while True:
        event, values = word_input_window.read()
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
            current_language.add_word(word,translation,pronunciation,example,topic,pos)

            sg.popup('Word added successfully!')
        if event == 'Done':
            current_language.save_data(current_language_name + '.csv')
            break

    # Close the word input window
    word_input_window.close()

# Run the program
startup_window()


# testing arena
if 1 == 0:
    Esperanto = vocabulary()
    Esperanto.load_data("Esperanto.csv")
    pos_list = Esperanto.get_pos()
    print(pos_list)
