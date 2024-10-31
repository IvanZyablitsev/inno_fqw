import pickle
import pandas as pd
import gradio as gr
import time

# словари с названиями признаков и соответствующими индексами
education_level_to_index = {'Associate': 0, 'Bachelor': 1, 'Doctorate': 2, 'High School': 3, 'Master': 4}

features = dict(
    hoursweek='Занятий в неделю',
    attendance_rate='Посещаемость',
    previous_grades='Предыдущие оценки',
    extracurricular_activities='Участие во внеклассных мероприятиях',
    parent_education_level='Уровень образования родителей'
)

# загрузка модели
model_path = 'model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# интерфейс приложения
with gr.Blocks() as demo:
    # приветсвенное сообщение
    gr.HTML(
        """
        <div style="text-align: center;">
            <h2 style="color: green; font-weight: bold; font-style: italic;">Прогнозирование результата обучения</h2>
            <h6>Введите ваши данные и получите результат</h6>
        </div>
        """
    )
    # строка в которой будут два столбца - 1) параметры ввода 2) картинка, датафрейм с введенными данными и результаты
    with gr.Row():
        # столбец с параметрами (scale между столбцами устанавливаем 1 к 3)
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown('**Данные**')
                # элементы параметров ввода данных пользователя (компоненты Gradio)
                hoursweek = gr.Number(minimum=0, maximum=1000, step=0.1, value=10.0, label=features['hoursweek'])
                with gr.Row():
                    extracurricular_activities = gr.Checkbox(value=False, label=features['extracurricular_activities'])
                parent_education_level = gr.Radio(education_level_to_index.keys(), value='Нет информации', label=features['parent_education_level'])
                attendance_rate = gr.Slider(minimum=0, maximum=100, value=85, step=1, label=features['attendance_rate'])
                previous_rades = gr.Slider(minimum=0, maximum=100, value=85, step=1, label=features['previous_rades'])

        # столбец с картинкой, датафреймом с введенными данными и результатом
        with gr.Column(scale=3):
            # отобразить картинку через через gr.Image()
            gr.Image('main_page_image.jpg', height=460, show_label=False)
            # датафрейм для отображения введенных данных
            dataframe = gr.DataFrame(
                value=pd.DataFrame(columns=features.values()),  # пустой датафрейм с нашими названиями столбцов
                label='Ваши данные',
                row_count=1,
                column_widths='50%',
                max_height=100,
                # type='pandas',
                )
            # текстовое поле для результата
            textbox = gr.Textbox(label='Результат')

    # для удобства входные параметры о пользователе собираем в список
    all_params = [hoursweek, extracurricular_activities, attendance_rate, previous_rades, parent_education_level]

    # функция для предсказания результата - принимает введенные параметры, и выводит результат вместе с датафреймом параметров
    def predict(*params):
        # датафрейм параметров для отображения
        data_df = pd.DataFrame([dict(zip(features.values(), params))])

        # преобразовать все столбцы датафрейма к числам перед предиктом
        df_to_predict = data_df.copy()
        df_to_predict['Уровень образования родителей'] = education_level_to_index[df_to_predict['Уровень образования родителей'][0]]

        # сделать предсказание моделью - вероятность диабета
        diabetes_prob = model.predict_proba(df_to_predict.values)[0, 1]
        text_result = f'Вероятность закончить обучение студентом равна: {diabetes_prob:.2f}'
        # вернуть датафрейм с параметрами и результат - вероятность диабета
        return data_df, text_result

    # назначить прослушиватель событий - функция predict будет вызывыатся при изменени (change) любого из компонентов
    gr.on(
        triggers=[param.change for param in all_params],
        fn=predict,
        inputs=[*all_params],
        outputs=[dataframe, textbox],
    )


demo.launch(debug=True)
