FROM procraft/s3-backuper:latest

ARG aws_id
ARG aws_secret
ARG aws_region

RUN /root/s3-configure.py ${aws_id} ${aws_secret} ${aws_region}

# this is workaround for strange problem of accessibility of s3 us-west2 region via https from simpleclound hosting
RUN aws configure set default.s3.use_dualstack_endpoint true
