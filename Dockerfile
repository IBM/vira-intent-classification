FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# install python and pip
RUN apt update && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.10 python3-pip python3-setuptools python3-distutils && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY logging.conf .
COPY *.py .
COPY intent_dataset/intents.csv intent_dataset/intents.csv

EXPOSE 8000

# run
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--log-config", "logging.conf"]
