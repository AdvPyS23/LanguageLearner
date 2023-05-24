# -------------------------------------------------
# Quinn Alexander Coxon & Santiago Marin Martinez
# Language Learner App
# Advanced Python FS2023
# -------------------------------------------------

#%% - Setup

# Import Libraries
import numpy as np
import pandas as pd
from os import listdir, getcwd
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tk
from VocabClass import vocabulary 

# Canvas Setup
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 100



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
        [sg.Button('Input'), sg.Button('Quiz')],
        [sg.Button('View Progress'), sg.Button('Go Back')]]
    window = sg.Window(current_language_name,layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Go Back':
            break

        if event == 'Input':
            add_vocabulary()

        if event == 'Quiz':
            quiz_menu()

        if event == 'View Progress':
            progress_menu()

    window.close()


# Quizzes setup
def quiz_menu():
    topics_list = current_language.get_topics()
    pos_list = current_language.get_pos()
    dif_list = ['Easy', 'Medium', 'Hard']

    layout = [
            [sg.Text(f'Setup your quiz - Leave empty for random', justification='center')],
            [sg.Text(f'Number of words'), sg.Input(key='n_words')],
            [sg.Text('By topic:'), sg.DropDown(topics_list, key='topic_dropdown')],
            [sg.Text('By part of speech:'), sg.DropDown(pos_list, key='pos_dropdown')],
            [sg.Text('By difficulty:'), sg.DropDown(dif_list, key = 'dif_dropdown')],
            [sg.Button("Let's go!"), sg.Button('Go back')]]
    window = sg.Window(current_language_name + "Quiz", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "Let's go!":
            #Topic and POS setting
            test_set = current_language.get_words_topic(topic = values['topic_dropdown'])
            test_set = pd.merge(test_set,current_language.get_words_pos(pos = values['pos_dropdown']))

            #Difficulty setting
            if values['dif_dropdown']:
                if values['dif_dropdown'] == 'Easy':
                    lower = 0.7
                    upper = 1
                if values['dif_dropdown'] == 'Medium':
                    lower = 0.4
                    upper = 0.7
                if values['dif_dropdown'] == 'Hard':
                    lower = 0
                    upper = 0.4
                test_set = pd.merge(test_set, current_language.get_words_familiar(lower, upper))
            if test_set.shape[0] == 0:
                sg.popup('No vocabulary available with these settings. Please change the values in the quiz setup page.')
                window.close()
                quiz_menu()

            #Number of words setting
            if values['n_words']:
                # Use try statement to makesure input number of words is interpretable as an integer 
                try:
                    n_words = int(values['n_words'])
                except:
                    sg.popup("Only digits for 'Number of words' allowed")
                    window.close()
                    quiz_menu()
            else:
                n_words = 10
            #Check that it is smaller than full test set
            if n_words <= test_set.shape[0]:
                test_set = test_set[["word", "translation"]].sample(n=n_words, replace = False).reset_index(drop=True)
            else:
                test_set = test_set[["word", "translation"]].sample(n=test_set.shape[0], replace = False).reset_index(drop=True)

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


# Progress window layout
def progress_layout(data_set, event):
    #Save data_set into temporary language
    temp_lang = vocabulary()
    temp_lang.data = data_set

    #Use functions to retrieve relevant data
    fam_list = temp_lang.familiarities()
    com_list = temp_lang.completed()

    #Reset matplotlib canvas
    plt.clf()
    fig = plt.figure(1)

    #Plot histogram using data_set
    fig.add_subplot(111).hist(fam_list, bins=10, range=(0,1), density = True)
    plt.xlabel('Familiarity [as float percentage]')
    plt.ylabel('Density [as float percentage]')
    plt.title(f'{event} Histogram in {current_language_name}')

    #Layout for progress window
    layout = [
        [sg.Menu(prog_menu)],
        [sg.Canvas(key='Canvas')],
        [sg.Text(f'Total number of attempts: {sum(temp_lang.data["attempts"])}'),
         sg.Text(f'Total number of successes: {sum(temp_lang.data["successes"])}')],
        [sg.Text(f'Average familiarity: {sum(fam_list) / len(fam_list):.2%}'),
         sg.Text(f'Median familiarity: {fam_list.median()}')],
        [sg.Text(f'Number of completed: {len(com_list)}'),
         sg.Text(f'Percentage of completed: {len(com_list) / len(fam_list):.2%}')],
        [sg.Text(f'Words count as completed when a word has more than 80% familiarity on 10 or more attempts.')],
        [sg.Button('Back')]
    ]

    #Draw window and return
    window = sg.Window('Progress', layout, finalize=True)
    fig_canvas_agg = draw_figure(window['Canvas'].TKCanvas, fig)
    return(window)


# Progress window setup and event loop
def progress_menu():
    #Get full language data
    topics_list = current_language.get_topics()
    pos_list = current_language.get_pos()
    fam_list = current_language.familiarities()
    com_list = current_language.completed()

    #Setup Menubar
    globals()['prog_menu'] = [
        ['All',['Global']],
        ['Topic',topics_list],
        ['Part of Speech',pos_list],
    ]

    #Use progress_layout function to draw initial window
    window = progress_layout(current_language.data, 'Global')

    #Event loop changes window according to event
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Back':
            break
        else:
            if event in topics_list:
                data_set = current_language.get_words_topic(topic = event).reset_index()
            if event in pos_list:
                data_set = current_language.get_words_pos(pos = event).reset_index()
            if event == 'Global':
                data_set = current_language.data
            window.close()
            window = progress_layout(data_set, event)

    window.close()


# Figure function for histograms
def draw_figure(canvas, figure):
   figure_canvas_agg = tk.FigureCanvasTkAgg(figure, canvas)
   figure_canvas_agg.draw()
   figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
   return figure_canvas_agg



#%% - RUN
Esperanto = vocabulary()
Esperanto.load_data("Esperanto.csv")

startup_window()
