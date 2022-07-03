from ast import arg
from detector import detector
import sys

def main():
	args: list[str] = sys.argv
	if len(args) < 2:
		print("You must specify the file path in the first argument.")
		return
	elif len(args) > 3:
		print("You must specify only 1 argument.")
		return

	filePath: str = args[1]

	URLs: list[str]  = [
		"https://www.fincode.jp/",
		"https://insider.10bace.com/",
		"https://obenkyolab.com/?p=3330",
		"https://www.google.com/search?q=%E3%83%99%E3%82%AF%E3%83%88%E3%83%AB%E9%96%93%E8%B7%9D%E9%9B%A2+%E8%8B%B1%E8%AA%9E",
	]

	results: dict[str, bool] = {}

	for _, url in enumerate(URLs):
		result = detector.detectImageInWebsite(url, filePath)
		results[url] = result
		print(f'{url}: {result}')


main()