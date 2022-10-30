FROM python:3.11

# environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_PATH=/usr/src/app

WORKDIR $APP_PATH

# install dependencies
RUN pip install --upgrade pip
# [optimization] I am copying just the requirements.txt file first. Why? Because this file has a smaller rate of change compared to the .py, .html, .js, .css project files.
COPY ./requirements.txt $APP_PATH
RUN pip install -r requirements.txt

# copy project
COPY . $APP_PATH