.PHONY: help tests black isort bandit format pydantic-schema serve
default: help

MAIN_SRC_DIRECTORY="takeout_maps"
PYTHON_SRC_DIRECTORIES=${MAIN_SRC_DIRECTORY} "tests" "scripts" 

tests: # Run tests using pytest.
	pytest --cov=${MAIN_PACKAGE_DIRECTORY} --cov-report term-missing

black: # Format the python files using black.
	black ${PYTHON_SRC_DIRECTORIES}

isort: # Sort the imports in python files.
	isort ${PYTHON_SRC_DIRECTORIES}

bandit: # Run security checks with bandit.
	bandit -r ${MAIN_PACKAGE_DIRECTORY}

docstrings: # Format the docstrings using docformatter
	docformatter --in-place -r ${PYTHON_SRC_DIRECTORIES};  pydocstyle ${PYTHON_SRC_DIRECTORIES}

format: isort black docstrings # Format the source files with isort and black.

mypy: # Check types with mypy.
	mypy ${PYTHON_SRC_DIRECTORIES}

qc: format tests bandit mypy # Run all the QC tasks.

pydantic-schema: # Generate the Pydantic schema from xsd files.
	python3 scripts/generate_schema.py

serve: 
	python -m takeout_maps --takeout=${takeout}

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m\n\t$$(echo $$l | cut -f 2- -d'#')\n"; done
