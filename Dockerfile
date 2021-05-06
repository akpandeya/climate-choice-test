FROM python

COPY ./requirements.txt /code/requirements.txt

WORKDIR /code

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "slack_file_upload.py"]