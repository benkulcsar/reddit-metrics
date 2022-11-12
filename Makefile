pre-commit:
	pre-commit run --all-files

terraform-init:
	cd terraform; terraform init -backend-config=backend.tfvars -migrate-state
	cd terraform/sns_lambda; zip sns_lambda.zip sns_lambda.py

deploy-extract: pre-commit
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com
	docker build -t reddit-extract -f dockerfiles/Dockerfile.extract .
	docker tag reddit-extract:latest ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com/reddit-extract:latest
	docker push ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com/reddit-extract:latest
	cd terraform && terraform apply -auto-approve

deploy-transform: pre-commit
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com
	docker build -t reddit-transform -f dockerfiles/Dockerfile.transform .
	docker tag reddit-transform:latest ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com/reddit-transform:latest
	docker push ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com/reddit-transform:latest
	cd terraform && terraform apply -auto-approve

deploy-load: pre-commit
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com
	docker build -t reddit-load -f dockerfiles/Dockerfile.load .
	docker tag reddit-load:latest ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com/reddit-load:latest
	docker push ${AWS_ACC_NO}.dkr.ecr.${AWS_REGION}.amazonaws.com/reddit-load:latest
	cd terraform && terraform apply -auto-approve
