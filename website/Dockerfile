FROM python:3.12

COPY requirements.txt .

RUN pip install -r requirements.txt --upgrade

EXPOSE 8000

COPY src src

CMD ["python", "src/app.py"]