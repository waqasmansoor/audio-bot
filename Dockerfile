FROM python:3.8-slim-buster

RUN mkdir -p /project
WORKDIR /project

COPY app.py ./app.py
COPY gunicorn.conf.py ./gunicorn.conf.py


COPY static/style.css ./static/style.css
COPY static/app.js ./static/app.js
COPY static/recorder.js ./static/recorder.js
COPY static/images/send.svg ./static/images/send.svg
COPY static/images/type.svg ./static/images/type.svg
COPY static/files ./static/files

COPY templates/index.html ./templates/index.html

COPY openai/openai.py ./openai/openai.py

COPY gcp/credentials/visual-chatbot-464090e61dce.json ./gcp/credentials/visual-chatbot-464090e61dce.json
COPY gcp/gsheet/gsheets.py ./gcp/gsheet/gsheets.py
COPY gcp/audio_text/speech2text.py ./gcp/audio_text/speech2text.py
COPY gcp/audio_text/text2speech.py ./gcp/audio_text/text2speech.py


COPY utils/utils.py ./utils/utils.py
COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y libsndfile1
RUN apt-get install -y libportaudio2
RUN apt-get install -y ffmpeg

CMD ["gunicorn"]

