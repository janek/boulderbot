#!/bin/bash

# https://backend.dr-plano.com/courses_reserve

# shiftSelector = [[0,null,true],155581628,37,34,0,134,1647298800000,1647385200000,"SKB-34-134"]
# shiftSelector = [[0,null,true],67359814,26,24,0,656,1647039600000,1647126000000,"EIK-24-656"]

# Tue, 15.03 18:00-20:00, Basement Boulderstudio
# shiftModelId = 155581628
# email = jan.szynal%40gmail.com
# shiftSelector = [[0,null,true],155581628,37,34,0,134,1647298800000,1647385200000,"SKB-34-134"]
# participantCount = 1
curl 'https://backend.dr-plano.com/courses_reserve?shiftModelId=155581628&email=jan.szynal%40gmail.com&shiftSelector=%5B%5B0%2Cnull%2Ctrue%5D%2C155581628%2C37%2C34%2C0%2C134%2C1647298800000%2C1647385200000%2C%22SKB-34-134%22%5D&participantCount=1' \
    -X POST \
    -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0' \
    -H 'Accept: */*' \
    -H 'Accept-Language: en-US,en;q=0.5' \
    -H 'Accept-Encoding: gzip, deflate, br' \
    -H 'Content-Type: application/json' \
    -H 'Origin: https://basement-boulderstudio.de' \
    -H 'Connection: keep-alive' \
    -H 'Referer: https://basement-boulderstudio.de/' \
    -H 'Sec-Fetch-Dest: empty' \
    -H 'Sec-Fetch-Mode: cors' \
    -H 'Sec-Fetch-Site: cross-site' \
    -H 'Content-Length: 0' \
    -H 'TE: trailers'

# Tue, 15.03 17:30-19:30, Bouldergarten
# shiftModelId = 67359814
# email = jan.szynal%40gmail.com
# shiftSelector = shiftSelector=[[0,null,true],67359814,26,24,0,656,1647039600000,1647126000000,"EIK-24-656"]
# participantCount = 1

curl 'https://backend.dr-plano.com/courses_reserve?shiftModelId=67359814&email=jan.szynal%40gmail.com&shiftSelector=%5B%5B0%2Cnull%2Ctrue%5D%2C67359814%2C26%2C24%2C0%2C656%2C1647039600000%2C1647126000000%2C%22EIK-24-656%22%5D&participantCount=1' \
    -X POST \
    -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0' \
    -H 'Accept: */*' \
    -H 'Accept-Language: en-US,en;q=0.5' \
    -H 'Accept-Encoding: gzip, deflate, br' \
    -H 'Content-Type: application/json' \
    -H 'Origin: https://bouldergarten.de' \
    -H 'Connection: keep-alive' \
    -H 'Referer: https://bouldergarten.de/' \
    -H 'Sec-Fetch-Dest: empty' \
    -H 'Sec-Fetch-Mode: cors' \
    -H 'Sec-Fetch-Site: cross-site' \
    -H 'Content-Length: 0' \
    -H 'TE: trailers'
