import requests
import subprocess
import plistlib

gitDirectory = "/Users/farheenshah/XcodeProjects/ios-v2"
plistFile = gitDirectory + "/XPrepV2/XPrepV2/info.plist"

OnlyBundleVersionUpdate = "OnlyBundleVersionUpdate"
ProvisioningProfileName = "ProvisioningProfileName"
CertificateName = "CertificateName"
AccountUserEmail = "AccountUserEmail"
AccountUserPassword = "AccountUserPassword"

orgsMeta = {
	"arav" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios13@gmail.com", AccountUserPassword : "Classplus@123"},

	"chac" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios12@gmail.com", AccountUserPassword : "Classplus@123"},

	"aims" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios10@gmail.com", AccountUserPassword : "Classplus@123"},

	"vkl" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios1@gmail.com", AccountUserPassword : "Classplus@123"},

	"tul" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios2@gmail.com", AccountUserPassword : "Classplus@123"},

	"asc" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios3@gmail.com", AccountUserPassword : "Classplus@123"},

	"shub" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios4@gmail.com", AccountUserPassword : "Classplus@123"},

	"rivan" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios9@gmail.com", AccountUserPassword : "Classplus@123"},

	"clat" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios11@gmail.com", AccountUserPassword : "Classplus@123"},

	"pray" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios14@gmail.com", AccountUserPassword : "Classplus@123"},

	"sumit" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios15@gmail.com", AccountUserPassword : "Classplus@123"},

	"vision" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios16@gmail.com", AccountUserPassword : "Classplus@123"},

	"gca" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios17@gmail.com", AccountUserPassword : "Classplus@123"},

	"kic" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios18@gmail.com", AccountUserPassword : "Classplus@123"},

	"apexl" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios19@gmail.com", AccountUserPassword : "Classplus@123"},

	"tch" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios20@gmail.com", AccountUserPassword : "Classplus@123"},

	"saar" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios21@gmail.com", AccountUserPassword : "Classplus@123"},

	"c2e" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios22@gmail.com", AccountUserPassword : "Classplus@123"},

	"orgnm" : { OnlyBundleVersionUpdate : False,
			   AccountUserEmail : "classplusios23@gmail.com", AccountUserPassword : "Classplus@123"}
}

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

def getBody(orgCode, branchHeader):
	body = '''{
  	"hook_info":{
    "type":"bitrise",
    "build_trigger_token":"IZ1V88S8eutzcJ-pBEYBMg"
    
  	},
  	"build_params":{
    "branch":"''' + branchHeader + orgCode + '''",
    "environments":[
      {
        "mapped_to":"ProvisioningProfileName", "value":"''' + orgCode + '''.mobileprovision", "is_expand":true
      },
      {
        "mapped_to":"CertificateName", "value":"''' + orgCode + '''.p12", "is_expand":true
      },
      {
        "mapped_to":"AccountUserEmail","value":"''' + orgsMeta[orgCode][AccountUserEmail] + '''","is_expand":true
      },
      {
        "mapped_to":"AccountUserPassword","value":"''' + orgsMeta[orgCode][AccountUserPassword] + '''","is_expand":true
      }
      ]
    
  	},"triggered_by":"curl"}'''
  	return body

def makeBitriseCall(orgCode, branchHeader):
	url = "https://app.bitrise.io/app/161745b57226d7f8/build/start.json"
	body = getBody(orgCode, branchHeader)
	headers = {'Content-Type': 'application/json'}
	response = requests.post(url, headers=headers, data=body)
	printResult("responseCode", response.status_code)

def updateShortVerion(plistDict):
	shortVersion = plistDict["CFBundleShortVersionString"]
	shortVersionArray = shortVersion.split(".")
	shortVersionArray[2] = int(shortVersionArray[2]) + 1
	shortVersion = shortVersionArray[0] + "." + shortVersionArray[1] + "." + str(shortVersionArray[2])
	plistDict["CFBundleShortVersionString"] = shortVersion
	updateBundleVersion(plistDict, True)

def updateBundleVersion(plistDict, toReset):
	if toReset == True:
		plistDict["CFBundleVersion"] = "1.0"
	elif toReset == False:
		bundleVersion = plistDict["CFBundleVersion"]
		bundleVersionArray = bundleVersion.split(".")
		bundleVersionArray[1] = int(bundleVersionArray[1]) + 1
		bundleVersion = bundleVersionArray[0] + "." + str(bundleVersionArray[1])
		plistDict["CFBundleVersion"] = bundleVersion

def editPlist(fileName, onlyUpdateBundleVersion):
	plistDict = plistlib.readPlist(fileName)
	if onlyUpdateBundleVersion == True:
		updateBundleVersion(plistDict, False)
	elif onlyUpdateBundleVersion == False:
		updateShortVerion(plistDict)
	plistlib.writePlist(plistDict, fileName)

def startAfterMerge(orgCode, branchHeader, parentBranch):
	editPlist(plistFile, orgsMeta[orgCode][OnlyBundleVersionUpdate])
	printResult("gitAddCode", addFilesToCommit())
	printResult("commitResult", commitBranch(orgCode))
	printResult("pushResult", pushBranch(orgCode, branchHeader))
	makeBitriseCall(orgCode, branchHeader)
	resetCode()
	changeResult = changeBranch(parentBranch)
	if(changeResult == 0):
		printResult("deleteResult", deleteBranch(orgCode, branchHeader))

def start(orgCode, branchHeader, parentBranch):
	resetResult = resetCode()
	if(resetResult != 0):
		return 1

	printResult("statusResult", branchStatus())
	printResult("checkoutResult", checkoutBranch(orgCode, branchHeader))
	mergeResult = mergeBranch(parentBranch)
	printResult("mergeResult", mergeResult)
	if(mergeResult != 0):
		return 1
	startAfterMerge(orgCode, branchHeader, parentBranch)
	return 0

# orgDict is just a dictionary or list of orgCodes 
def loopInCodes(orgDict, branchHeader, parentBranch):
	success = []
	failure = []
	for org in orgDict:
		finalresult = start(org, branchHeader, parentBranch)
		if finalresult == 0:
			success.append(org)
		else:
			failure.append(org)

	print("success:")
	print success
	print("failure:")
	print failure

currentBranchHeader = "whitelabel_"
currentParentBranch = "white_label"
currentOrgCode = "arav"
fewOrgs = ["arav"]

# loopInCodes(orgsMeta, currentBranchHeader, currentParentBranch)
# start(currentOrgCode, currentBranchHeader, currentParentBranch)
# print getBody(currentOrgCode, currentBranchHeader)
# editPlist(plistFile, True)
# pl = plistlib.readPlist(plistFile)
# print pl["CFBundleShortVersionString"]
# makeBitriseCall("light", "a")
