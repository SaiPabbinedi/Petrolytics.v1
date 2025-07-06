FROM python:3.12.1-slim as builder

WORKDIR /app

RUN pip install --upgrade pip
COPY frontend/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12.1-slim

RUN useradd --create-home appuser
WORKDIR /home/appuser

COPY --from=builder /root/.local /home/appuser/.local

COPY frontend/ ./

RUN chown -R appuser:appuser ./

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]