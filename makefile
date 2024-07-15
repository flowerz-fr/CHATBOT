.PHONY: initialize-environment
init_env_os:
	python -m venv .venv
	source .venv/bin/activate
	python -m pip install -r requirements.txt

init_env_win:
	python -m venv .venv
	.venv/Scripts/Activate.ps1
	python -m pip install -r requirements.txt


.PHONY: initialize-runpod
init_runpod:
	git config --global user.name "MilenkaCiprian"
	git config --global user.email "giovana.ciprian@gmail.com"