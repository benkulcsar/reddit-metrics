test: mypy pytest

mypy:
	mypy . --ignore-missing-imports

pytest:
	pytest

pre-commit:
	pre-commit run --all-files

run-extract:
	python src/extract.py

terraform-init:
	cd terraform; terraform init -backend-config=backend.tfvars -migrate-state

create-extract-lambda:
	rm -rf ./extract_lambda extract_lambda.zip
	mkdir extract_lambda
	pip install $$(cat requirements.txt | grep -v boto) --target ./extract_lambda
	cp -r ./src/*.py ./extract_lambda/; mkdir ./extract_lambda/clients && cp -r ./src/clients/*.py ./extract_lambda/clients/
	cd extract_lambda; zip -r ../extract_lambda.zip *; cd ..
	rm -rf ./extract_lambda

deploy: test create-extract-lambda
	cd terraform && terraform apply -auto-approve
