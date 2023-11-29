all: install

install:
	pip install -e .
	python setup.py install

app:
	streamlit run power_predict/app/app.py

sandbox:
	python sandbox.py
