FROM python:3.12-alpine
COPY . /app
WORKDIR /app 
RUN apk add --no-cache   \
    && pip install --upgrade pip \
    && pip install -r requirements.txt
# Expose port and set environment variable
EXPOSE 80
ENV NAME World
# Run the application
CMD ["python", "main.py"]

