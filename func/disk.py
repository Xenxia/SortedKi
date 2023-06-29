# import wmi
# import win32api, pywintypes # optional

# looking_for = "Backup Drive"
# drive_names = []
# drive_letters = []

# c = wmi.WMI()

# for drive in c.Win32_LogicalDisk ():
#     drive_names.append(str(drive.VolumeName).strip().lower())
#     drive_letters.append(str(drive.Caption).strip().lower())
#     #    below is optional
#     #    need a try catch because some drives might be empty but still show up (like D: drive with no disk inserted)
#     try:
#         if str(win32api.GetVolumeInformation(str(drive.Caption) + "\\")[0]).strip().lower() != str(drive.VolumeName).strip().lower():
#             print("Something has gone horribly wrong...")
#     except pywintypes.error:
#         pass

# if looking_for.strip().lower() not in drive_names:
#     print("The drive is not connected currently.")
# else:
#     print("The drive letter is " + str(drive_letters[drive_names.index(looking_for.strip().lower())]).upper())


# print(drive_letters)
# print(drive_names)

import wmi

DRIVE_TYPES = {
  0 : "Unknown",
  1 : "No Root Directory",
  2 : "Removable Disk",
  3 : "Local Disk",
  4 : "Network Drive",
  5 : "Compact Disc",
  6 : "RAM Disk"
}

c = wmi.WMI()
for drive in c.Win32_LogicalDisk ():
    # prints all the drives details including name, type and size
    # print(drive)
    if drive.DriveType == 2:
        pass
    print(drive.Caption, drive.VolumeName, DRIVE_TYPES[drive.DriveType], drive.VolumeSerialNumber, drive.FileSystem)
