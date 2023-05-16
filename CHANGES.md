### Abstraction

- We decided to separate our app into sets of vocabularies for each language. 
To do this, we created a class "Vocabulary" that contains the dataframe with all
the relevant translations etc...

- It is within these vocabulary classes that we define functions relating to the 
manipulation of the dataframe, e.g. adding new words, saving into .csv-file, etc..

- The second relevant module of our app deals with the GUI for learning.

### Decomposition
- Seperated dataframe manipulation functions into many subfunctions.
  - e.g. addword(), get_word_pos(), add_attempt(), etc...
- Each window of the GUI is also separated into its own function. 

Because we are quite happy with the overall structure of the code, it has
not been necessary yet to make any drastic changes. We do aim and try to keep
the code organised throughout the project with the use of decomposition and abstraction. 