import pandas as pd
from os import listdir, getcwd
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

current_language = None
current_language_name = None

globals()['current_language_name'] = 'Esperanto'

current_language = Vocabulary()
current_language.load_data(current_language_name + '.csv')
animals = current_language.get_words('nature')
print(animals)