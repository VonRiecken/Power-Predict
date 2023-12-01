FROM python:3.10.6-buster

WORKDIR /prod

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY power_predict power_predict
COPY setup.py setup.py

RUN pip install .

COPY Makefile Makefile
# RUN make reset_local_files

CMD uvicorn power_predict.api.fastapi:app --host 0.0.0.0 --port $PORT
