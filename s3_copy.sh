#!/bin/bash

S3_BUCKET="s3://zappa-j2ith0vcq"

declare -a COPY_ITEMS=("static/css/style.css" "static/js/index.js" "static/favicon.ico" "static/images/main_logo_en.png")

for item in ${COPY_ITEMS[@]}
    do
        aws s3 cp $item $S3_BUCKET/$item --acl public-read
    done
