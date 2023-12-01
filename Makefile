all: install

run_install:
	pip install -e .
	python setup.py install

run_app:
	streamlit run power_predict/app/app.py
=======

run_sandbox:
	python sandbox.py
=======

run_api:
	uvicorn power_predict.api.fastapi:app --reload
