import os
import xml.etree.ElementTree as ET
from lxml import etree
from PIL import Image
from resizeimage import resizeimage
import fileinput
import sys
import git
import requests
import subprocess
import re
from pathlib2 import Path

gitDirectory = "/Users/farheenshah/AndroidStudioProjects/classplus"
stringsFile = gitDirectory + "/app/src/main/res/values/strings.xml"
gradleFile = gitDirectory + "/app/build.gradle"
keystorePath = gitDirectory + "/app/"
keyPassWord = "classplus@2018"
rootImageDir = "/Users/farheenshah/Desktop/images"
resourcesDir = gitDirectory + "/app/src/main/res"

keyCommand = "keytool -genkey -v -keystore /Users/farheenshah/AndroidStudioProjects/classplus/app/orgnm.jks -keyalg RSA -keysize 2048 -validity 10000 -alias classplus -keypass classplus@2018 -storepass classplus@2018 -dname CN=Classplus"

class CommentedTreeBuilder(ET.TreeBuilder):
    def __init__(self, *args, **kwargs):
        super(CommentedTreeBuilder, self).__init__(*args, **kwargs)

    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)

def parseStrings(appName, orgId, orgCode):
	tree = ET.parse(gitDirectory + "/app/src/main/res/values/strings.xml", ET.XMLParser(target=CommentedTreeBuilder()))
	root = tree.getroot()
	for child in root:
		if child.tag == "string":
			if child.attrib["name"] == "app_name":
				child.text = appName
			if child.attrib["name"] == "classplus_org_id":
				child.text = orgId
			if child.attrib["name"] == "classplus_org_code":
				child.text = orgCode
			if child.attrib["name"] == "classplus_provider_authority":
				child.text = "co.classplus." + orgCode + ".classplus.provider"
			if child.attrib["name"] == "freshchat_file_provider_authority":
				child.text = "co.classplus." + orgCode + ".provider"
	tree.write(gitDirectory + "/app/src/main/res/values/strings.xml")

def iter(appName, orgId, orgCode):
	context = ET.iterparse(gitDirectory + "/app/src/main/res/values/strings.xml")
	for event, child in context:
		if child.tag == "string":
			if child.attrib["name"] == "app_name":
				print child.text
				child.text = appName
			if child.attrib["name"] == "classplus_org_id":
				print child.text
				child.text = orgId
			if child.attrib["name"] == "classplus_org_code":
				print child.text
				child.text = orgCode
			if child.attrib["name"] == "classplus_provider_authority":
				print child.text
				child.text = "co.classplus." + orgCode + ".classplus.provider"
			if child.attrib["name"] == "freshchat_file_provider_authority":
				print child.text
				child.text = "co.classplus." + orgCode + ".provider"
	print ET.tostring(context.root)

def tryLxml(appName, orgId, orgCode):
	tree = etree.parse(gitDirectory + "/app/src/main/res/values/strings.xml")
	root = tree.getroot()
	print root.tag
	for child in root:
		if child.tag == "string":
			if child.attrib["name"] == "app_name":
				child.text = appName
			if child.attrib["name"] == "classplus_org_id":
				child.text = orgId
			if child.attrib["name"] == "classplus_org_code":
				child.text = orgCode
			if child.attrib["name"] == "classplus_provider_authority":
				child.text = "co.classplus." + orgCode + ".classplus.provider"
			if child.attrib["name"] == "freshchat_file_provider_authority":
				child.text = "co.classplus." + orgCode + ".provider"
	tree.write(gitDirectory + "/app/src/main/res/values/strings.xml")

def editStrings(filename, appName, orgId, orgCode):
	for line in fileinput.input(filename, inplace=True):
		if "name=\"app_name\"" in line:
			line = line.replace("Classplus", appName)
			sys.stdout.write(line)
		elif "name=\"classplus_org_id\"" in line:
			line = line.replace("1", orgId)
			sys.stdout.write(line)
		elif "name=\"classplus_org_code\"" in line:
			line = line.replace("demo", orgCode)
			sys.stdout.write(line)
		elif "name=\"classplus_provider_authority\"" in line:
			line = line.replace("demo", orgCode)
			sys.stdout.write(line)
		elif "name=\"freshchat_file_provider_authority\"" in line:
			line = line.replace("demo", orgCode)
			sys.stdout.write(line)
		else:
			sys.stdout.write(line)


def editBuildGradle(filename, orgCode, versionCode, versionName):
	for line in fileinput.input(filename, inplace=True):
		if "./demo.jks" in line:
			line = line.replace("demo", orgCode)
			sys.stdout.write(line)
		elif "co.classplus.app" in line:
			line = line.replace("co.classplus.app", "co.classplus." + orgCode)
			sys.stdout.write(line)
		elif "versionCode" in line:
			line = line.replace("15", versionCode)
			sys.stdout.write(line)
		elif "versionName" in line:
			line = line.replace("1.0.15", versionName)
			sys.stdout.write(line)
		else:
			sys.stdout.write(line)

iconSizes = {
	"mipmap-xxxhdpi" : [192, 192],
	"mipmap-xxhdpi" : [144, 144],
	"mipmap-xhdpi" : [96, 96],
	"mipmap-hdpi" : [72, 72],
	"mipmap-mdpi" : [48, 48]
}

