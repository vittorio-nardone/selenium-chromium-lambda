FROM lambci/lambda:python3.6

USER root

ENV APP_DIR /var/task

WORKDIR $APP_DIR

COPY requirements.txt .

RUN mkdir -p $APP_DIR/lib
RUN pip3 install -r requirements.txt -t $APP_DIR/lib

COPY bin /opt/bin



