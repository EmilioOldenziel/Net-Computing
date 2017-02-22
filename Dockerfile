FROM ubuntu:latest
RUN apt-get upgrade
RUN apt-get update -y
RUN apt-get install  python-pip python-dev build-essential
COPY . /netcomp
WORKDIR /netcomp
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["netcomp.py"]