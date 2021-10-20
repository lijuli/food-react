FROM python:3.8.0-slim
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean \
&& mkdir /code
WORKDIR /code
COPY requirements.txt .
ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt
COPY . .
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000
