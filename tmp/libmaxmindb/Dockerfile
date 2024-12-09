FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    gcc \
    make \
    autoconf \
    automake \
    libtool \
    valgrind \
    git

WORKDIR /home/soumya/Automation/git_repos

RUN git clone https://github.com/maxmind/libmaxminddb.git

COPY ./libmaxminddb /home/soumya/Automation/git_repos/libmaxminddb

WORKDIR /home/soumya/Automation/git_repos/libmaxminddb

RUN ./configure && make && make check && ldconfig