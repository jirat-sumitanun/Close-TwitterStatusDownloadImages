import urllib
import requests
from bs4 import BeautifulSoup
import os, datetime, time, math

image_count = 0
link_count = 0

def readText():
	with open("your text file here") as f: #change to your text file
    		content = f.readlines() #read text file line by line
	for link in content:
		openLink(link.rstrip('\n')) #send link to request
		global link_count
		link_count += 1
	f.close()


def openLink(url_link):
	global link_count
	try:
		url = urllib.request.urlopen(url_link).read() #open tweet's status
		soup = BeautifulSoup(url,"lxml")
		images = []
		images = soup.findAll("img") #get all images in tweet it include images in reply too
		for img in images:
			image = str(img.get("src")) # filter only images in status and reply
			if(image.find("media") > 0):
				#print(image)
				DLImage(image)
		link_count += 1
	except:
		print("404 not found on",url_link)


def DLImage(link):
	global image_count
	Photo_URL = changeToOrig(link) #convert images url to original size
	path = r"Download Path Here" #Change to your path
	fileName = link[link.find("media/")+6:]
	destination_path_file = path+fileName
	if os.path.isfile(destination_path_file):
		print(fileName, "already downloaded")
	else:
		Picture_request = requests.get(Photo_URL)
		try:
			if Picture_request.status_code == 200:
				with open(destination_path_file, 'wb') as f:
					f.write(Picture_request.content) #download image
				print("Download:",fileName)
				image_count += 1
		except:
			print("404 not found on",Photo_URL)


def changeToOrig(link):
	if(link.find(".png") != -1):
		ext = "?format=png&name=orig"
		origLink = link[0:link.find(".png")] + ext
	elif(link.find(".jpg") != -1):
		ext = "?format=jpg&name=orig"
		origLink = link[0:link.find(".jpg")] + ext
	#print(origLink)
	return origLink

def main():
	start = time.time()
	readText()
	print("\nDownload {} Images from {} Link\n".format(image_count,link_count))
	end = time.time()
	#print(end - start,'Sec')
	second = end - start
	m, s = divmod(math.ceil(second), 60)
	print('Use {:02d} Minutes {:02d} Second'.format(m, s))
	input('Hit Enter to close.....')
if __name__ == "__main__":
    main()
