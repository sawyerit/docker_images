FROM alexellis2/python-gpio-flask:v6

ADD lights.py ./
ADD app.py ./

EXPOSE 5000


# RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

# USER docker


RUN pip install gpiozero 
RUN pip install pigpio

CMD ["python2", "app.py"]
