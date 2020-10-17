FROM python:3.8

#RUN apt update \
#        && apt install -y build-essential \
#        && pip install --no-cache-dir uWSGI==2.0.15 \
#        && apt remove -y build-essential

RUN pip install --no-cache-dir uWSGI==2.0.18


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/

USER nobody
EXPOSE 5000
ENV PYTHONPATH /usr/src/app
ENV FLASK_APP impala

CMD ["uwsgi", "--master", "--http", ":5000", "--processes", "4", "--harakiri", "90", "--module", "impala", "--callable", "app"]
