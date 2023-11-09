FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt ./
CMD ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]
