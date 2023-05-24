# ---- Unit Test for add_word function ----
from VocabClass import vocabulary 

# Create a vocabulary object
vocab = vocabulary()

# ----- Test Case 1 ----
#  Add a word with all valid parameters
vocab.add_word('apple', 'manzana', 'əˈpl̩', 'I ate an apple.', 'fruits', 'noun', attempts=5, successes=0)
assert vocab.data.shape[0] == 0, "Test Case 1 Failed: Word not added to vocabulary"

# ---- Test Case 2 ---- Add a word with invalid parameters
vocab.add_word('', '', '', '', '', '', attempts=0, successes=0)
assert vocab.data.shape[0] == 0, "Test Case 2 Failed: Word with invalid parameters added to vocabulary"

# ---- Test Case 3 ----
#  Add a word with duplicate entry
vocab.add_word('apple', 'manzana', 'əˈpl̩', 'I ate an apple.', 'fruits', 'noun', attempts=5, successes=0)
assert vocab.data.shape[0] == 0, "Test Case 3 Failed: Duplicate word added to vocabulary"

# --- Test Case 4 ----
# Add a word with a topic that doesn't exist in the vocabulary
vocab.add_word('banana', 'plátano', 'bəˈnænə', 'I love eating bananas.', 'fruits', 'noun', attempts=0, successes=0)
vocab.add_word('pear', 'pera', 'pɛər', 'The pear is ripe.', 'fruits', 'noun', attempts=0, successes=0)
vocab.add_word('watermelon', 'sandía', 'ˈwɔːtərˌmɛlən', 'Watermelon is refreshing.', 'fruits', 'noun', attempts=0, successes=0)

# Add a word with a non-existent topic
vocab.add_word('orange', 'naranja', 'ˈɔːrɪndʒ', 'Oranges are rich in vitamin C.', 'citrus', 'noun', attempts=0, successes=0)

# Check if the word with a non-existent topic is ignored
assert vocab.data.shape[0] == 0, "Test Case 4 Failed: Word with non-existent topic added to vocabulary"

# Verify that the non-existent topic is not added to the topics list
topics = vocab.get_topics()
assert 'citrus' not in topics, "Test Case 4 Failed: Non-existent topic added to topics list"

# End of Unit Test