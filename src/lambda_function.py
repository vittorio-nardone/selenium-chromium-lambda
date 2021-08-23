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
 
    screenshot_file = str(uuid.uuid4())
    driver = WebDriverScreenshot()

    # logger.info('Generate fixed height screenshot')
    # driver.save_screenshot(os.environ['URL'], '/tmp/{}-fixed.png'.format(screenshot_file), width=1245, height=1755)

    png_file_name = '{}-full.png'.format(screenshot_file)
    png_file_path = '/tmp/{}'.format(png_file_name)
    pdf_file_name = png_file_name.replace('.png', '.pdf')
    pdf_file_path = '/tmp/{}'.format(pdf_file_name)
    logger.info('Generate full height screenshot')
    url = event['url']
    format = event['format']
    key_path = event['s3_key']
    bucket = event['s3_bucket'] if 's3_bucket' in event else os.environ['BUCKET']
    driver.save_screenshot(url, png_file_path, width=1245, height=1755)

    driver.close()

    if format == 'png':
        s3.upload_file(png_file_path, 
                    bucket,
                    key_path)
    if format == 'pdf':
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.image(png_file_path, 5, 5, 200)
        pdf.output(pdf_file_path, 'F')
        s3.upload_file(pdf_file_path, 
                    bucket,
                    key_path)

    ## Upload generated screenshot files to S3 bucket.
    # s3.upload_file('/tmp/{}-fixed.png'.format(screenshot_file), 
    #                os.environ['BUCKET'], 
    #                '{}/{}-fixed.png'.format(os.environ['DESTPATH'], screenshot_file))
