FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /library
WORKDIR /library
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean
COPY requirements.txt /library/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /library/