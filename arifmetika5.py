#!/usr/bin/python3
#
#
#
#

import tkinter as tk
from tkinter import scrolledtext
import random as rnd
import time

COUNT_OF_EVERY_OPERATION = 100 // 4
INSERT_BLANKS = False
MAX_LENGTH_OF_QUESTION = 4
MAX_LENGTH_OF_ANSWER_MAIN = 3
MAX_LENGTH_OF_MODULO = 1

answer = '' # контрольное значение ответа на задачу
modulo = '1' # контрольное значение остатка от деления в ответе на задачу.
# при непустом (и ненулевом) значении - фрейм остатка виден, иначе скрыт
done = True # флаг, что выполнение продолжается

rights = 0 # количество правильно решенных примеров
wrongs = 0 # количество НЕправильно решенных примеров


class Tasks():
    ''' '''
    def __init__(self):
        self.operators_queue = []
        for i in range(COUNT_OF_EVERY_OPERATION):
            self.operators_queue.append('+')
            self.operators_queue.append('-')
            self.operators_queue.append('*')
            self.operators_queue.append('/')
        rnd.shuffle(self.operators_queue)
        rnd.shuffle(self.operators_queue)
        rnd.shuffle(self.operators_queue)
        self.num_pairs_queue = []
        while len(self.num_pairs_queue) < len(self.operators_queue):
            for a in range(10):
                for b in range(10):
                    pair = (a, b)
                    self.num_pairs_queue.append(pair)
        rnd.shuffle(self.num_pairs_queue)
        rnd.shuffle(self.num_pairs_queue)
        rnd.shuffle(self.num_pairs_queue)

    def generate_task(self):
        if len(self.operators_queue) < 1:
            return None
        operator = self.operators_queue.pop(0)
        (first, second) = self.num_pairs_queue.pop(0)
        if operator == '+':
            result = first + second
            modulo = 0
        elif operator == '-':
            result = first
            first = result + second
            modulo = 0            
        elif operator == '*':
            result = first * second
            modulo = 0
        elif operator == '/':
            result = first
            if second == 0:
                modulo = 0
                second = rnd.randrange(1, 10)
            elif second > 1:
                modulo = rnd.randrange(1, second)
            else:
                modulo = 0
            first = (result * second) + modulo
        else:
            return None

        if INSERT_BLANKS:
            question = str(first).strip() + ' ' + operator + ' ' +  str(second).strip()
        else:
            question = str(first).strip() + operator + str(second).strip()
        answer = str(result).strip()
        if modulo > 0:
            modulo = str(modulo).strip()

        return (question, answer, modulo)


tsk = Tasks()

window = tk.Tk()
window.geometry('800x600')
window.resizable(width=False, height=False)
window.title('Тренажёр мозга - Арифметика')
window['bg'] = 'white'
mainframe = tk.Frame(master=window) # , font="20", bg='white', fg='black')
mainframe.pack()
lbl_question = tk.Label(
    master=mainframe, font=("Arial Bold", 36), fg='black', bg='white',
    text='', width=MAX_LENGTH_OF_QUESTION)
lbl_question.pack(side=tk.LEFT)
lbl_eq = tk.Label(
    master=mainframe,
    font=("Arial Bold", 36), fg='black', bg='white',
    text='=')
lbl_eq.pack(side=tk.LEFT)
ent_answer_main = tk.Entry(
    master=mainframe,
    font=("Arial Bold", 36), fg='black', bg='white',
    width=MAX_LENGTH_OF_ANSWER_MAIN)
ent_answer_main.pack(side=tk.LEFT)
frm_answer_modulo = tk.Frame(master=mainframe)
frm_answer_modulo.pack(side=tk.LEFT)
lbl_mod = tk.Label(
    master=frm_answer_modulo,
    font=("Arial Bold", 36), fg='black', bg='white',
    text='ост.')
lbl_mod.pack(side=tk.LEFT)
ent_answer_modulo = tk.Entry(
    master=frm_answer_modulo,
    font=("Arial Bold", 36), fg='black', bg='white',
    width=MAX_LENGTH_OF_MODULO)
ent_answer_modulo.pack(side=tk.LEFT)
lbl_status_bar = tk.Label(
    master=window,
    font=("Arial Bold", 20),
    text='строка состояния',
    bg='light grey')
lbl_status_bar.pack()
txt_errors = scrolledtext.ScrolledText(
    master=window,
    font=("Arial Bold", 20),
    bg='light grey',
    fg='red')
txt_errors.pack()


def filter_digits(s):
    'Эта функция удаляет из строки все нецифровые символы'
    result = ''
    if len(s) > 0:
        for ch in s:
            if ch in '0123456789':
                result += ch
    return result


def error_message(ans, mdl):
    s = lbl_question['text'] + ' НЕ ' + ans
    if mdl:
        s += 'ост' + mdl
    txt_errors.insert(tk.END, s + '\n')


def check_answer():
    ans = ent_answer_main.get()
    ans = filter_digits(ans.strip())
    if modulo:
        mdl = ent_answer_modulo.get()
        mdl = filter_digits(mdl.strip())
    else:
        mdl = ''
    if answer.strip() == ans:
        if modulo:
            if modulo.strip() == mdl:
                return True
            else:
                error_message(ans, mdl)
                return False
        else:
            return True
    else:
        error_message(ans, mdl)
        return False


def process_answer():
    global rights, wrongs
    if check_answer():
        rights += 1
    else:
        wrongs += 1
    status = ' Решено ' + str(rights).strip() + ' : ' + str(wrongs).strip()
    status += ' /// Время ' + str(int(time.time() - time_start)).strip() + ' сек. '
    lbl_status_bar['text'] = status


def start_task():
    ''' '''
    current_task = tsk.generate_task()
    if current_task:
        lbl_question['text'] = current_task[0]
        ent_answer_main.delete(0, tk.END)
        ent_answer_main.focus_set()
        global answer, modulo
        flag = modulo
        # временно сохраняем старое значение "остатка от деления", чтобы
        # решить, нужно ли менять видимость фрейма остатка
        answer = current_task[1]
        modulo = current_task[2]
        if modulo:
            ent_answer_modulo.delete(0, tk.END)
            if not flag:
                frm_answer_modulo.pack()
        elif flag:
            frm_answer_modulo.pack_forget()
    else: # UNDER CONSTRUCTION !!!
        window.title('Готово!')
        global done
        done = False


def next_task():
    if done:
        process_answer()
        start_task()
    else:
        pass


def handle_key_return_answer_main(event):
    # только если в поле ответа введено непустое значение
    if len(filter_digits(ent_answer_main.get().strip())) > 0:
        if modulo:
            ent_answer_modulo.focus_set()
        else:
            next_task() # global_check_answer() # main.check_answer()
    else:
        pass


def handle_key_return_answer_modulo(event):
    # только если в поле ответа введено непустое значение
    if len(filter_digits(ent_answer_modulo.get().strip())) > 0:
        next_task() # global_check_answer() # main.check_answer()


ent_answer_main.bind("<Key-Return>", handle_key_return_answer_main)
ent_answer_main.bind("<Key-Tab>", handle_key_return_answer_main)
ent_answer_modulo.bind("<Key-Return>", handle_key_return_answer_modulo)
start_task()

time_start = time.time()
window.mainloop()

