FROM alexellis2/python-gpio-flask:v6

#ADD controller.py ./
#ADD config.json ./
#ADD spreadsheet.py ./
#ADD client_secret.json ./

#RUN mkdir /www  
#COPY www /www

EXPOSE 8000
WORKDIR /root

# RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
# USER docker
 
RUN pip install pigpio gspread oauth2client
RUN sudo apt-get update && apt-get install python-twisted

CMD ["python2", "controller.py"]
