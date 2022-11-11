# Source: https://aws.amazon.com/blogs/mt/get-notified-specific-lambda-function-error-patterns-using-cloudwatch/
# A copy of the License is located at## http://aws.amazon.com/apache2.0/
# or in the "license" file accompanying this file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
# Description: This Lambda function sends an email notification to a given AWS SNS topic when a particular
#              pattern is matched in the logs of a selected Lambda function. The email subject is
#              Execution error for Lambda-<insert Lambda function name>.
#              The JSON message body of the SNS notification contains the full event details.
# Author: Sudhanshu Malhotra
from __future__ import annotations

import base64
import gzip
import json
import logging
import os

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def logpayload(event):
    logger.setLevel(logging.DEBUG)
    logger.debug(event["awslogs"]["data"])
    compressed_payload = base64.b64decode(event["awslogs"]["data"])
    uncompressed_payload = gzip.decompress(compressed_payload)
    log_payload = json.loads(uncompressed_payload)
    return log_payload


def error_details(payload):
    error_msg = ""
    log_events = payload["logEvents"]
    logger.debug(payload)
    loggroup = payload["logGroup"]
    logstream = payload["logStream"]
    lambda_func_name = loggroup.split("/")
    logger.debug(f"LogGroup: {loggroup}")
    logger.debug(f"Logstream: {logstream}")
    logger.debug(f"Function name: {lambda_func_name[3]}")
    logger.debug(log_events)
    for log_event in log_events:
        error_msg += log_event["message"]
    logger.debug("Message: %s" % error_msg.split("\n"))
    return loggroup, logstream, error_msg, lambda_func_name


def publish_message(loggroup, logstream, error_msg, lambda_func_name):
    sns_arn = os.environ["snsARN"]  # Getting the SNS Topic ARN passed in by the environment variables.
    snsclient = boto3.client("sns")
    try:
        message = ""
        message += "\nLambda error  summary" + "\n\n"
        message += "##########################################################\n"
        message += "# LogGroup Name:- " + str(loggroup) + "\n"
        message += "# LogStream:- " + str(logstream) + "\n"
        message += "# Log Message:- " + "\n"
        message += "# \t\t" + str(error_msg.split("\n")) + "\n"
        message += "##########################################################\n"

        # Sending the notification...
        snsclient.publish(
            TargetArn=sns_arn,
            Subject=f"Execution error for Lambda - {lambda_func_name[3]}",
            Message=message,
        )
    except ClientError as e:
        logger.error("An error occured: %s" % e)


def lambda_handler(event, context):
    pload = logpayload(event)
    lgroup, lstream, errmessage, lambdaname = error_details(pload)
    publish_message(lgroup, lstream, errmessage, lambdaname)
