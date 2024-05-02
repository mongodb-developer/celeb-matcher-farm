FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD [ "python", "./src/server.py" ]