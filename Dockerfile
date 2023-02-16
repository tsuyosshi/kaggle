FROM python:3

ENV PROJECT_DIR kaggle
WORKDIR /${PROJECT_DIR}

RUN pip install --upgrade pip && \
    pip install fastprogress japanize-matplotlib

RUN pip install pipenv
COPY src/ /${PROJECT_DIR}/src/
RUN pip install -r /${PROJECT_DIR}/src/requirements.txt
RUN mkdir /root/.kaggle
COPY src/kaggle.json /root/.kaggle/
RUN chmod 600 /root/.kaggle/kaggle.json

