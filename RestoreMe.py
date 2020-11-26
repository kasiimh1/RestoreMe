import sys, os, argparse, glob, argparse, subprocess, json, requests, os.path
from sys import platform
from remotezip import RemoteZip

frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = sys._MEIPASS 
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(bundle_dir + '/SupportFiles/')

with open('devices.json') as json_file:
    data = json.load(json_file)

def download(url, path, version, product, log):
    try:
        os.mkdir(path)
    except OSError:
        if log:
            print ("\nCreation of the directory %s failed (might already exist)" % path)
    else:
        if log:
            print ("\nSuccessfully created the directory %s " % path)

    ipsw = path + "/" + product + "_" + version + ".ipsw"
    if not os.path.isfile(ipsw):
        with open(path + "/" + product + "_" + version + ".ipsw", 'wb') as f:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')
            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50*downloaded/total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                    sys.stdout.flush()
        sys.stdout.write('\n')
    else:
        if log:
            print("\n[*] IPSW already exists for " + product + " on iOS " + version + " at path: %s" %ipsw)

def deviceExtractionTool(binaryName, stripValue, grepValue, replace):
    if platform != "Windows":
        command = binaryName + ' | grep ' + grepValue
    if platform == "Windows":
        command = binaryName + ' | findstr ' + grepValue
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')
    output = process.communicate()
    stdOutput, stdErrValue = output
    stdOutput = stdOutput.strip()
    stdOutput = stdOutput[stripValue:]
    if replace == True:
        stdOutput = stdOutput.replace(' ', '')
    return dataReturn(stdOutput, stdErrValue)

def dataReturn(output, error):
    ret = None
    if error != None:
        ret = error
    if output != None:
        ret = output       
    return ret

def signedVersionChecker(model, version, log):
    ret = None
    signedReq = requests.get("https://api.ipsw.me/v4/device/" + model + "?type=ipsw")
    if log:
        print("\n-- Checking Currently Signed iOS Versions --")
        print("[A] IPSW.me API Response Code: ["+ str(signedReq.status_code) + "]")
    if signedReq.status_code == 200:
        print("-- Server Response --")
        api = json.loads(signedReq.text)
        apiLength = len(api['firmwares'])
        for i in range(apiLength):
            if api['firmwares'][i]['signed'] == True or version == None and api['firmwares'][i]['signed'] == True:
                print("[V] iOS", api['firmwares'][i]['version'], "is currently being signed for the:", api['identifier'])
                ret = api['firmwares'][i]['version']
    return ret

def deviceLookup(product, version):
    try:
        if data['Devices'][product]['Firmwares'][0][version] != None:
            print("\n-- IPSW found for you version, downloading --\n ", data['Devices'][product]['Firmwares'][0][version][0]['IPSW'])
            return(str(data['Devices'][product]['Firmwares'][0][version][0]['IPSW']))
        else:
            print("\n-- No IPSW found for your version --")
    except: 
        return("[E] Either we couldn't find the IPSW for your device or couldn't connect to device, please try again!")

def restoreFileFetch(product, signed, homePath):
    with RemoteZip(data['Devices'][product]['Firmwares'][0][signed][0]['IPSW']) as zip:
        print("\nDownloading, SEP, Baseband and Buildmanifest")
        zip.extract('BuildManifest.plist', homePath)    
        zip.extract(data['Devices'][product]['Firmwares'][0][signed][0]['SEP'], homePath)     
        try:   
            zip.extract(data['Devices'][product]['Firmwares'][0][signed][0]['Baseband'], homePath)    
        except:
            print("\n-- Device does not have a baseband.. fine if device is an iPad/iPod --\n")
            
