FROM quay.io/jupyter/scipy-notebook:latest as learning

USER root

COPY requirements.txt /tmp/requirements.txt
COPY requirements_jupyter.txt /tmp/requirements_jupyter.txt
RUN cat /tmp/requirements_jupyter.txt >> /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
ADD scraping/scraping.ipynb scraping.ipynb

RUN ipython scraping.ipynb


FROM python:3.10-slim

LABEL org.opencontainers.image.source=https://github.com/IvanZyablitsev/inno_fqw
LABEL org.opencontainers.image.description="Прогностическая модель предсказания окончания студентом обучения."
LABEL org.opencontainers.image.licenses=MIT

COPY requirements.txt /tmp/requirements.txt
RUN echo "gradio" >> /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /usr/src/app
COPY app/* /usr/src/app/
COPY --from=learning /app/model.pkl /usr/src/app/model.pkl
COPY --from=learning /app/report.html /usr/src/app/report.html

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
CMD ["python", "main.py"]
