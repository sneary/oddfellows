FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY meeting_plans.py meeting_plans.py

CMD ["python", "meeting_plans.py"]
