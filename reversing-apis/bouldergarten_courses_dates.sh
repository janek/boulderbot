#!/bin/bash

# https://backend.dr-plano.com/courses_dates?id=67359814&advanceToFirstMonthWithDates=&start=1646089200000&end=1648764000000
# id = 67359814 -> hall ID of Bouldergarten
# advanceToFirstMonthWithDates -> ???
# start = 1646089200000, GMT +1 -> March 1, 00:00:00
# end = 1648764000000, GMT +2 (because of daylifght savings time) -> April 1, 00:00:00
curl 'https://backend.dr-plano.com/courses_dates?id=67359814&advanceToFirstMonthWithDates&start=1646089200000&end=1648764000000' \
    -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0' \
    -H 'Accept: */*' \
    -H 'Accept-Language: en-US,en;q=0.5' \
    -H 'Origin: https://bouldergarten.de' \
    -H 'Connection: keep-alive' \
    -H 'Referer: https://bouldergarten.de/' \
    -H 'Sec-Fetch-Dest: empty' \
    -H 'Sec-Fetch-Mode: cors' \
    -H 'Sec-Fetch-Site: cross-site' \
    -H 'TE: trailers'


{
  "selector": [
    [
      0,
      null,
      true
    ],
    67359814,
    11,
    9,
    0,
    645,
    1646089200000,
    1646175600000,
    "EIK-9-645"
  ],
  "bookableFrom": 0,
  "state": "NOT_BOOKABLE_ANYMORE",
  "bookableUntilDuration": 0,
  "minCourseParticipantCount": 1,
  "maxCourseParticipantCount": 15,
  "currentCourseParticipantCount": 11,
  "dateList": [
    {
      "start": 1646125200000,
      "end": 1646132400000
    }
  ]
}

JSON
