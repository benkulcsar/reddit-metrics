# Reddit Statistics Dashboard

## About the Project

### Objective

A simple dashboard to compare aggregated metrics of data and programming related subreddits over time: upvotes, downvotes, upvote ratio, awards, new posts, etc.

### Roadmap

* [x] AWS infra
* [x] Extract (lambda)
* [X] Transform (lambda)
* [ ] Load (lambda)
* [ ] Dashboard (looker studio)
* [ ] Improvements from the backlog

### Tools

- Python 3.9
- PRAW Reddit API Wrapper
- AWS: S3, Lambda and EventBridge (with Terraform)

## Deploy and Run

### Environment Variables

The project requires the following environment variables to be set:

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (except if running in AWS)
- `AWS_ACC_NO` and `AWS_REGION` (for ECR)
- `TF_VAR_REDDIT_CLIENT_ID`, `TF_VAR_REDDIT_CLIENT_SECRET` and `TF_VAR_REDDIT_S3_BUCKET`

### Run Locally (for testing and development)

Clone the project, create a virtual environment and install dependencies. Example using pyenv:

```bash
git clone https://github.com/benkulcsar/reddit-stats
cd reddit-stats
pyenv virtualenv 3.9.0 reddit
pyenv activate reddit
pip install .[test|extract|transform]
```

Run tests (pytest, mypy, etc):

```bash
pre-commit run -a
```

Run the extract task:

```bash
make extract
```

Run the transform task:

```bash
python src/transform.py -b [BUCKET] -k [KEY]
```

### Deployment

Deploying in AWS requires terraform set up to use an S3 backend:

```bash
make deploy-extract
make deploy-transform
```
