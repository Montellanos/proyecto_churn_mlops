FROM python:3.14.5-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python src/preparar_datos.py && \
    python src/entrenar_modelo.py && \
    python src/evaluar_modelo.py

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]