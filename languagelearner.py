# Set Up (import modules)
import pandas as pd
from os import listdir, getcwd
import PySimpleGUI as sg

# Define Vocabulary class
class Vocabulary:
    def __init__(self):
        self.data = pd.DataFrame(columns=['word', 'translation', 'pronunciation', 'example', 'category'])

    def add_word(self, word, translation, pronunciation, example, category):
        new_row = {'word': word, 'translation': translation, 'pronunciation': pronunciation, 'example': example, 'category': category}
        self.data = pd.concat([self.data,pd.DataFrame([new_row])], ignore_index=True)

    def get_words(self, category=None):
        if category:
            return self.data[self.data['category'] == category]
            
        else:
            return self.data

    def save_data(self, filename):
        self.data.to_csv(filename, index=False)

    def load_data(self, filename):
        self.data = pd.read_csv(filename)

# Example usage (test case)
    # we dont want to run this every time so nest it in an if statement 
if 1 == 0:
    French = Vocabulary()
    French.add_word('apple', 'pomme', 'æpl', 'I ate an apple for breakfast.', 'fruits')
    French.add_word('book', 'livre', 'bʊk', 'I like to read books in my free time.', 'education')
    French.add_word('cat', 'chat', 'kæt', 'My cat likes to play with string.', 'animals')
    French.save_data('French.csv')
    French.load_data('French.csv')
    French.get_words('fruits')


# Find languages already stored 
path = getcwd()
allfiles = listdir(path)
languages = [filename for filename in allfiles if filename.endswith("csv")]
languages = [filename.replace('.csv', '') for filename in languages]

# Create different menus for the UI

### Start a new language 
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
            globals()[values[0]] = Vocabulary()
            break
    window.close()
    startup_window()

            
            

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
    startup_window.close()

# Run the program
startup_window()
