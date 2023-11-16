FROM python:3.10

COPY . /diplom

COPY ./requirements.txt /diplom/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /diplom/requirements.txt 

EXPOSE 8000

WORKDIR /diplom

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput 

CMD ["python", "/diplom/manage.py", "runserver", "0.0.0.0:8000"]