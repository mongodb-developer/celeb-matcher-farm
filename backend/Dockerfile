FROM python:3.12

WORKDIR /usr/src/app
COPY requirements.txt ./
COPY src/ src/

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 3001

CMD [ "python", "./src/server.py" ]