FROM python:3.9-alpine
WORKDIR /app
EXPOSE 5168
RUN pip3 install flask -i https://mirrors.ustc.edu.cn/pypi/web/simple \
     && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
     && echo 'Asia/Shanghai' >/etc/timezone 
COPY . /app
RUN chmod 777 /app/*
ENTRYPOINT ["python3", "signapi.py"]
