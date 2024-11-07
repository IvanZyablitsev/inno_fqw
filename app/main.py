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
    parent_education_level='Уровень образования родителей'
)

# загрузка модели
model_path = 'model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# описание интерфейса приложения
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown('  **Данные**')
                hoursweek = gr.Number(minimum=0, maximum=200, step=0.1, value=14.0, label=features['hoursweek'])
                attendance_rate = gr.Slider(minimum=0, maximum=100, value=65, step=0.1, label=features['attendance_rate'])
                previous_grades = gr.Slider(minimum=0, maximum=100, value=78, step=0.1, label=features['previous_grades'])
                extracurricular_activities = gr.Checkbox(value=False, label=features['extracurricular_activities'])
                parent_education_level = gr.Radio(education_level_to_index.keys(), value='Associate', label=features['parent_education_level'])

        with gr.Column(scale=3):
            gr.Image('main_page_image.jpg', height=440, show_label=False)

            dataframe = gr.DataFrame(
                value=pd.DataFrame(columns=features.values()),
                label='Ваши данные',
                row_count=1,
                column_widths='75%',
                max_height=100,
                # type='pandas'
                )
            textbox = gr.Textbox(label='Результат')

    all_params = [hoursweek, attendance_rate, previous_grades, extracurricular_activities, parent_education_level]

    def predict(*params):
        data_df = pd.DataFrame([dict(zip(features.values(), params))])

        df_to_predict = data_df.copy()
        df_to_predict[features['parent_education_level']] = education_level_to_index[df_to_predict[features['parent_education_level']][0]]

        diabetes_prob = model.predict_proba(df_to_predict.values)[0, 1]
        text_result = f'Вероятность закончить обучение студентом равна: {diabetes_prob:.2f}'

        return data_df, text_result

    gr.on(
        triggers=[param.change for param in all_params],
        fn=predict,
        inputs=[*all_params],
        outputs=[dataframe, textbox],
    )


demo.launch(debug=True)
