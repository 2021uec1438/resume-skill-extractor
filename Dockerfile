FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py extractor.py ./

EXPOSE 8522
CMD ["streamlit", "run", "app.py", "--server.port=8522", "--server.address=0.0.0.0"]
