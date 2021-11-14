BACKGROUND_COLOR = "#B1DDC6"

import pandas
from tkinter import messagebox
from tkinter import *
import random
import os


try:
    df = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    df = pandas.read_csv("data/french_words.csv")
dict_words = df.to_dict(orient='records')
english_text = ''
french_text = ''
current_card = {}

def random_flashcard():
    #print(french_text,english_text)
    global title, win_timer, word, english_text,french_text,current_card
    window.after_cancel(win_timer)
    current_card = random.choice(dict_words)
    french_text = current_card["French"]
    english_text = current_card['English']
    canvas.itemconfig(canvas_image, image=img)
    canvas.itemconfig(title,text='French',  fill='black')
    canvas.itemconfig(word, text=french_text,  fill='black')
    win_timer = window.after(3000, display_change, english_text)

def display_change(english_text):
    canvas.itemconfig(title,text='English', fill='white')
    canvas.itemconfig(word, text=english_text, fill='white')
    canvas.itemconfig(canvas_image,image=card_back_img)

def remove_card():
    global current_card
    dict_words.remove(current_card)
    df1 = pandas.DataFrame.from_records(dict_words)
    df1.to_csv('words_to_learn.csv', index=False)
    try:
        random_flashcard()
    except IndexError:
        try:
            os.remove('words_to_learn.csv')
            messagebox.showinfo(title="Pop-up",message="You have completed the list,\n please restart the app to reset the words")
            exit()
        except OSError:
            pass


window = Tk()

window.title("Flash Card App - French")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)
win_timer = window.after(3000, display_change, english_text)

canvas = Canvas(height=526,width=800,highlightthickness=0)
img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400,263,image=img)
title = canvas.create_text(400,150,text='Title',font=("Ariel",40,"italic"))
word = canvas.create_text(400,263,text='word',font=("Ariel",50,"bold"))
canvas.grid(row=0,column=0, columnspan=2, rowspan=2)
canvas.config(bg=BACKGROUND_COLOR)

my_image_right = PhotoImage(file="images/right.png")
button_right = Button(image=my_image_right, highlightthickness=0,command=remove_card)
button_right.config( height = 50, width = 50 )
button_right.grid(row=2,column=0)

my_image_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=my_image_wrong, highlightthickness=0,command=random_flashcard)
button_wrong.config( height = 50, width = 50 )
button_wrong.grid(row=2,column=1)

random_flashcard()

window.mainloop()
