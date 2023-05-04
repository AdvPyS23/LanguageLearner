import pandas as pd

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

# Example usage
vocabulary = Vocabulary()
vocabulary.add_word('apple', 'pomme', 'æpl', 'I ate an apple for breakfast.', 'fruits')
vocabulary.add_word('book', 'livre', 'bʊk', 'I like to read books in my free time.', 'education')
vocabulary.add_word('cat', 'chat', 'kæt', 'My cat likes to play with string.', 'animals')
vocabulary.save_data('vocabulary.csv')
vocabulary.load_data('vocabulary.csv')
vocabulary.get_words('fruits')

# Now This has an extra line 

