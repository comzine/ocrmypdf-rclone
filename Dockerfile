# Extend the existing ocrmypdf image
FROM jbarlow83/ocrmypdf

# Install curl, unzip, and fuse
RUN apt-get update \
    && apt-get install -y curl unzip fuse util-linux wget jq \
    && curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip \
    && unzip rclone-current-linux-amd64.zip \
    && cd rclone-*-linux-amd64 \
    && cp rclone /usr/bin/ \
    && chown root:root /usr/bin/rclone \
    && chmod 755 /usr/bin/rclone \
    && rm -rf /tmp/* /var/lib/apt/lists/* rclone-*-linux-amd64.zip

ENV RCLONE_CONFIG="/config/rclone.conf"

RUN ln -s /bin/fusermount /bin/fusermount3

# Set up a volume for the rclone configuration
VOLUME ["/config"]

COPY entrypoint.sh /entrypoint.sh
COPY ocrmypdf.json /ocrmypdf.json
COPY watchit.py /app/watchit.py
RUN chmod +x /entrypoint.sh && chmod +x /app/watchit.py && chmod +r /ocrmypdf.json

USER root

RUN mkdir /input \
    && chmod 777 /input \
    && mkdir /output \
    && chmod 777 /output \
    && mkdir /processed \
    && chmod 777 /processed

ENTRYPOINT ["/entrypoint.sh"]
