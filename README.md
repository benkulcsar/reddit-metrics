# Reddit Metrics

## What's this?

This repository is dedicated to one of my hobby projects, which focuses on visualising upvote ratios and other metrics for selected subreddits.

**[Link to the dashboard](https://datastudio.google.com/reporting/865759fa-0b1a-4bee-8b67-89cb2ed0d2f0 "Looker Studio")**

!["Dashboard"](images/dash.png?v=4&s=200 "Dashboard")

## How was it built?

### Tools

The project was developed using the following tools:

- Python 3.9
- Docker, Make and Terraform
- AWS: S3, Lambda, EventBridge and ECR (managed by Terraform)
- GCP: GCS, BigQuery, and Looker Studio

### High Level Architecture

!["Architecture"](images/architecture.png?v=4&s=200 "Architecture")

The project utilises Lambda functions deployed as Docker images.

Additionally, SNS is used for email alerting. A separate Lambda function subscribes to CloudWatch logs and forwards any error-containing logs to SNS.

## How to deploy and run this?

The following instructions are provided for future reference when fixing or modifying the project.
### Environment Variables

Ensure that the following environment variables are set before running the project:

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (except if running in AWS)
- `AWS_ACC_NO` and `AWS_REGION` (for ECR)
- `TF_VAR_REDDIT_CLIENT_ID`, `TF_VAR_REDDIT_CLIENT_SECRET` and `TF_VAR_REDDIT_S3_BUCKET`
- `GCP_ACCESS_KEY` and `GCP_SECRET_ACCESS_KEY` (to access Google Cloud)
- `MY_EMAIL` (for email alerts from SNS)

### Run Locally (for testing and development)

Clone the project, create a virtual environment and install dependencies. Example using pyenv:

```bash
git clone https://github.com/benkulcsar/reddit-metrics
cd reddit-metrics
pyenv virtualenv 3.9.0 reddit
pyenv activate reddit
pip install .[test|extract|transform]
```

Run tests (pytest, mypy, etc):

```bash
pre-commit run -a
```

Run the tasks:

```bash
python src/extract.py
python src/transform.py -b [BUCKET] -k [KEY]
python src/load.py -b [BUCKET] -k [KEY]
```

### Deploy

For deployment on AWS, it is necessary to set up Terraform with an S3 backend.

*Note: Before deploying for the first time, the ECR repositories must be created. To create them, execute a Terraform apply command, which will eventually fail when attempting to create the Lambdas without the Docker images.*

```bash
make terraform-init
make deploy-extract
make deploy-transform
make deploy-load
```

### Re-running / Backfilling

Both the transform and load Lambdas can be triggered using a custom test event that specifies a list of objects. This enables re-running or backfilling functionality.

Format of the event:
```json
{
    "Backfill":[
      {"bucket":"bucket_name","key":"obj_key1"},
      {"bucket":"bucket_name","key":"obj_key2"}
    ]
}
```

Alternatively, the same result can be achieved by a series of local runs.

Example:
```bash
python src/transform.py -b bucket_name -k obj_key1
python src/transform.py -b bucket_name -k obj_key2
```