def changeIcons(imageName, rootDir, changedName):
	os.chdir(rootDir)
	with open(imageName, 'r+b') as file:
		with Image.open(file) as image:
			for directory, size in iconSizes.iteritems():
				cover = resizeimage.resize_cover(image, size)	
				# if not os.path.exists(directory):
				# 	os.makedirs(directory)
				# os.chdir(directory)
				cover.save(changedName, image.format)
				os.rename(rootDir + "/" + changedName, resourcesDir + "/" + directory + "/" + changedName)
				os.chdir(rootDir)

def moveLogoAndSlides(ic_logo_name, slide1, slide2, slide3, rootDir, destDir):
	moveImage(ic_logo_name, rootDir, destDir)
	moveImage(slide1, rootDir, destDir)
	moveImage(slide2, rootDir, destDir)
	moveImage(slide3, rootDir, destDir)

def moveImage(imageName, rootDir, destDir):
	image = Path(rootDir + "/" + imageName)
	if image.exists():
		os.rename(rootDir + "/" + imageName, destDir + "/" + imageName)
		return True
	else:
		return False


def makeBitriseCall(orgCode, branchHeader):
	url = "https://app.bitrise.io/app/8d0551b8d426d749/build/start.json"
	body = getBody(orgCode, branchHeader)
	headers = {'Content-Type': 'application/json'}
	response = requests.post(url, headers=headers, data=body)
	printResult("responseCode", response.status_code)


def getBody(orgCode, branchHeader):
	body = '''{
	"hook_info":{"type":"bitrise","api_token":"Iu22CqIaH2Ej96C2dRk7iw"},
	"build_params":{"workflow_id":"build_apk","environments":[
	  {
	      "mapped_to":"BITRISEIO_ANDROID_KEYSTORE_URL",
	        "value":"file://./app/''' + orgCode + '''.jks",
	        "is_expand":true
	        },
	        {
	        "mapped_to":"BITRISE_GIT_BRANCH",
	        "value":"''' + branchHeader + orgCode + '''",
	        "is_expand":true
	        }
	        ] 
	        },
	        "triggered_by":"curl"}'''

	return body



def printResult(resultLabel, result):
	print("\n\n" + resultLabel + ": " + str(result) + "\n\n")

def branchStatus():
	statusResult = subprocess.call(["git", "-C", gitDirectory, "status"], stdin=None, stdout=None, stderr=None, shell=False)
	return statusResult

def addFilesToCommit():
	addCode = subprocess.call(["git", "-C", gitDirectory, "add", "."])
	return addCode

def commitBranch(orgCode):
	commitResult = subprocess.call(["git", "-C", gitDirectory, "commit", "-m", orgCode + " code"])
	return commitResult

def pushBranch(orgCode, branchHeader):
	pushResult = subprocess.call(["git", "-C", gitDirectory, "push", "origin", branchHeader + orgCode])
	return pushResult

def resetCode():
	addResult = addFilesToCommit()
	resetResult = subprocess.call(["git", "-C", gitDirectory, "reset", "--hard"])
	return resetResult

def changeBranch(branchName):
	changeResult = subprocess.call(["git", "-C", gitDirectory, "checkout", branchName])
	return changeResult

def createBranch(orgCode, branchHeader):
	createResult = subprocess.call(["git", "-C", gitDirectory, "branch", branchHeader + orgCode])
	return createResult

def generateKeystore(keyPath, orgCode, password):
	keyResult = subprocess.call(["keytool", "-genkey", "-v", "-keystore", keyPath + orgCode + ".jks", "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000", "-alias", "classplus", "-keypass", password, "-storepass", password, "-dname", "CN=Classplus"])
	return keyResult


adBranchHeader = "whitelabel_ads_"
noAdBranchHeader = "whitelabel_"
adParentBranch = "white_label_ads"
noAdParentBranch = "white_label"

currentVersionCode = "1"
currentVersionName = "1.0.23.1"
currentOrgCode = "testing"
currentAppName = "Test App"
currentOrgId = "25"

def start(parentBranch, branchHeader, orgCode, appName, orgId, versionCode, versionName):
	printResult("resetResult", resetCode())
	printResult("changeResult", changeBranch(parentBranch))
	printResult("createResult", createBranch(orgCode, branchHeader))
	printResult("changeResult", changeBranch(branchHeader + orgCode))
	editStrings(stringsFile, appName, orgId, orgCode)
	editBuildGradle(gradleFile, orgCode, versionCode, versionName)
	printResult("keyResult", generateKeystore(keystorePath, orgCode, keyPassWord))
	changeIcons("logo.png", rootImageDir, "ic_launcher.png")
	moveLogoAndSlides("ic_logo_full.png", "intro_1.png", "intro_2.png", "intro_3.png", rootImageDir, resourcesDir + "/drawable-xxxhdpi")
	printResult("gitAddCode", addFilesToCommit())
	printResult("commitResult", commitBranch(orgCode))
	printResult("pushResult", pushBranch(orgCode, branchHeader))
	makeBitriseCall(orgCode, branchHeader)


start(noAdParentBranch, noAdBranchHeader, currentOrgCode, currentAppName, currentOrgId, currentVersionCode, currentVersionName)
# start(adParentBranch, adBranchHeader, currentOrgCode, currentAppName, currentOrgId, currentVersionCode, currentVersionName)












