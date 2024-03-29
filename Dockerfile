FROM python:3.9-alpine
WORKDIR /app
EXPOSE 17840
RUN pip3 install flask \
     && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
     && echo 'Asia/Shanghai' >/etc/timezone 
COPY . /app
RUN chmod 777 /app/*
ENTRYPOINT ["python3", "signapi.py"]
