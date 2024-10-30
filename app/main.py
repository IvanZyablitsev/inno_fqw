import pickle
import pandas as pd
import gradio as gr
import time

# словари с названиями признаков и соответствующими индексами
education_level_to_index = {
    'Associate' : 0,
    'High School': 1,
    'Bachelor': 2,
    'Master': 3,
    'Doctorate': 4
}

features = dict(
    hoursweek='Занятий в неделю',
    attendance_rate='Посещаемость',
    previous_rades='Предыдущие оценки',
    extracurricular_activities='Участие во внеклассных мероприятиях',
    parent_education_level='Уровень образования родителей'
)

def slowly_reverse(word, progress=gr.Progress()):
    progress(0, desc="Starting")
    time.sleep(1)
    progress(0.05)
    new_string = ""
    for letter in progress.tqdm(word, desc="Reversing"):
        time.sleep(0.25)
        new_string = letter + new_string
    return new_string

# запустить приложения с тремя страницами + установка темы
with gr.Blocks(theme=gr.themes.Glass()) as demo:
    with gr.Tab('Страница 1'):
        gr.Markdown('Это страница ')
        gr.Interface(slowly_reverse, gr.Text(), gr.Text())

    with gr.Tab('Страница 2'):
        gr.Markdown('Это страница 2')

    with gr.Tab('Страница 3'):
        gr.Markdown('Это страница 3')


demo.launch(debug=True)
