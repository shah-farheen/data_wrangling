import os
import git
import requests
import subprocess
import fileinput
import re

gitDirectory = "/Users/farheenshah/AndroidStudioProjects/classplus"

def testSubprocess():
	a = subprocess.call(["ls -l"], stdin=None, stdout=None, stderr=None, shell=False)
	print(a)
	# print(getBody("demo"))

def test():
	command = "l" + "s"
	print(command)
	os.system(command)

def printResult(resultLabel, result):
	print("\n\n" + resultLabel + ": " + str(result) + "\n\n")

def branchStatus():
	statusResult = subprocess.call(["git", "-C", gitDirectory, "status"], stdin=None, stdout=None, stderr=None, shell=False)
	return statusResult

def checkoutBranch(orgCode, branchHeader):
	checkoutResult = subprocess.call(["git", "-C", gitDirectory, "checkout", "-b", branchHeader + orgCode, "--track", "origin/" + branchHeader + orgCode])
	return checkoutResult

def mergeBranch(parentBranch):
	mergeResult = subprocess.call(["git", "-C", gitDirectory, "merge", "--no-commit", parentBranch])
	return mergeResult

def addFilesToCommit():
	addCode = subprocess.call(["git", "-C", gitDirectory, "add", "."])
	return addCode

def commitBranch(orgCode):
	commitResult = subprocess.call(["git", "-C", gitDirectory, "commit", "-m", orgCode + ": version updated"])
	return commitResult

def pushBranch(orgCode, branchHeader):
	pushResult = subprocess.call(["git", "-C", gitDirectory, "push", "origin", branchHeader + orgCode])
	return pushResult

def resetCode():
	addResult = addFilesToCommit()
	resetResult = subprocess.call(["git", "-C", gitDirectory, "reset", "--hard"])
	return resetResult

def deleteBranch(orgCode, branchHeader):
	deleteResult = subprocess.call(["git", "-C", gitDirectory, "branch", "-d", branchHeader + orgCode])
	return deleteResult

def changeBranch(parentBranch):
	changeResult = subprocess.call(["git", "-C", gitDirectory, "checkout", parentBranch])
	return changeResult

def changeVersions(versionName):
  data = []
  with open(gitDirectory + "/app/build.gradle", "r") as file:
  	data = file.readlines()
  	# print(data[20].split(' '))
  	# print(data[21].split(' '))
  	# versionCodeLine = data[20].strip().split(' ')
  	# versionCode = int(a[1]) + 1
  	# data[20] = "        versionCode " + str(versionCode) + "\n"
  	# data[21] = '        versionName "1.0.22.1"\n'

  	for i, line in enumerate(data):
  		if "versionCode" in line:
  			versionCodeLine = data[i].strip().split(' ')
  			versionCode = int(versionCodeLine[1]) + 1
  			data[i] = "        versionCode " + str(versionCode) + "\n"
  		if "versionName" in line:
  			data[i] = '        versionName "' + versionName + '"\n'

  with open(gitDirectory + "/app/build.gradle", "w") as file:
  	file.writelines(data)
  # 
  #   for line in file:
  #     if "versionName" in line:
  #       file.write("versionName 1.0.20.1")
  #     if "versionCode" in line:
  #       a = line.strip().split(' ')
  #       code = a[1] + 1
  #       file.write("versionCode code")
  
  # with fileinput.FileInput("/Users/farheenshah/AndroidStudioProjects/classplus/app/build.gradle", inplace=True) as file:
  #   for line in file:
  #     if "versionName" in line:
  #       print(line)

  # for line in fileinput.input('/Users/farheenshah/AndroidStudioProjects/classplus/app/build.gradle', inplace=True): 
  #     if "versionCode" in line:
  #       # print(line)
  #       a = line.strip().split(' ')
  #       versionNumber = int(a[1]) + 1
  #       line.replace('versionCode ' + str(versionNumber-1), 'versionCode ' + str(versionNumber))


def makeBitriseCall(orgCode, branchHeader):
	url = "https://www.bitrise.io/app/8d0551b8d426d749/build/start.json"
	body = getBody(orgCode, branchHeader)
	headers = {'Content-Type': 'application/json'}
	response = requests.post(url, headers=headers, data=body)
	printResult("responseCode", response.status_code)


