pre-commit:
	pre-commit run --all-files

extract:
	python src/extract.py

terraform-init:
	cd terraform; terraform init -backend-config=backend.tfvars -migrate-state

deploy-extract: pre-commit
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com
	docker build -t reddit-extract -f Dockerfile.extract .
	docker tag reddit-extract:latest ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com/reddit-extract:latest
	docker push ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com/reddit-extract:latest
	cd terraform && terraform apply -auto-approve

deploy-transform: pre-commit
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com
	docker build -t reddit-transform -f Dockerfile.transform .
	docker tag reddit-transform:latest ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com/reddit-transform:latest
	docker push ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com/reddit-transform:latest
	cd terraform && terraform apply -auto-approve
