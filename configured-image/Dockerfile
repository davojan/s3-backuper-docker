FROM davojan/s3-backuper:0.0.1

ARG aws_id
ARG aws_secret
ARG aws_region

RUN /root/s3-configure.py ${aws_id} ${aws_secret} ${aws_region}
