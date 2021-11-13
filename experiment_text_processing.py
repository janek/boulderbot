import re
import os

dates_old = '''
<div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
1 freier Platz
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 10:00 - 12:00
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 10:30 - 12:30
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 11:00 - 13:00
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 11:30 - 13:30
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 12:00 - 14:00
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
9 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 12:30 - 14:30
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
6 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 13:00 - 15:00
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
7 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 13:30 - 15:30
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 14:00 - 16:00
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 14:30 - 16:30
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
2 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 15:00 - 17:00
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
11 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 15:30 - 17:30
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 16:00 - 18:00
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 16:30 - 18:30
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 17:00 - 19:00
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
12 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 17:30 - 19:30
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
4 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 18:00 - 20:00
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
9 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 18:30 - 20:30
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
6 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 19:00 - 21:00
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
15 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 19:30 - 21:30
<!----></span></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
3 freie Plätze
</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
Buchen
</span></button></div> <div class="drp-course-date-item-dates drp-w-100 drp-d-table drp-p-2"><div class="drp-course-date-item-date drp-d-table-row"><!----> <span class="drp-d-table-cell">
So., 31.10.21, 20:00 - 22:00
<!----></span></div></div></div>'
'''

dates = '''
<div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            10:00 - 12:00
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            10:30 - 12:30
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
										1 freier Platz
									</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
									Buchen
								</span></button></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            11:00 - 13:00
                            <div class="drp-course-has-started-warning drp-warning drp-mt-2"><span class="drp-fas drp-fa-hourglass-half drp-mr-1"></span>
								bereits begonnen
							</div></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            11:30 - 13:30
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            12:00 - 14:00
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            12:30 - 14:30
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            13:00 - 15:00
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            13:30 - 15:30
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            14:00 - 16:00
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            14:30 - 16:30
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            15:00 - 17:00
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            15:30 - 17:30
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            16:00 - 18:00
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            16:30 - 18:30
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            17:00 - 19:00
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            17:30 - 19:30
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            18:00 - 20:00
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            18:30 - 20:30
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            19:00 - 21:00
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3 drp-date-not-relevant"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <span>ausgebucht</span> <!----> <!----> <!----> <!----> <!----></span> <!----></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            19:30 - 21:30
                            <!----></div></div></div></div></div><div class="drp-course-date-item drp-mb-3"><div class="drp-course-date-item-booking-box drp-p-2"><span><span class="drp-course-date-item-booking-status drp-mr-1"></span> <!----> <!----> <!----> <!----> <!----> <!----> <span><span class="drp-course-date-item-max-participants">
										10 freie Plätze
									</span></span></span> <button class="drp-course-date-item-booking-button drp-ml-2"><span>
									Buchen
								</span></button></div> <div class="drp-course-date-item-dates drp-p-2"><!----> <div><!----> <div><div class="drp-course-date-item-date"><span class="drp-fas drp-fa-calendar-day" style="padding-left: 1px;"></span>
                            Sa., 13.11.21
                            <span class="drp-fas drp-fa-clock drp-pl-2"></span>
                            20:00 - 22:00
                            <!----></div></div></div></div></div>
'''



from pprint import pprint
# dates = dates_old
dates = re.sub('<[^>]*>', '', dates)
lines = [line.strip() for line in dates.splitlines() if len(re.sub('\s*', '', line)) > 0 and not "Buchen" in line and not "begonnen" in line]
# pprint(lines)

date_strings = lines[2::3]
status_strings = lines[::3]
data = [a + " → " + b for a, b in list(zip(date_strings, status_strings)) if not "ausgebucht" in b]
pprint(data)
