clean:		## delete pycache, build files
	@rm -rf build build.zip 
	@rm -rf __pycache__

## create Docker image with requirements
docker-build:	
	cd bin; unzip -u ../chromium.zip 
	docker-compose build

## run "src.lambda_function.lambda_handler" with docker-compose
## mapping "./tmp" and "./src" folders. 
## "event.json" file is loaded and provided to lambda function as event parameter  
lambda-run:	docker-build		
	docker-compose run lambda src.lambda_function.lambda_handler 

## create Docker image with requirements
docker-build:		
	docker-compose build

## run "src.lambda_function.lambda_handler" with docker-compose
## mapping "./tmp" and "./src" folders. 
## "event.json" file is loaded and provided to lambda function as event parameter  
lambda-run:			
	docker-compose run lambda src.lambda_function.lambda_handler 

## prepares build.zip archive for AWS Lambda deploy 
lambda-build: clean 
	mkdir build build/lib
	cp -r src build/.
	cp -r bin build/.
	cd build/bin; unzip -u ../../chromium.zip 
	pip3 install -r requirements.txt -t build/lib
	cd build; zip -9qr build.zip .
	cp build/build.zip .
	rm -rf build

## create CloudFormation stack with lambda function and role.
## usage:	make BUCKET=your_bucket_name create-stack 
create-stack: 
	aws s3 cp build.zip s3://${BUCKET}/src/ScreenshotFunction.zip
	aws cloudformation create-stack --stack-name LambdaScreenshot --template-body file://cloud.yaml --parameters ParameterKey=BucketName,ParameterValue=${BUCKET} --capabilities CAPABILITY_IAM