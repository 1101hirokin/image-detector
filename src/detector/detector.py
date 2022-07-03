import requests
import bs4


def detectImageInWebsite(url: str, fileName: str) -> bool:

	res: requests.Response = requests.get(url)
	text: str = res.text
	
	soup: bs4.BeautifulSoup = bs4.BeautifulSoup(text, "html.parser")
	
	# list up images by fileName and check similarity
	imgTagResultSet: bs4.ResultSet = soup.find_all(
		name="img",
	)
	for imgTagResult in imgTagResultSet:
		

	return False