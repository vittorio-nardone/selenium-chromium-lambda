# selenium-chromium-lambda

How to run automated (Selenium) Headless Chromium in AWS Lambda.

Read full article [https://www.vittorionardone.it/en/2020/06/04/chromium-and-selenium-in-aws-lambda](https://www.vittorionardone.it/en/2020/06/04/chromium-and-selenium-in-aws-lambda)

An example about taking a full height screenshot of a given webpage in Python.

## Contents

Selenium wrapper to get a full height screenshot of a given webpage. Code is in `src/webdriver_screenshot.py`.

Lambda source code is in `src/lambda_function.py`. It's a sample function using wrapper to get screenshot of a given URL. Fixed size and full height size screenshots are saved to a S3 bucket.

CloudFormation template to create Lambda stack. Please change `WebSite` parameter to your favorite URL.

## Commands

`make fetch-dependencies` to download chromedriver and headless-chrome

`make lambda-build` to prepare archive for AWS Lambda deploy 

`make BUCKET=<your_bucket_name> create-stack` to create CloudFormation stack (lambda function and IAM role)

## Credits

Inspired by [this awesome project](https://github.com/21Buttons/pychromeless)
