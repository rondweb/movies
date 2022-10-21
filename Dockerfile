FROM tiangolo/uwsgi-nginx-flask:python3.9

COPY ./app /app
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# # copy every content from the local file to the image
# COPY . /app
EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]