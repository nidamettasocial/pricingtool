# 
FROM python:3.10

# 
WORKDIR /


ENV SQLALCHEMY_DATABASE_URI $SQLALCHEMY_DATABASE_URI
# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY ./app /app


ENV PYTHONPATH "${PYTHONPATH}:/app"
# 
CMD ["uvicorn", "main:app","--workers","3", "--host", "0.0.0.0", "--port", "5000"]