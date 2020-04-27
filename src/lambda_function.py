import boto3
import os
import logging
import uuid
from webdriver_screenshot import WebDriverScreenshot

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
 
    logger.info('Generate full height screenshot')
    driver = WebDriverScreenshot()
    screenshot_file = str(uuid.uuid4()) + ".png"
    driver.save_screenshot(os.environ['URL'], '/tmp/{}'.format(screenshot_file))
    driver.close()

    ## Upload generated screenshot file to S3 bucket.
    s3.upload_file('/tmp/{}'.format(screenshot_file), 
                   os.environ['BUCKET'], 
                   '{}/{}'.format(os.environ['DESTPATH'], screenshot_file))

