from detector import detector

def main():
	URLs = [
		"https://www.fincode.jp/",
	]

	results: dict[str, bool] = {}

	for i, url in enumerate(URLs):
		result = detector.detectImageInWebsite(url)
		results[url] = result

main()