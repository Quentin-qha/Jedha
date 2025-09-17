FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/data ./data
COPY app/.streamlit ./.streamlit
COPY app/main.py ./main.py

EXPOSE 7860

CMD ["streamlit", "run", "/app/main.py", "--server.port=7860", "--server.address=0.0.0.0"]