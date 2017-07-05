FROM python:3.5
FROM django

RUN mkdir -p /Users/renminghe/xiaomingBook
WORKDIR  /Users/renminghe/xiaomingBook

COPY . /Users/renminghe/xiaomingBook
RUN python3 manage.py migrate

EXPOSE 8000
CMD ["python3", "manage.py", "runserver"]
