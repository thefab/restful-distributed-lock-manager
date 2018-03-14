FROM python:2.7
LABEL author="stakater"

EXPOSE 8888

RUN apt-get update

# based on python:2.7-onbuild, but if we use that image directly
# the above apt-get line runs too late.
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY pip-requirements.txt /usr/src/app/
RUN pip install -r pip-requirements.txt

COPY . /usr/src/app
RUN make -f Makefile-Build install

CMD python rdlm-daemon.py