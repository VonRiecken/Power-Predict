FROM python:3.10.6-buster

WORKDIR /prod

COPY requirements_prod.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY power_predict power_predict
COPY setup.py setup.py

RUN pip install .

COPY Makefile Makefile
# RUN make train_models

CMD uvicorn power_predict.api.fastapi:app --host 0.0.0.0 --port $PORT
