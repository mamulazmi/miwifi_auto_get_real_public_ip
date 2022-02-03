FROM python:3.9-alpine3.14

WORKDIR /app

COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

CMD [ "python", "./main.py", "start"]