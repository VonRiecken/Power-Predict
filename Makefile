all: install

install:
	python setup.py install

app:
	streamlit run power_predict/app/app.py
