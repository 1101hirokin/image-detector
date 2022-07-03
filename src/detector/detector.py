from posixpath import abspath
from exceptions import exceptions
from const import const

import tempfile
import os
import re
import cv2
import requests
import bs4
import imgsim

import urllib
from urllib.request import urlopen
from urllib.parse import urljoin

const.SIMILARITY_THRESHOLD: float = 5.0
const.SVG_REGEX: str = r'(?:<\?xml\b[^>]*>[^<]*)?(?:<!--.*?-->[^<]*)*(?:<svg|<!DOCTYPE svg)\b'
COMPILED_SVG_REGEX: re.Pattern[str] = re.compile(const.SVG_REGEX)
REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

def detectImageInWebsite(url: str, filePath: str) -> bool:
	if _isSupportable(filePath): return False

	targetImage: cv2.Mat = cv2.imread(filePath)
	if targetImage is None:
		print(filePath+ " is not found :(")
		return False
	fileName: str = os.path.basename(filePath)
	
	vectorizer:imgsim.Vectorizer = imgsim.Vectorizer()
	targetVec = vectorizer.vectorize(targetImage)

	res: requests.Response = requests.get(url, headers=REQUEST_HEADERS)
	print("requested "+url+" and responded code was "+str(res.status_code))
	if 400 <= res.status_code | res.status_code < 500:
		return False
	
	text: str = res.text
	
	soup: bs4.BeautifulSoup = bs4.BeautifulSoup(text, "html.parser")
	
	# list up images by fileName and check similarity
	pattern: str = f'"^(?=.*"{fileName}).*$'
	imgTagResultSet: bs4.ResultSet = soup.find_all(
		name='img',
	)

	putOffSrcs: list[str] = []
	for imgTagResult in imgTagResultSet:
		src: str = imgTagResult["src"]
		absPath: str = urljoin(url ,src)
		
		if re.search(pattern, absPath) is None:
			putOffSrcs.append(absPath)
			continue

		print(absPath)
		if not _isSupportable(absPath):
			continue
		if _checkDistance(vectorizer, targetVec, absPath):
			return True
	
	for absPath in putOffSrcs:
		print(absPath)
		if not _isSupportable(absPath):
			continue
		if _checkDistance(vectorizer, targetVec, absPath):
			return True

	return False

def _imreadFromWeb(absPath) -> cv2.Mat:
		res: requests.Response = requests.get(absPath, headers=REQUEST_HEADERS)
		image: cv2.Mat | None = None
		
		with tempfile.NamedTemporaryFile(dir="./") as fp:
			fp.write(res.content)
			fp.file.seek(0)
			image = cv2.imread(fp.name)
		
		if image is not None:
			return image
		else:
			raise exceptions.LocalImreadFailedError(f"couldnot read image of {absPath}")

def _checkDistance(vectorizer: imgsim.Vectorizer ,targetVec , absPath: str) -> bool:
	try:
		image = _imreadFromWeb(absPath)
		imageVec = vectorizer.vectorize(image)

		d: float = imgsim.distance(targetVec, imageVec) # Euclidian distance between the target image and the current loop image; the closer to zero, the higher the similarity.
		print(d)
		return d <= const.SIMILARITY_THRESHOLD
	except exceptions.LocalImreadFailedError as e:
		print(e)
		return False
	except urllib.error.HTTPError as e:
		print(e)
		return False
	except urllib.error.URLError as e:
		print(e)
		return False
	except:
		print("some error has occured")
		return False

def _isSVG(absPath: str)-> bool:
	try: 
		f = urlopen(absPath)
		fileContents = f.read().decode("latin_1")
		return COMPILED_SVG_REGEX.match(fileContents) is not None
	except urllib.error.HTTPError as e:
		raise e
	except urllib.error.URLError as e:
		raise

def _isSupportable(absPath: str) -> bool:
	try:
		isSVG: bool = _isSVG(absPath)
		if isSVG:
			print("SVG is not supported")
		return not isSVG
	except urllib.error.HTTPError as e:
		print(e)
		return False
	except urllib.error.URLError as e:
		print(e)
		return False