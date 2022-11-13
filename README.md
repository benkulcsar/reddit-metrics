# Reddit Metrics

## About the Project

### Objective

Create an ETL pipeline for a simple dashboard showing upvote ratios of selected subreddits over time:

**[Link to the dashboard](https://datastudio.google.com/reporting/1969ea1a-3a19-4061-aa8a-43df7739af68 "Looker Studio")**

!["Dashboard"](images/dash.png?v=4&s=200 "Dashboard")

### Roadmap

* [x] AWS infra
* [x] Extract (lambda)
* [X] Transform (lambda)
* [X] Load (lambda)
* [X] Dashboard (looker studio)
* [X] Improvements from the "must have" backlog
* [ ] Improvements from the "nice to have" backlog (see below)

### Tools

- Python 3.9
- Docker, Make and Terraform
- AWS: S3, Lambda, EventBridge and ECR (with Terraform)
- GCP: GCS, BigQuery and Looker Studio

### High Level Architecture

!["Architecture"](images/architecture.png?v=4&s=200 "Architecture")

Lambda functions are deployed using docker images.

SNS is used for email alerting. A separate lambda function is subscribed to CloudWatch logs and forwards the ones containing errors to SNS.

## Deploy and Run

### Environment Variables

The project requires the following environment variables to be set:

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

Deploying in AWS requires terraform set up to use an S3 backend.

*Note: the ECR repos have to be created first which requires a terraform apply that eventually fails when trying to create the lambdas without the docker images.*

```bash
make terraform-init
make deploy-extract
make deploy-transform
make deploy-load
```

### Re-running / Backfilling

Both the transform and the load lambdas can be triggered with a custom test event specifying a list of objects that enables re-running / backfilling.
Format of the event:
```json
{
    "Backfill":[
      {"bucket":"bucket_name","key":"obj_key1"},
      {"bucket":"bucket_name","key":"obj_key2"}
    ]
}
```

Alternatively, a series of local runs can achieve the same result, for example:
```bash
python src/transform.py -b bucket_name -k obj_key1
python src/transform.py -b bucket_name -k obj_key2
```

## Backlog (nice to haves)

* [X] Add `num_comments` to the RedditPost model
* [ ] Add new metrics (e.g. number of posts)
* [ ] Dashboard improvements (e.g. moving average)
* [ ] Review list of subreddits
* [ ] Make Terraform code DRY
* [ ] Catch and handle exceptions that don't have to stop the lambdas
* [ ] Create ECR repos with Terraform before deploying (see note in Deployment section)
* [ ] Test the actual ETL methods in integration tests
