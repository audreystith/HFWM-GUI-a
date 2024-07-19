from pipython import GCSDevice
with GCSDevice() as pidevice:
    pidevice.InterfaceSetupDlg()
    print('connected: {}'.format(pidevice.qIDN().strip()))
from pipython import GCSDevice
with GCSDevice() as pidevice:
    pidevice.InterfaceSetupDlg('MyTest')
    print('connected: {}'.format(pidevice.qIDN().strip()))