def getBody(orgCode, branchHeader):
	body = '''{
  	"hook_info":{
    "type":"bitrise",
    "api_token":"Iu22CqIaH2Ej96C2dRk7iw"
    
  	},
  	"build_params":{
    "workflow_id":"stellar_academy",
    "environments":[
      {
        "mapped_to":"BITRISEIO_ANDROID_KEYSTORE_URL", "value":"file://./app/''' + orgCode + '''.jks", "is_expand":true
      },
      {
        "mapped_to":"APP_PACKAGE_NAME", "value":"co.classplus.''' + orgCode + '''", "is_expand":true
      },
      {
        "mapped_to":"BITRISE_GIT_BRANCH","value":"''' + branchHeader + orgCode + '''","is_expand":true
        
      }
      ]
    
  	},"triggered_by":"curl"}'''
  	return body


def changeAndDeleteBranch(orgCode, branchHeader, parentBranch):
	changeResult = changeBranch(parentBranch)
	if(changeResult == 0):
		deleteBranch(orgCode, branchHeader)


def start(orgCode, versionName, branchHeader, parentBranch):
	resetResult = resetCode()
	if(resetResult != 0):
		return 1

	printResult("statusResult", branchStatus())
	printResult("checkoutResult", checkoutBranch(orgCode, branchHeader))
	mergeResult = mergeBranch(parentBranch)
	printResult("mergeResult", mergeResult)
	if(mergeResult != 0):
		return 1
	startAfterMerge(orgCode, versionName, branchHeader)
	return 0


def startAfterMerge(orgCode, versionName, branchHeader):
	changeVersions(versionName)
	printResult("gitAddCode", addFilesToCommit())
	printResult("commitResult", commitBranch(orgCode))
	printResult("pushResult", pushBranch(orgCode, branchHeader))
	makeBitriseCall(orgCode, branchHeader)	


def loopInCodes(codesList, versionName, branchHeader, parentBranch):
	success = []
	failure = []
	for code in codesList:
		finalResult = start(code, versionName, branchHeader, parentBranch)
		if(finalResult == 0):
			success.append(code)
		else:
			failure.append(code)

	resetCode()
	changeResult = changeBranch(parentBranch)
	if(changeResult == 0):
		for code in codesList:
			printResult("deleteResult", deleteBranch(code, branchHeader))		

	print("success:")
	print(success)
	print("failure:")
	print(failure)


currentVersion = "1.0.21.1"
currentOrgCode = "demo"
old1orgCodes = ["apex", "apexl", "base", "bkc", "bw", "csac", "cal", "cara", "carm", "cef", "chin", "chac", "rudra"]
old2orgCodes = ["clat", "cm", "dedu", "dtos", "dest", "disha", "dri", "eds", "evilla", "educ", "edut", "eduv", "ekl", "eedu", "elite", "ejee", "fec", "edge"]
old3orgCodes = ["gb", "gta", "grvty", "gwr", "mantra", "gyan", "hima", "hkc", "shed", "isr", "ikan", "ime", "impl", "jram", "jmd", "jp", "kic", "kgyan", "khan", "knowc"]
old4orgCodes = ["ach", "lzone", "mark", "bcc", "mmc", "mmgc", "aims", "np", "nbw", "ntc", "nkc", "osr", "pam", "pcc", "pari", "pray", "qs", "rdc", "real", "ace", "rivan", "rkg", "ruchi", "stc", "sai", "sanj", "cc", "sdk", "ssc", "shik", "shree", "skc", "eco", "spec", "ss", "sski", "stay", "demo", "sumit", "tutp", "smc", "citi", "topp", "vidya", "vector", "vin", "vkl", "vision", "wadh", "win", "zenith"]

orgCodes = ["demo", "ie", "phoenix", "reddy"]
adOrgCodes = ["arav", "alti", "arya", "dc", "edup", "kd", "kp", "gaut", "pc", "rays", "srma", "twc", "vish"]
adBranchHeader = "whitelabel_ads_"
noAdBranchHeader = "whitelabel_"
adParentBranch = "white_label_ads"
noAdParentBranch = "white_label"


# loopInCodes(orgCodes, currentVersion, noAdBranchHeader, noAdParentBranch)
# start(currentOrgCode, currentVersion, noAdBranchHeader, noAdParentBranch)
# startAfterMerge(currentOrgCode, currentVersion, noAdBranchHeader)
changeAndDeleteBranch(currentOrgCode, noAdBranchHeader, noAdParentBranch)











