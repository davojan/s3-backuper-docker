FROM python:3.5-alpine

MAINTAINER davojan

RUN pip install --upgrade pip

RUN pip install awscli plumbum

COPY *.py /root/

RUN chmod a+x /root/*.py && \
    python -OO -m compileall -l /root/

ONBUILD RUN /root/s3-configure.py

ENTRYPOINT ["/root/s3-backuper.py"]
