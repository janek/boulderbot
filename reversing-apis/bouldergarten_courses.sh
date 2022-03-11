#!/bin/bash

curl 'https://backend.dr-plano.com/courses_list?id=66563713' \
    -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0' \
    -H 'Accept: */*' \
    -H 'Accept-Language: en-US,en;q=0.5' \
    -H 'Accept-Encoding: gzip, deflate, br' \
    -H 'Origin: https://bouldergarten.de' \
    -H 'Connection: keep-alive' \
    -H 'Referer: https://bouldergarten.de/' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: cross-site'
