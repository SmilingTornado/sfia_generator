FROM python:3.7.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install gensim==3.8.2
RUN pip install -r requirements.txt
COPY . /code/