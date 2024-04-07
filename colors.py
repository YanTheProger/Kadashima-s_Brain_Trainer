#!/usr/bin/python3
#
#
#
#

TASKS_COUNT = 12
TASKS_VARIANTS = (
    ("красный", "red"),
    ("жёлтый", "yellow"),
    ("зелёный", "green"),
    ("синий", "blue")
    )
TASK_WORD_MAX_LENGTH = 7
INSTRUCTION = "Указывайте щелчком мыши по кнопкам цвет слов, делая это как можно быстрее. Будьте внимательны: вы должны указывать не слова, а их цвет. Если ошибётесь, выберите цвет ещё раз."


import tkinter as tk
from tkinter import messagebox
import random as rnd
import time

rights = 0 # количество правильно решенных примеров
wrongs = 0 # количество НЕправильно решенных примеров


def check(pattern):
    # msg = '<<' + lbl_question_color + '>> <<' + pattern + '>>'
    # messagebox.showinfo('', msg)
    global rights
    if rights <= TASKS_COUNT:
        if lbl_question_color == pattern:
            rights += 1
            update_status()
            next_task()
        else:
            global wrongs
            wrongs += 1
            update_status()

def check_red():
    check('red')

def check_yellow():
    check('yellow')

def check_green():
    check('green')

def check_blue():
    check('blue')


def update_status():
    status = ' Правильных: ' + str(rights).strip()
    status += ' /// Ошибок: ' + str(wrongs).strip()
    status += ' /// Время ' + str(int(time.time() - time_start)).strip() + ' сек. '
    if rights >= TASKS_COUNT:
        status += '\n Задание Выполнено! '
    lbl_status_bar['text'] = status


def next_task():
    global lbl_question_color
    #rights += 1
    if rights < TASKS_COUNT:
        color1 = rnd.choice(TASKS_VARIANTS)
        lbl_question['text'] = color1[0]
        color2 = rnd.choice(TASKS_VARIANTS)
        lbl_question['fg'] = color2[1]
        lbl_question_color = color2[1]


window = tk.Tk()
window.geometry('800x600')
window.resizable(width=False, height=False)
window.title('Тренажёр мозга - Цвета - тест Струпа')
window['bg'] = 'white'

lbl_question = tk.Label(
    master=window, font=("Arial Bold", 36), fg='black', bg='white',
    text='', width=TASK_WORD_MAX_LENGTH)
lbl_question.pack()
lbl_question_color = ''
lbl_instruction = tk.Label(
    master=window, font=("Arial Bold", 14, "italic"), fg='black', bg='white',
    text=INSTRUCTION, wraplength=780)
lbl_instruction.pack()

frm_answers = tk.Frame(master=window, bg='white')
frm_answers.pack()
'''
for color in TASKS_VARIANTS:
    btn = tk.Button(
        master=frm_answers, font=("Arial Bold", 14), fg='black', bg='white',
        text=color[0], command=lambda:check(color[1])
        )
    btn.pack(side=tk.LEFT)
'''
btn_red = tk.Button(
    master=frm_answers, font=("Arial Bold", 14), fg='black', bg='white',
    text='красный', command=check_red)
btn_red.pack(side=tk.LEFT)
btn_yellow = tk.Button(
    master=frm_answers, font=("Arial Bold", 14), fg='black', bg='white',
    text='жёлтый', command=check_yellow)
btn_yellow.pack(side=tk.LEFT)
btn_green = tk.Button(
    master=frm_answers, font=("Arial Bold", 14), fg='black', bg='white',
    text='зелёный', command=check_green)
btn_green.pack(side=tk.LEFT)
btn_blue = tk.Button(
    master=frm_answers, font=("Arial Bold", 14), fg='black', bg='white',
    text='синий', command=check_blue)
btn_blue.pack(side=tk.LEFT)

lbl_status_bar = tk.Label(
    master=window, font=("Arial Bold", 14), fg='black', bg='lightgrey',
    text='строка состояния'
    )
lbl_status_bar.pack()

time_start = time.time()
next_task()
window.mainloop()
