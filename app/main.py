import pickle
import pandas as pd
import gradio as gr
import time

# словари с названиями признаков и соответствующими индексами
education_level_to_index = {'Associate': 0, 'Bachelor': 1, 'Doctorate': 2, 'High School': 3, 'Master': 4}

features = dict(
    hoursweek='Занятий в неделю',
    attendance_rate='Посещаемость',
    previous_grades='Успеваемость',
    extracurricular_activities='Участие во внеклассных мероприятиях',
    parent_education_level='Образования родителей'
)

# загрузка модели
model_path = 'model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# интерфейс приложения
with gr.Blocks() as demo:
    # приветсвенное сообщение
    # gr.HTML(
    #     """
    #     <div style="text-align: center;">
    #         <h2 style="color: green; font-weight: bold; font-style: italic;">Прогнозирование результата обучения</h2>
    #         <h6>Введите ваши данные и получите результат</h6>
    #     </div>
    #     """
    # )
    with gr.Row():
        # столбец с параметрами (scale между столбцами устанавливаем 1 к 3)
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown('**Данные**')
                hoursweek = gr.Number(minimum=0, maximum=1000, step=0.1, value=10.0, label=features['hoursweek'])
                attendance_rate = gr.Slider(minimum=0, maximum=100, value=85, step=0.1, label=features['attendance_rate'])
                previous_grades = gr.Slider(minimum=0, maximum=100, value=85, step=0.1, label=features['previous_grades'])
                parent_education_level = gr.Radio(education_level_to_index.keys(), value='Associate', label=features['parent_education_level'])
                extracurricular_activities = gr.Checkbox(value=False, label=features['extracurricular_activities'])

        with gr.Column(scale=3):
            gr.Image('main_page_image.jpg', height=460, show_label=False)

            dataframe = gr.DataFrame(
                value=pd.DataFrame(columns=features.values()),  # пустой датафрейм с нашими названиями столбцов
                label='Ваши данные',
                row_count=1,
                column_widths='50%',
                max_height=100,
                # type='pandas',
                )
            textbox = gr.Textbox(label='Результат')

    # для удобства входные параметры о пользователе собираем в список
    all_params = [hoursweek, attendance_rate, previous_grades, extracurricular_activities, parent_education_level]

    # функция для предсказания результата - принимает введенные параметры, и выводит результат вместе с датафреймом параметров
    def predict(*params):
        data_df = pd.DataFrame([dict(zip(features.values(), params))])

        df_to_predict = data_df.copy()
        df_to_predict[features['parent_education_level']] = education_level_to_index[df_to_predict[features['parent_education_level']][0]]

        diabetes_prob = model.predict_proba(df_to_predict.values)[0, 1]
        text_result = f'Вероятность закончить обучение студентом равна: {diabetes_prob:.2f}'

        return data_df, text_result

    # назначить прослушиватель событий - функция predict будет вызываться при изменени (change) любого из компонентов
    gr.on(
        triggers=[param.change for param in all_params],
        fn=predict,
        inputs=[*all_params],
        outputs=[dataframe, textbox],
    )


demo.launch(debug=True)
