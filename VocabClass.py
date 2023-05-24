# import modules
import pandas as pd
import numpy as np

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

    def get_topics(self):
        topics = list(self.data['topic'].unique())
        return(topics)

    def get_pos(self):
        pos = list(self.data['part of speech'].unique())
        return(pos)

    def familiarities(self):
        familiarities = self.data['successes'] / self.data['attempts']
        familiarities = familiarities.replace(np.NaN, 0)
        return(familiarities)

    def get_familiarity(self, word):
        row = self.data['word'].str.match(word)
        familiarities = self.familiarities()
        familiarity = familiarities[row]
        return(familiarity)

    def completed(self):
        familiarities = self.familiarities()
        completed_words = pd.DataFrame(columns = self.data.columns)
        for i in range(self.data.shape[0]):
            if self.data['attempts'][i] >= 10 and familiarities[i] >= 0.8:
                completed_words.append(self.data.loc[i])
        return(completed_words)




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

    def get_words_familiar(self, lower = 0, upper = 1):
        fam_col = self.familiarities()
        #Takes float as percentage of correct attempts and threshold filters vocabulary
        return(pd.merge(self.data[fam_col >= lower], self.data[fam_col <= upper]))
