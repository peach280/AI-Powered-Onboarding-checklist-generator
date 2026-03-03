FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
CMD ["gunicorn","--bind","0.0.0.0:7860","app:app"]