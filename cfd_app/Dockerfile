# Dockerfile for CFD App

FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]