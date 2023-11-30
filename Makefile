all: install

install:
<<<<<<< HEAD
=======
	pip install -e .
>>>>>>> a5af15a1d3c8793377ee05a03cccea4e5b64855b
	python setup.py install

app:
	streamlit run power_predict/app/app.py
<<<<<<< HEAD
=======

sandbox:
	python sandbox.py
>>>>>>> a5af15a1d3c8793377ee05a03cccea4e5b64855b
