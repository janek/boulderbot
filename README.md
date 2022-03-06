# Deployment & hosting

### Versions
- v0.1 - Bot works both on heroku and locally, checking doesn't 

### Current
1. Test caching locally
2. Test on heroku
3. Super simple server vs express or something?
   - bro webhook instead 
4. Hosting dilemma: 
 - Double Heroku for hosting?
 - What is a "worker" process? 
 - Do we need a port for the caching? What if we invert things and do a webhook instead?

### Basics
- Telegram bot used to fetch information from the website(s) and present them, so it just needed one port to run
- I implemented caching to a JSON file and wanted to add a web frontend
- now there are 3 things to host:
    - Telegram bot frontend
    - Website frontend
    - “Backend” (periodic cache refresh)

### Considerations: 
- keep or quit heroku:
	- apparently you can’t have more than one port on a heroku dyno (hence the problem)
	- it was a bit painful to set up. Now it feels okay, but still not easy. Is it worth keeping or worth switching?
	- it's free
- be very careful about false or low priority performance concerns
	- example: maybe the website doesn’t need to run on the same machine as the telegram bot 
	- very little matters before there are users; it's probably fast enough - could 
	- fetching 600 lines of json really shouldn’t be a problem
- it might be a pain to get selenium and chrome working (maybe not with docker)
- the website could be separate, deployed to Netlify or Vercel
- having three different deployments doesn’t sound good either though

Options:
- vercel for webapp, heroku for telegram, what's the connection? webhook, api?
- docker for everything?
  
Questions:
- Should I have used a database?
- Should I be using webhooks? 

### Current context

### Older context
- json dilemma: should we save {free_slots: "0} or just ignore an empty timeslot
	- lean towards ignore because that's what webclimber does
- create a cache with slots, refresh conservatively at first 
	- can there be a vpn? because of suspicous calls - leave for later but note down
	-  read from cache on call, maybe also say how old the cache is or something
	- do we need to save in a DB? since the website needs to serve it -
		- maybe we just have an API and do an API call? go for easiest at first
		- ideally a scheduled refresh should push an update to the website
			- can that be done by just overwriting the HTML? that would be bonkers easy, but maybe bad practice?
		- setting up the website already would be very satisfying! why not? - https://gist.github.com/wh1tney/2ad13aa5fbdd83f6a489
- create a user if not existing in DB
	- 176G, boulderbot.py
- make sure one version of the bot works on both deployments
- check if an exception breaks the program - it should keep running
	- also make sure the whole stacktrace is not printed
	- maybe https://stackoverflow.com/questions/14695330/python-how-to-keep-program-going-after-exception-is-caught
- fix bouldergarten for the nth time 

### Next steps
- 🏓 user registration!
- fix local vs remote (print env vars and check why IS_HEROKU doesn't work)
	- make sure that sth is printed on IS_HEROKU, because otherwise moving to another server would break things
	- it seems like local vs remote work, but why aren't we just using webhooks locally? I guess it doesn't matter too much if it works at the moment
- secure sheetDB API on their website, implement auth in Heroku
- consider starting a test deploy to have clean & versioned releases on production
- try/except blocks, handling empty input, too
- fix bugs: off by one and "specific day"

(later)
- 'gym' structs in code 
	- name, emoji, link, what else?
	- hardcode: also save the path to check and book as a series of steps
	
(older)

- for the common section, support choosing day 
- for booking, support choosing hour
- add config parameters to telegram commands
- improve documentation
- webclimbers: https://141.webclimber.de/de/booking/book/boulderslots-gesamt?date=2021-11-27&time=09%3A00&period=2&places=1&persons=1&place_id=29

**Optional:**
- get booking to work locally

### Version roadmap
- book()
	- For a person 
		- Hardcoded as Janek (DONE)
		- Implement registration
		- Book for anyone
	- For a slot
		- specific free slot (DONE)
		- specific slot, free or not 
		- payment method
		- +1 or +2 possibility 
- check():
	- For the next day, one hall
	- if time is passed, only a little earlier and till the end of the day
	- (upper bound of time could also be passed, but low priority)
- Supported halls:
	- Bouldergarten
	- all Dr Plano (Bouldergarten & Boulderklub)
	- all Dr Plano & webclimber
- Other:
	-	fake usc number


- recorded a clickthru in Selenium's Firefox extension
- tutorial from towardsdatascience (https://towardsdatascience.com/how-to-use-selenium-to-web-scrape-with-example-80f9b23a843a)

- record smaller test in Vivaldi (Chromium) Selenium IDE 
	- export
	- failed in Safari, try chrome and firefox drivers
	- evtl. try webclimber, it might be easier
		- note the numbers, like 135.webclimber.de
- next: have working code that checks avail. slots
- python sleeps should later be replaced with selenium wait functions

### Troubleshooting: endless problems with dr plano
- Bouldergarten
  - 88bf602: selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <div href="javascript:void(0)" class="drp-calendar-day drp-calendar-day-dates">...</div> is not clickable at point (820, 802). Other element would receive the click: <div class="drp-calendar-legend drp-mt-2">...</div>
  
- Boulderklub
  - 88bf602: selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//div[text()='
								6
							']"}


### Troubleshooting: bot doesn't work
- try echobot_original.py with janek and with bukowski tokens 

### Current problems
- why don't webhooks work locally? would make things easier
- 2min heroku sleep timer

### Potential problems
- if 0000, zeros get truncated - remember for phone
- can you update a user? if yes, can somebody else update your user? maybe generate a password? (for sure at first do not update users)
	- if we generate the passwords, and they cannot be changed, we can proudly store passwords in plaintext
- if we calc dates based on the "dates" class then we might be wrong if today is ausgebucht (but maybe)
### Past problems
- 
- needs chrome version 95 -> managed to get it
- Safari webdriver didn't work -> use Firefox
- Cookie banner can obscure view -> click it -> it's only there the first time -> block cookies for the site in Firefox so that it doesn't appear again
-  `selenium.common.exceptions.ElementClickInterceptedException: Message: Element <h3 id="eintritt-buchen" class="ffHeavy"> is not clickable at point (616,628) because another element <span id="cn-notice-text" class="cn-text-container"> obscures it` (despite previous point) - >
- was breaking on finding css .drp-calendar-day-dates -> adding sleep everywhere solves most problems
