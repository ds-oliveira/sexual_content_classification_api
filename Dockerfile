FROM python:3.7.4
WORKDIR /app
COPY ./ ./
RUN pip install open-nsfw-python3==0.0.5
RUN pip install uuid==1.30
RUN pip install requests==2.22.0
RUN pip install flask==1.1.1
RUN apt update && apt install caffe-cpu --yes

ENV PYTHONPATH=/usr/lib/python3/dist-packages:
ENV FLASK_APP=app.py

CMD flask run -h 0.0.0.0 -p 80