FROM python:2.7
#RUN python -m pip install --upgrade pip
RUN pip install lxml && pip install openxmllib && pip install requests  && pip install flask 
RUN mkdir app
COPY ./flask ./app/flask
WORKDIR /app/flask
EXPOSE 5000
#CMD "source" "env/bin/activate"
#CMD  "python" "./run.py"
CMD export FLASK_APP=run.py; export FLASK_ENV=development; flask run --host=0.0.0.0
