FROM python:3.5.1
MAINTAINER joway wong "joway.w@gmail.com"

# Install packages
RUN apt-get update && apt-get install -y \
    git \
    libmysqlclient-dev \
    mysql-client \
    nginx \
    supervisor

RUN mkdir /code
WORKDIR /code

# for cache
# Configure Nginx and uwsgi
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
ADD ./requirements.txt /code/requirements.txt
RUN rm /etc/nginx/sites-enabled/default
ADD ./.deploy/nginx.conf /etc/nginx/sites-enabled/nginx.conf
ADD ./.deploy/supervisord.conf /etc/supervisor/conf.d/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /code

EXPOSE 80
CMD ["supervisord", "-n"]


