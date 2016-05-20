# Simple Dockerized S3 Backup Tool

Simple S3 Backup Synchronizer. Manages local backup folder with configurable maximum number of backup files and uses [awscli](https://aws.amazon.com/ru/cli/) (``aws s3 sync``) to synchronize the local backup with configurable Amason S3 location.

To show script help:

```bash
docker run --rm davojan/s3-backuper --help
```

## Usage

Before you can use the backup script you should create your own derived docker image with your Amazon credentials:

```bash
mkdir -p path/to/some/dir
cd path/to/some/dir
wget https://raw.githubusercontent.com/davojan/s3-backuper-docker/master/configured-image/Dockerfile
docker build -t foo/s3-backuper --build-arg aws_id='your-aws-id' --build-arg aws_secret='your-aws-secret' --build-arg aws_region='us-west-2' .
```

You can replace ``foo/s3-backuper`` with any valid docker image tag. This image is created locally on your docker host and should never be shared because it contains your credentials.

Now you can call the backuper script. Let's assume you have a running docker container named ``my-service`` which periodically creates backup files in volume ``/data/backups/``. You can create a cron job with command:

```bash
docker run --rm --volumes-from my-service foo/s3-backuper /data/backups/ s3.bucket.name s3/folder/my-service --keep 5
```

This will:

* Scan directory ``/data/backups`` for any new files and move them to the ``_processed`` subfolder with added date-prefix.
* Remove oldest files in ``_processed`` subfolder if there are more then 5 files (``--keep`` option, default is 10).
* Create bucket ``s3.bucket.name`` (if it doesn't exist) in the configured previously region.
* Sync ``_processed/`` subfolder with ``s3://s3.bucket.name/s3/folder/my-service/`` using ``aws s3 sync`` with ``--delete`` switch.

## License

MIT

## Thanks

[Plumbum](http://plumbum.readthedocs.io/)
