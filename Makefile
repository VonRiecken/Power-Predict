all: install

run_install:
	pip install -e .

run_app:
	streamlit run power_predict/app/app.py

run_sandbox:
	python sandbox.py

run_api:
	uvicorn power_predict.api.fastapi:app --reload

train_models:
	python power_predict/models/train_models.py
