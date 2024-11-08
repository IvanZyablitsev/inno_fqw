# Итоговая аттестация

## О работе

Обучение моделей для решения задачи классификации по предсказанию вероятности завершения обучения студентом на основе датасета [souradippal/student-performance-prediction](https://www.kaggle.com/datasets/souradippal/student-performance-prediction). В работе использованы следующие инструменты: [Jupyter Notebook](https://jupyter.org/), фрэймворк [gradio.app](https://www.gradio.app/), [Docker](https://docker.com), python([numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [seaborn](https://seaborn.pydata.org/), [mathplotlib](https://matplotlib.org/), [scikit-learn](https://scikit-learn.org/)).

## Локальное использование - development

`docker compose up -d` - запускает среду Jupyter Notebook (порт 8888) и сервер приложения разработчика из app/main.py (порт 7860)

## Для прода

### Подготовка образа

`make build-push` - для сборки образа. Предварительно авторизоваться на ghcr.io `make login`.

### Запуск - Deploy

Например через ansible. Пример task:

```yalm
- name: Запуск docker-контейнера student_predictor
    docker_container:
    name: student_predictor
    image: ghcr.io/ivanzyablitsev/inno_fqw/student_predictor
    memory: 128M
    memory_swap: 128M
    env:
        GRADIO_SERVER_NAME: '0.0.0.0'
    labels:
        source: https://github.com/IvanZyablitsev/inno_fqw
    comparisons:
        env: strict
    restart_policy: on-failure
    networks:
        - name: llm
    networks_cli_compatible: yes
```
