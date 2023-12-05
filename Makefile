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

create_dataset:
	python power_predict/interface/create_dataset.py

delete_local_datasets:
	rm -r power_predict/data/*
