# Stage 1: Install requirements 
FROM python:3.11.12-slim AS base

LABEL MAINTAINER="Kittichai Inkhumpan <kittichai.ink@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11.12-slim AS production

COPY --from=base /usr/local /usr/local

COPY . ./app

WORKDIR /app


CMD ["streamlit", "run", "app.py" , "--server.port=8501", "--server.address=0.0.0.0"]