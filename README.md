# RestoreMe
 Help Make FutureRestore Restore's Easier, Downloads SEP, Baseband, Buildmanifest and IPSW and automates the restore

Only supports 64Bit devies on iOS 14+

iPhone11,2 iOS 14+ 
iPad7,4 iOS 14+

Other devices to be added in a future update

## Usage

  -h, --help  show this help message and exit
  
  -p P        Set Custom Save Path for Downloaded Files
  
  -d          Download Restore Files Only
  
  -e          Exit Recovery Mode
  
  -u          Set Update paramater, to keep user data, do not perform FDR
  
  -t T        Set SHSH ticket used for the restore
  
  -l          Set program to print all info

## Todo 

1) Build for Linux
2) Test on Linux

When checkm8 and/or Futurerestore allow for downgrades on blackbird vulerable devices (bypassing SEP and with working Baseband Support on iPhones. iPod's and iPad's don't have a baseband unless they're cellular) them firmwares will be added for supported devices

## To Compile / Run
1) Compile futurerestore 
2) Compile libimobiledevice
3) Place 'FutureRestore, ideviceinfo, ideviceenterrecovery' in SupportFiles
4) Install python libs `pip3 / pip install -r requirements.txt`
5) compile with something like auto-py-to-exe or something similar or run with `python RestoreMe.py`

## Thanks to the following 

https://github.com/m1stadev/futurerestore

https://github.com/libimobiledevice/libimobiledevice

https://github.com/tihmstar/futurerestore

https://github.com/marijuanARM/futurerestore

https://www.theiphonewiki.com/wiki/Firmware
