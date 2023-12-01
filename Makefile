all: install

<<<<<<< HEAD
install:
=======
run_install:
>>>>>>> 843a8870693ccc43c778f3a96650a874b3318822
	pip install -e .
	python setup.py install

run_app:
	streamlit run power_predict/app/app.py

run_sandbox:
	python sandbox.py

run_api:
	uvicorn power_predict.api.fastapi:app --reload