parser = argparse.ArgumentParser(description='RestoreMe: FutureRestore Helper Util by Kasiimh1')
parser.add_argument('-p', help='Set Custom Save Path for Downloaded Files', default=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop//RestoreMe'))
parser.add_argument('-t', help='Set SHSH ticket used for the restore')
parser.add_argument('-l', help='Set program to print all info', action='store_true')
args = parser.parse_args()

print('\nRestoreMe v1.0 by Kasiimh1\n')

input('[*] Press ENTER when Device is connected > ')
if platform == "Windows":
    try:
        udid = deviceExtractionTool('ideviceinfo.exe', 16, 'UniqueDeviceID: ', False)
        ecid = deviceExtractionTool('ideviceinfo.exe', 13, 'UniqueChipID: ', True)
        platform = deviceExtractionTool('ideviceinfo.exe', 18, 'HardwarePlatform: ', False)
        product = deviceExtractionTool('ideviceinfo.exe', 13, 'ProductType: ', False)
        user = deviceExtractionTool('ideviceinfo.exe', 12, 'DeviceName: ', False)
        boardid = deviceExtractionTool('ideviceinfo.exe', 15, 'HardwareModel: ', False)
    except:
        print("Unabled to query device info")
if platform != "Windows":
    try:
        udid = deviceExtractionTool('ideviceinfo', 16, 'UniqueDeviceID: ', False)
        ecid = deviceExtractionTool('ideviceinfo', 13, 'UniqueChipID: ', True)
        platform = deviceExtractionTool('ideviceinfo', 18, 'HardwarePlatform: ', False)
        product = deviceExtractionTool('ideviceinfo', 13, 'ProductType: ', False)
        user = deviceExtractionTool('ideviceinfo', 12, 'DeviceName: ', False)
        boardid = deviceExtractionTool('ideviceinfo', 15, 'HardwareModel: ', False)
    except:
        print("Unabled to query device info")
        sys.exit(-1)
if args.l:
    print("\n[*] Fetching Infromation From Device")                
    print("-- Device Information --")                
    print('[D] Found ' + user)
    print('[D] Device is:', product)
    print('[D] BoardID is:', boardid)
    print('[D] Found Device: UDID:', udid)
    print('[D] ECID:', ecid)
    print('[D] Device Platform:', platform) 

version = input("[*] enter iOS version you will be futurerestoring to: ")
signed = signedVersionChecker(product, version, args.l)
download(deviceLookup(product, version), args.p, version, product, args.l)
restoreFileFetch(product, signed, args.p)

buildManifest = args.p + "/BuildManifest.plist"
sep = glob.glob(os.path.join(args.p + "/Firmware/all_flash", f'sep-firmware.*.RELEASE.im4p'))
baseband = glob.glob(os.path.join(args.p + "/Firmware" , f'*.Release.bbfw'))
ipsw = args.p + "/" + product + "_" + version + ".ipsw"

if args.t == None:
    args.t = input("Enter path to SHSH Ticket for the device you wish to restore")
if product.find("iPad") == True:
    print("[*] No Baseband set, adding no-baseband flag to the restore")
proceed = input("No Baseband provided, Continue with the Restore (fine for iPod and iPad) ? y/n: ").lower().strip()

if platform == "Windows":
    fr = "futurerestore.exe"
if platform != "Windows":
    fr = "futurerestore"

if proceed == 'y':
    print("[DEBUG] futurerestore.exe -w -t %s " %args.t + "-m %s " %buildManifest + "-p %s " %buildManifest + "-s %s " %sep[0] + "--no-baseband")
    os.system("%s" %fr + " -w -t %s " %args.t + "-m %s " %buildManifest + "-p %s " %buildManifest + "-s %s " %sep[0] + "--no-baseband")
if proceed == 'n':
    print("User didn't wish to proceed with the restore, Exiting")
    sys.exit(-1)
else:
    print("[DEBUG] futurerestore.exe -w -t %s " %args.t + "-m %s " %buildManifest + "-p %s " %buildManifest + "-s %s " %sep[0] + "-b %s " %baseband)
    os.system("%s" %fr + " -w -t %s " %args.t + "-m %s " %buildManifest + "-p %s " %buildManifest + "-s %s " %sep[0] + "-b %s " %baseband)