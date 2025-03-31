FROM python:3.12

# WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 

COPY src ./src
COPY res/prompts.py ./res

EXPOSE 5000

RUN python -m src.app

CMD ["python", "-m", "src.app"]