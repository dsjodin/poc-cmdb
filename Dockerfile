FROM python:3-alpine

RUN pip install --upgrade pip

# Create app directory
WORKDIR /app

RUN pip install --no-cache-dir flask psycopg2-binary

# Bundle app source
COPY  . /app

ENTRYPOINT ["python"]

CMD ["cmdb_app.py"]
