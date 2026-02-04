FROM python:3.11-slim

WORKDIR /app
RUN pip install --no-cache-dir -U pip

COPY pyproject.toml /app/
RUN pip install --no-cache-dir -e ".[dev]"

COPY app /app/app
COPY tests /app/tests

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]