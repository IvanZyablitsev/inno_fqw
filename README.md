# Выпускная квалификационная работа

## О работе

Обучение моделей для решения задачи классификации по предсказанию вероятности завершения обучения студентом на основе датасета [souradippal/student-performance-prediction](https://www.kaggle.com/datasets/souradippal/student-performance-prediction). В работе использованы следующие инструменты: Jupyter Notebook, фрэймворк [gradio.app](https://www.gradio.app/), [Docker](docker.com), python. Работа предполает работу data science специалиста, разработчика приложения, а также ci/cd pipeline процесс сборки окружения для деплоя на прод.

## Локальное использование - development

`docker compose up` - запускает среду Jupyter Notebook (порт 8888) и сервер приложения разработчика из app/main.py (порт 7860)

## Для прода

### Подготовка через Ci/CD

`.gitlab-ci` - для gitlab ci с загрузкой образа в register.

### Запуск на проде

Например через ansible. Пример task:

```yalm
- name: Запуск docker-контейнера gradio.app
    docker_container:
    name: gradio_app
    image: register.zyablitsev.ru/docker/gradioapp:latest
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
