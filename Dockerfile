FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir \
    "flask>=3.1" \
    "flask-socketio>=5.3" \
    "gunicorn>=23" \
    "numpy>=2.3" \
    "psycopg[binary]>=3.2"

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
