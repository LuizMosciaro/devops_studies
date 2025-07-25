
FROM python:3.12-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP=app
EXPOSE 8000
CMD ["python3", "-m", "flask", "--app", "src/phase2/flaskr/app", "run", "--host", "0.0.0.0", "--port", "8000"]
