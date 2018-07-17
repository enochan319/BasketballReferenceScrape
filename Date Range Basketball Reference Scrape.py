from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
#outside 

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + datetime.timedelta(n)

start_date = datetime.datetime(2017, 4, 22)
end_date = datetime.datetime(2017, 4, 29)

fdpts = 1
fdreb = 1.2
fdast = 1.5
fdblk = 2
fdstl = 2
fdto = -1

dkpts = 1
dk3ptm = 0.5
dkreb = 1.25
dkast = 1.5
dkstl = 2
dkblk = 2
dkto = -0.5
dkdd = 1.5
dktd = 3


for single_date in daterange(start_date, end_date):
	a = single_date.strftime("%Y")
	b = single_date.strftime("%m")
	c = single_date.strftime("%d")

	my_url = ("http://www.basketball-reference.com/friv/dailyleaders.cgi?month=" + str(b) + "&day=" + str(c) + "&year=" + str(a))

	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll("tr")
	date_container = page_soup.findAll("div",{"class":"prevnext"})
	game_date = date_container[0].span.text.strip()
	converted_date_container = datetime.datetime.strptime(game_date, '%b %d, %Y')
	converted_date = converted_date_container.strftime("%Y-%m-%d")

	if len(containers) == 0:
		continue



	header_container = containers[0].findAll("th")

	filename = ("Basketball Reference Stats.csv")

	if single_date == start_date:
		f = open(filename, "w")
		header = "year, month, day"
		for i in range(1,(len(header_container)-1)):
			header = header + "," + header_container[i].text.strip()
		header = (header + ',' + "FanDuel Points" + ',' + 'DraftKings Points' + "\n")
		f.write(header)
		f.close()
	
	f = open(filename,"a")

	for container in containers[1:(len(containers)-1)]:
		stats_container = container.findAll("td")
		stats = (a + "," + b + "," + c + ",")
		if len(stats_container) == 0:
			continue
		for i in range(len(stats_container)-1):
			stats = (stats + stats_container[i].text.strip() + ",")
		#find double/double + triple/double
		ddlist = [23,17,18,19,20]
		double_categories = 0
		dd = 0
		td = 0
		for i in ddlist:
			if len(stats_container[i].text.strip()) > 1:
				double_categories += 1
		if double_categories == 2:
			dd = 1
		if double_categories > 2:
			dd = 1
			td = 1		

		fdscore = (fdpts*int(stats_container[23].text.strip()) + fdreb*int(stats_container[17].text.strip()) + fdast*int(stats_container[18].text.strip()) + fdstl*int(stats_container[19].text.strip()) + fdblk*int(stats_container[20].text.strip()) + fdto*int(stats_container[21].text.strip()))
		dkscore = (dkpts*int(stats_container[23].text.strip()) + dkreb*int(stats_container[17].text.strip()) + dkast*int(stats_container[18].text.strip()) + fdstl*int(stats_container[19].text.strip()) + fdblk*int(stats_container[20].text.strip()) + fdto*int(stats_container[21].text.strip()) + dk3ptm*int(stats_container[9].text.strip()) + dkreb*dd + dkreb*td)
		stats = (stats + str(fdscore) + ',' + str(dkscore) + "\n")
		f.write(stats)

	f.close()