"""Issues from users"""

from datetime import datetime
from json import loads
import logging
from types import MappingProxyType
from typing import Final
from async_reolink.api.network.typings import LinkTypes
from async_reolink.api.commands import CommandRequest
from async_reolink.rest.commands import CommandResponse
from async_reolink.rest import system, network, ptz, ai, alarm
from .models import MockConnection

_JSON: Final = MappingProxyType(
    {
        "int5": '[{"cmd": "GetAbility", "code": 0, "value": {"Ability": {"3g": {"permit": 0, "ver": 0}, "abilityChn": [{"aiTrack": {"permit": 0, "ver": 0}, "aiTrackDogCat": {"permit": 0, "ver": 0}, "alarmAudio": {"permit": 0, "ver": 0}, "alarmIoIn": {"permit": 0, "ver": 0}, "alarmIoOut": {"permit": 0, "ver": 0}, "alarmMd": {"permit": 6, "ver": 1}, "alarmRf": {"permit": 0, "ver": 0}, "batAnalysis": {"permit": 0, "ver": 0}, "battery": {"permit": 0, "ver": 0}, "cameraMode": {"permit": 6, "ver": 0}, "disableAutoFocus": {"permit": 6, "ver": 1}, "enc": {"permit": 6, "ver": 1}, "floodLight": {"permit": 0, "ver": 0}, "ftp": {"permit": 6, "ver": 6}, "image": {"permit": 6, "ver": 1}, "indicatorLight": {"permit": 0, "ver": 0}, "isp": {"permit": 6, "ver": 1}, "isp3Dnr": {"permit": 0, "ver": 0}, "ispAntiFlick": {"permit": 6, "ver": 1}, "ispBackLight": {"permit": 0, "ver": 0}, "ispBright": {"permit": 6, "ver": 1}, "ispContrast": {"permit": 6, "ver": 1}, "ispDayNight": {"permit": 6, "ver": 1}, "ispExposureMode": {"permit": 0, "ver": 0}, "ispFlip": {"permit": 6, "ver": 1}, "ispHue": {"permit": 0, "ver": 0}, "ispMirror": {"permit": 6, "ver": 1}, "ispSatruation": {"permit": 6, "ver": 1}, "ispSharpen": {"permit": 6, "ver": 1}, "ispWhiteBalance": {"permit": 6, "ver": 0}, "ledControl": {"permit": 6, "ver": 1}, "live": {"permit": 4, "ver": 1}, "mainEncType": {"permit": 0, "ver": 1}, "mask": {"permit": 6, "ver": 1}, "mdTriggerAudio": {"permit": 0, "ver": 0}, "mdTriggerRecord": {"permit": 0, "ver": 0}, "mdWithPir": {"permit": 0, "ver": 0}, "osd": {"permit": 6, "ver": 1}, "powerLed": {"permit": 0, "ver": 0}, "ptzCtrl": {"permit": 7, "ver": 2}, "ptzDirection": {"permit": 1, "ver": 0}, "ptzPatrol": {"permit": 0, "ver": 0}, "ptzPreset": {"permit": 0, "ver": 0}, "ptzTattern": {"permit": 0, "ver": 0}, "ptzType": {"permit": 0, "ver": 1}, "recCfg": {"permit": 6, "ver": 1}, "recDownload": {"permit": 6, "ver": 1}, "recReplay": {"permit": 6, "ver": 1}, "recSchedule": {"permit": 6, "ver": 2}, "shelterCfg": {"permit": 6, "ver": 1}, "snap": {"permit": 6, "ver": 1}, "supportAi": {"permit": 6, "ver": 1}, "supportAiAnimal": {"permit": 0, "ver": 0}, "supportAiDetectConfig": {"permit": 6, "ver": 1}, "supportAiDogCat": {"permit": 6, "ver": 1}, "supportAiFace": {"permit": 0, "ver": 0}, "supportAiPeople": {"permit": 6, "ver": 1}, "supportAiSensitivity": {"permit": 6, "ver": 1}, "supportAiStayTime": {"permit": 6, "ver": 1}, "supportAiTargetSize": {"permit": 6, "ver": 1}, "supportAiTrackClassify": {"permit": 0, "ver": 0}, "supportAiVehicle": {"permit": 6, "ver": 1}, "supportAoAdjust": {"permit": 0, "ver": 0}, "supportFLBrightness": {"permit": 0, "ver": 0}, "supportFLIntelligent": {"permit": 0, "ver": 0}, "supportFLKeepOn": {"permit": 0, "ver": 0}, "supportFLSchedule": {"permit": 0, "ver": 0}, "supportFLswitch": {"permit": 0, "ver": 0}, "supportGop": {"permit": 0, "ver": 1}, "supportMd": {"permit": 6, "ver": 1}, "supportPtzCheck": {"permit": 0, "ver": 0}, "supportThresholdAdjust": {"permit": 6, "ver": 1}, "supportWhiteDark": {"permit": 6, "ver": 1}, "videoClip": {"permit": 6, "ver": 2}, "waterMark": {"permit": 6, "ver": 1}, "white_balance": {"permit": 6, "ver": 0}}], "alarmAudio": {"permit": 0, "ver": 0}, "alarmDisconnet": {"permit": 6, "ver": 1}, "alarmHddErr": {"permit": 6, "ver": 1}, "alarmHddFull": {"permit": 6, "ver": 1}, "alarmIpConflict": {"permit": 6, "ver": 1}, "auth": {"permit": 6, "ver": 1}, "autoMaint": {"permit": 6, "ver": 1}, "cloudStorage": {"permit": 0, "ver": 0}, "customAudio": {"permit": 0, "ver": 0}, "dateFormat": {"permit": 6, "ver": 1}, "ddns": {"permit": 6, "ver": 9}, "ddnsCfg": {"permit": 6, "ver": 1}, "devInfo": {"permit": 4, "ver": 1}, "devName": {"permit": 6, "ver": 2}, "disableAutoFocus": {"permit": 6, "ver": 1}, "disk": {"permit": 0, "ver": 0}, "display": {"permit": 6, "ver": 1}, "email": {"permit": 6, "ver": 3}, "emailInterval": {"permit": 6, "ver": 1}, "emailSchedule": {"permit": 6, "ver": 1}, "exportCfg": {"permit": 4, "ver": 0}, "ftpAutoDir": {"permit": 6, "ver": 1}, "ftpExtStream": {"permit": 6, "ver": 1}, "ftpPic": {"permit": 0, "ver": 0}, "ftpSubStream": {"permit": 6, "ver": 1}, "ftpTest": {"permit": 6, "ver": 0}, "hourFmt": {"permit": 6, "ver": 2}, "http": {"permit": 6, "ver": 3}, "httpFlv": {"permit": 6, "ver": 1}, "https": {"permit": 6, "ver": 3}, "importCfg": {"permit": 1, "ver": 0}, "ipcManager": {"permit": 6, "ver": 1}, "ledControl": {"permit": 7, "ver": 1}, "localLink": {"permit": 6, "ver": 1}, "log": {"permit": 6, "ver": 1}, "mediaPort": {"permit": 6, "ver": 1}, "ntp": {"permit": 6, "ver": 1}, "online": {"permit": 6, "ver": 1}, "onvif": {"permit": 6, "ver": 3}, "p2p": {"permit": 6, "ver": 1}, "performance": {"permit": 4, "ver": 1}, "pppoe": {"permit": 6, "ver": 0}, "push": {"permit": 6, "ver": 1}, "pushSchedule": {"permit": 6, "ver": 1}, "reboot": {"permit": 1, "ver": 1}, "recExtensionTimeList": {"permit": 6, "ver": 1}, "recOverWrite": {"permit": 6, "ver": 1}, "recPackDuration": {"permit": 6, "ver": 0}, "recPreRecord": {"permit": 6, "ver": 1}, "restore": {"permit": 1, "ver": 1}, "rtmp": {"permit": 6, "ver": 3}, "rtsp": {"permit": 6, "ver": 3}, "scheduleVersion": {"permit": 6, "ver": 1}, "sdCard": {"permit": 6, "ver": 1}, "showQrCode": {"permit": 6, "ver": 0}, "simMoudule": {"permit": 6, "ver": 0}, "supportAudioAlarm": {"permit": 0, "ver": 0}, "supportAudioAlarmEnable": {"permit": 0, "ver": 0}, "supportAudioAlarmSchedule": {"permit": 0, "ver": 0}, "supportAudioAlarmTaskEnable": {"permit": 0, "ver": 0}, "supportBuzzer": {"permit": 0, "ver": 0}, "supportBuzzerEnable": {"permit": 0, "ver": 0}, "supportBuzzerTask": {"permit": 0, "ver": 0}, "supportBuzzerTaskEnable": {"permit": 0, "ver": 0}, "supportEmailEnable": {"permit": 6, "ver": 1}, "supportEmailTaskEnable": {"permit": 6, "ver": 1}, "supportFtpCoverPicture": {"permit": 6, "ver": 1}, "supportFtpCoverVideo": {"permit": 6, "ver": 1}, "supportFtpDirYM": {"permit": 6, "ver": 1}, "supportFtpEnable": {"permit": 6, "ver": 1}, "supportFtpPicCaptureMode": {"permit": 6, "ver": 1}, "supportFtpPicResoCustom": {"permit": 6, "ver": 0}, "supportFtpPictureSwap": {"permit": 6, "ver": 1}, "supportFtpTask": {"permit": 6, "ver": 1}, "supportFtpTaskEnable": {"permit": 6, "ver": 1}, "supportFtpVideoSwap": {"permit": 6, "ver": 1}, "supportFtpsEncrypt": {"permit": 6, "ver": 1}, "supportHttpEnable": {"permit": 6, "ver": 1}, "supportHttpsEnable": {"permit": 6, "ver": 1}, "supportOnvifEnable": {"permit": 6, "ver": 1}, "supportPushInterval": {"permit": 6, "ver": 1}, "supportRecScheduleEnable": {"permit": 6, "ver": 1}, "supportRecordEnable": {"permit": 6, "ver": 1}, "supportRtmpEnable": {"permit": 6, "ver": 1}, "supportRtspEnable": {"permit": 6, "ver": 1}, "talk": {"permit": 4, "ver": 0}, "time": {"permit": 6, "ver": 2}, "tvSystem": {"permit": 6, "ver": 0}, "upgrade": {"permit": 1, "ver": 2}, "upnp": {"permit": 6, "ver": 1}, "user": {"permit": 6, "ver": 1}, "videoClip": {"permit": 6, "ver": 2}, "wifi": {"permit": 0, "ver": 0}, "wifiTest": {"permit": 6, "ver": 0}}}}, {"cmd": "GetTime", "code": 0, "value": {"Dst": {"enable": 1, "endHour": 2, "endMin": 59, "endMon": 4, "endSec": 0, "endWeek": 1, "endWeekday": 0, "offset": 1, "startHour": 1, "startMin": 59, "startMon": 10, "startSec": 0, "startWeek": 1, "startWeekday": 0}, "Time": {"day": 15, "hour": 21, "hourFmt": 0, "min": 21, "mon": 9, "sec": 57, "timeFmt": "DD/MM/YYYY", "timeZone": -36000, "year": 2022}}}, {"cmd": "GetNetPort", "code": 0, "value": {"NetPort": {"httpEnable": 0, "httpPort": 80, "httpsEnable": 1, "httpsPort": 443, "mediaPort": 9000, "onvifEnable": 1, "onvifPort": 8000, "rtmpEnable": 1, "rtmpPort": 1935, "rtspEnable": 1, "rtspPort": 554}}}, {"cmd": "GetDevInfo", "code": 0, "value": {"DevInfo": {"B485": 0, "IOInputNum": 0, "IOOutputNum": 0, "audioNum": 1, "buildDay": "build 22041507", "cfgVer": "v3.1.0.0", "channelNum": 1, "detail": "IPC_523128M8MPS16AE1W0110000000", "diskNum": 1, "exactType": "IPC", "firmVer": "v3.1.0.956_22041507", "frameworkVer": 1, "hardVer": "IPC_523128M8MP", "model": "RLC-822A", "name": "Gate", "pakSuffix": "pak,paks", "serial": "XXXXXXXXXXXXXXXXXXXX", "type": "IPC", "wifi": 0}}}, {"cmd": "GetMdState", "code": 0, "value": {"state": 0}}, {"cmd": "GetAiState", "code": 0, "value": {"channel": 0, "dog_cat": {"alarm_state": 0, "support": 1}, "face": {"alarm_state": 0, "support": 0}, "people": {"alarm_state": 0, "support": 1}, "vehicle": {"alarm_state": 0, "support": 1}}}, {"cmd": "GetZoomFocus", "code": 0, "value": {"ZoomFocus": {"channel": 0, "focus": {"pos": 46}, "zoom": {"pos": 1}}}}, {"cmd": "GetAutoFocus", "code": 0, "value": {"AutoFocus": {"disable": 0}}}, {"cmd": "GetAiCfg", "code": 0, "value": {"AiDetectType": {"dog_cat": 1, "face": 0, "people": 0, "vehicle": 0}, "aiTrack": 0, "channel": 0, "trackType": {"dog_cat": 0, "face": 0, "people": 1, "vehicle": 0}}}]',
        "int9": '[{"cmd": "GetAbility", "code": 0, "value": {"Ability": {"3g": {"permit": 0, "ver": 0}, "abilityChn": [{"aiTrack": {"permit": 6, "ver": 1}, "aiTrackDogCat": {"permit": 6, "ver": 1}, "alarmAudio": {"permit": 6, "ver": 1}, "alarmIoIn": {"permit": 0, "ver": 0}, "alarmIoOut": {"permit": 0, "ver": 0}, "alarmMd": {"permit": 6, "ver": 1}, "alarmRf": {"permit": 0, "ver": 0}, "batAnalysis": {"permit": 0, "ver": 0}, "battery": {"permit": 0, "ver": 0}, "cameraMode": {"permit": 6, "ver": 0}, "disableAutoFocus": {"permit": 6, "ver": 1}, "enc": {"permit": 6, "ver": 1}, "floodLight": {"permit": 0, "ver": 0}, "ftp": {"permit": 6, "ver": 6}, "image": {"permit": 6, "ver": 1}, "indicatorLight": {"permit": 0, "ver": 0}, "isp": {"permit": 6, "ver": 1}, "isp3Dnr": {"permit": 0, "ver": 0}, "ispAntiFlick": {"permit": 6, "ver": 1}, "ispBackLight": {"permit": 0, "ver": 0}, "ispBright": {"permit": 6, "ver": 1}, "ispContrast": {"permit": 6, "ver": 1}, "ispDayNight": {"permit": 6, "ver": 1}, "ispExposureMode": {"permit": 0, "ver": 0}, "ispFlip": {"permit": 6, "ver": 1}, "ispHue": {"permit": 0, "ver": 0}, "ispMirror": {"permit": 6, "ver": 1}, "ispSatruation": {"permit": 6, "ver": 1}, "ispSharpen": {"permit": 6, "ver": 1}, "ispWhiteBalance": {"permit": 6, "ver": 0}, "ledControl": {"permit": 6, "ver": 1}, "live": {"permit": 4, "ver": 1}, "mainEncType": {"permit": 0, "ver": 0}, "mask": {"permit": 6, "ver": 1}, "mdTriggerAudio": {"permit": 0, "ver": 0}, "mdTriggerRecord": {"permit": 0, "ver": 0}, "mdWithPir": {"permit": 0, "ver": 0}, "osd": {"permit": 6, "ver": 1}, "powerLed": {"permit": 0, "ver": 0}, "ptzCtrl": {"permit": 7, "ver": 2}, "ptzDirection": {"permit": 1, "ver": 0}, "ptzPatrol": {"permit": 7, "ver": 1}, "ptzPreset": {"permit": 7, "ver": 1}, "ptzTattern": {"permit": 7, "ver": 0}, "ptzType": {"permit": 0, "ver": 2}, "recCfg": {"permit": 6, "ver": 1}, "recDownload": {"permit": 6, "ver": 1}, "recReplay": {"permit": 6, "ver": 1}, "recSchedule": {"permit": 6, "ver": 2}, "shelterCfg": {"permit": 6, "ver": 1}, "snap": {"permit": 6, "ver": 1}, "supportAi": {"permit": 6, "ver": 1}, "supportAiAnimal": {"permit": 0, "ver": 0}, "supportAiDetectConfig": {"permit": 6, "ver": 1}, "supportAiDogCat": {"permit": 6, "ver": 1}, "supportAiFace": {"permit": 0, "ver": 0}, "supportAiPeople": {"permit": 6, "ver": 1}, "supportAiSensitivity": {"permit": 6, "ver": 1}, "supportAiStayTime": {"permit": 6, "ver": 1}, "supportAiTargetSize": {"permit": 6, "ver": 1}, "supportAiTrackClassify": {"permit": 6, "ver": 1}, "supportAiVehicle": {"permit": 6, "ver": 1}, "supportAoAdjust": {"permit": 0, "ver": 1}, "supportFLBrightness": {"permit": 6, "ver": 1}, "supportFLIntelligent": {"permit": 6, "ver": 1}, "supportFLKeepOn": {"permit": 0, "ver": 0}, "supportFLSchedule": {"permit": 6, "ver": 1}, "supportFLswitch": {"permit": 6, "ver": 1}, "supportGop": {"permit": 0, "ver": 1}, "supportMd": {"permit": 6, "ver": 1}, "supportPtzCheck": {"permit": 6, "ver": 0}, "supportThresholdAdjust": {"permit": 6, "ver": 1}, "supportWhiteDark": {"permit": 6, "ver": 1}, "videoClip": {"permit": 6, "ver": 2}, "waterMark": {"permit": 6, "ver": 1}, "white_balance": {"permit": 6, "ver": 0}}], "alarmAudio": {"permit": 6, "ver": 1}, "alarmDisconnet": {"permit": 6, "ver": 1}, "alarmHddErr": {"permit": 6, "ver": 1}, "alarmHddFull": {"permit": 6, "ver": 1}, "alarmIpConflict": {"permit": 6, "ver": 1}, "auth": {"permit": 6, "ver": 1}, "autoMaint": {"permit": 6, "ver": 1}, "cloudStorage": {"permit": 0, "ver": 0}, "customAudio": {"permit": 1, "ver": 1}, "dateFormat": {"permit": 6, "ver": 1}, "ddns": {"permit": 6, "ver": 9}, "ddnsCfg": {"permit": 6, "ver": 1}, "devInfo": {"permit": 4, "ver": 1}, "devName": {"permit": 6, "ver": 2}, "disableAutoFocus": {"permit": 6, "ver": 1}, "disk": {"permit": 0, "ver": 0}, "display": {"permit": 6, "ver": 1}, "email": {"permit": 6, "ver": 3}, "emailInterval": {"permit": 6, "ver": 1}, "emailSchedule": {"permit": 6, "ver": 1}, "exportCfg": {"permit": 4, "ver": 0}, "ftpAutoDir": {"permit": 6, "ver": 1}, "ftpExtStream": {"permit": 6, "ver": 1}, "ftpPic": {"permit": 0, "ver": 0}, "ftpSubStream": {"permit": 6, "ver": 1}, "ftpTest": {"permit": 6, "ver": 0}, "hourFmt": {"permit": 6, "ver": 2}, "http": {"permit": 6, "ver": 3}, "httpFlv": {"permit": 6, "ver": 1}, "https": {"permit": 6, "ver": 3}, "importCfg": {"permit": 1, "ver": 0}, "ipcManager": {"permit": 6, "ver": 1}, "ledControl": {"permit": 7, "ver": 1}, "localLink": {"permit": 6, "ver": 1}, "log": {"permit": 6, "ver": 1}, "mediaPort": {"permit": 6, "ver": 1}, "ntp": {"permit": 6, "ver": 1}, "online": {"permit": 6, "ver": 1}, "onvif": {"permit": 6, "ver": 3}, "p2p": {"permit": 6, "ver": 1}, "performance": {"permit": 4, "ver": 1}, "pppoe": {"permit": 6, "ver": 0}, "push": {"permit": 6, "ver": 1}, "pushSchedule": {"permit": 6, "ver": 1}, "reboot": {"permit": 1, "ver": 1}, "recExtensionTimeList": {"permit": 6, "ver": 1}, "recOverWrite": {"permit": 6, "ver": 1}, "recPackDuration": {"permit": 6, "ver": 0}, "recPreRecord": {"permit": 6, "ver": 1}, "restore": {"permit": 1, "ver": 1}, "rtmp": {"permit": 6, "ver": 3}, "rtsp": {"permit": 6, "ver": 3}, "scheduleVersion": {"permit": 6, "ver": 1}, "sdCard": {"permit": 6, "ver": 1}, "showQrCode": {"permit": 6, "ver": 0}, "simMoudule": {"permit": 6, "ver": 0}, "supportAudioAlarm": {"permit": 6, "ver": 1}, "supportAudioAlarmEnable": {"permit": 6, "ver": 1}, "supportAudioAlarmSchedule": {"permit": 6, "ver": 1}, "supportAudioAlarmTaskEnable": {"permit": 6, "ver": 1}, "supportBuzzer": {"permit": 0, "ver": 0}, "supportBuzzerEnable": {"permit": 0, "ver": 0}, "supportBuzzerTask": {"permit": 0, "ver": 0}, "supportBuzzerTaskEnable": {"permit": 0, "ver": 0}, "supportEmailEnable": {"permit": 6, "ver": 1}, "supportEmailTaskEnable": {"permit": 6, "ver": 1}, "supportFtpCoverPicture": {"permit": 6, "ver": 1}, "supportFtpCoverVideo": {"permit": 6, "ver": 1}, "supportFtpDirYM": {"permit": 6, "ver": 1}, "supportFtpEnable": {"permit": 6, "ver": 1}, "supportFtpPicCaptureMode": {"permit": 6, "ver": 1}, "supportFtpPicResoCustom": {"permit": 6, "ver": 0}, "supportFtpPictureSwap": {"permit": 6, "ver": 1}, "supportFtpTask": {"permit": 6, "ver": 1}, "supportFtpTaskEnable": {"permit": 6, "ver": 1}, "supportFtpVideoSwap": {"permit": 6, "ver": 1}, "supportFtpsEncrypt": {"permit": 6, "ver": 1}, "supportHttpEnable": {"permit": 6, "ver": 1}, "supportHttpsEnable": {"permit": 6, "ver": 1}, "supportOnvifEnable": {"permit": 6, "ver": 1}, "supportPushInterval": {"permit": 6, "ver": 1}, "supportRecScheduleEnable": {"permit": 6, "ver": 1}, "supportRecordEnable": {"permit": 6, "ver": 1}, "supportRtmpEnable": {"permit": 6, "ver": 1}, "supportRtspEnable": {"permit": 6, "ver": 1}, "talk": {"permit": 4, "ver": 1}, "time": {"permit": 6, "ver": 2}, "tvSystem": {"permit": 6, "ver": 0}, "upgrade": {"permit": 1, "ver": 2}, "upnp": {"permit": 6, "ver": 1}, "user": {"permit": 6, "ver": 1}, "videoClip": {"permit": 6, "ver": 2}, "wifi": {"permit": 0, "ver": 0}, "wifiTest": {"permit": 6, "ver": 0}}}}, {"cmd": "GetTime", "code": 0, "value": {"Dst": {"enable": 1, "endHour": 1, "endMin": 59, "endMon": 10, "endSec": 0, "endWeek": 5, "endWeekday": 0, "offset": 1, "startHour": 0, "startMin": 59, "startMon": 3, "startSec": 0, "startWeek": 4, "startWeekday": 0}, "Time": {"day": 15, "hour": 0, "hourFmt": 0, "min": 52, "mon": 9, "sec": 51, "timeFmt": "DD/MM/YYYY", "timeZone": 0, "year": 2022}}}, {"cmd": "GetNetPort", "code": 0, "value": {"NetPort": {"httpEnable": 1, "httpPort": 80, "httpsEnable": 1, "httpsPort": 443, "mediaPort": 9000, "onvifEnable": 1, "onvifPort": 8000, "rtmpEnable": 1, "rtmpPort": 1935, "rtspEnable": 1, "rtspPort": 554}}}, {"cmd": "GetDevInfo", "code": 0, "value": {"DevInfo": {"B485": 0, "IOInputNum": 0, "IOOutputNum": 0, "audioNum": 1, "buildDay": "build 22041511", "cfgVer": "v3.1.0.0", "channelNum": 1, "detail": "IPC_523128M8MPS16CE1W0110000000", "diskNum": 1, "exactType": "IPC", "firmVer": "v3.1.0.956_22041511_v1.0.0.30", "frameworkVer": 1, "hardVer": "IPC_523128M8MP", "model": "RLC-823A", "name": "Frente", "pakSuffix": "pak,paks", "serial": "00000000000000", "type": "IPC", "wifi": 0}}}, {"cmd": "GetLocalLink", "code": 0, "value": {"LocalLink": {"activeLink": "LAN", "dns": {"auto": 1, "dns1": "10.10.0.3", "dns2": "10.10.0.3"}, "mac": "Mac ", "static": {"gateway": "10.10.0.1", "ip": "10.10.0.27", "mask": "255.255.255.0"}, "type": "DHCP"}}}, {"cmd": "GetP2p", "code": 0, "value": {"P2p": {"enable": 1, "uid": "UID"}}}, {"cmd": "GetMdState", "code": 0, "value": {"state": 1}}, {"cmd": "GetAiState", "code": 0, "value": {"channel": 0, "dog_cat": {"alarm_state": 0, "support": 1}, "face": {"alarm_state": 0, "support": 0}, "people": {"alarm_state": 0, "support": 1}, "vehicle": {"alarm_state": 0, "support": 1}}}, {"cmd": "GetZoomFocus", "code": 0, "value": {"ZoomFocus": {"channel": 0, "focus": {"pos": 11}, "zoom": {"pos": 0}}}}, {"cmd": "GetPtzPatrol", "code": 0, "value": {"PtzPatrol": [{"channel": 0, "enable": 0, "id": 1, "name": "cruise1", "preset": null, "running": 0}, {"channel": 0, "enable": 0, "id": 2, "name": "cruise2", "preset": null, "running": 0}, {"channel": 0, "enable": 0, "id": 3, "name": "cruise3", "preset": null, "running": 0}, {"channel": 0, "enable": 0, "id": 4, "name": "cruise4", "preset": null, "running": 0}, {"channel": 0, "enable": 0, "id": 5, "name": "cruise5", "preset": null, "running": 0}, {"channel": 0, "enable": 0, "id": 6, "name": "cruise6", "preset": null, "running": 0}]}}, {"cmd": "GetAiCfg", "code": 0, "value": {"AiDetectType": {"dog_cat": 1, "face": 0, "people": 1, "vehicle": 1}, "aiTrack": 1, "channel": 0, "trackType": {"dog_cat": 1, "face": 0, "people": 1, "vehicle": 1}}}]',
    }
)


class TestRig(MockConnection, system.System, network.Network, ptz.PTZ, ai.AI):
    """Test Rig"""

    def __init__(
        self, *args, issue: str, logger: logging.Logger = None, **kwargs
    ) -> None:
        super().__init__(*args, logger=logger, **kwargs)
        self._issue = issue

    def _execute(self, *args: CommandRequest):
        if self._logger is not None:
            self._logger.info("_execute fired")

        json: list[dict] = loads(_JSON[self._issue])

        async def _mock_iterable():
            for response in json:
                yield CommandResponse.create_from(response)

        return _mock_iterable()


async def test_int5():
    """Issue #5 from integration"""

    client = TestRig(issue="int5")

    async for response in client.batch(()):
        if isinstance(response, system.system.GetAbilitiesResponse):
            continue
        elif isinstance(response, system.system.GetTimeResponse):
            continue
        elif isinstance(response, system.system.GetDeviceInfoResponse):
            continue
        elif isinstance(response, network.network.GetNetworkPortsResponse):
            continue
        elif isinstance(response, alarm.alarm.GetMotionStateResponse):
            continue
        elif isinstance(response, ai.ai.GetAiConfigResponse):
            continue
        elif isinstance(response, ai.ai.GetAiStateResponse):
            continue
        elif isinstance(response, ptz.commands.GetAutoFocusResponse):
            continue
        elif isinstance(response, ptz.commands.GetZoomFocusResponse):
            continue
        elif isinstance(response, ai.ai.GetAiStateResponse):
            continue
        else:
            assert False


async def test_int9():
    """Issue #9 from integration"""

    client = TestRig(issue="int9")

    async for response in client.batch(()):
        if isinstance(response, system.system.GetAbilitiesResponse):
            ability = response.capabilities
            assert ability is not None
            assert ability.auth is not None
            assert ability.auth
            assert (
                ability.auth.permissions
                == system.system.capabilities.Permissions.READ
                | system.system.capabilities.Permissions.WRITE
            )
            continue
        elif isinstance(response, system.system.GetTimeResponse):
            assert isinstance(response.to_datetime(), datetime)
            continue
        elif isinstance(response, system.system.GetDeviceInfoResponse):
            info = response.info
            assert info.name == "Frente"
            continue
        elif isinstance(response, network.network.GetNetworkPortsResponse):
            ports = response.ports
            assert ports.http.enabled
            continue
        elif isinstance(response, network.network.GetLocalLinkResponse):
            local_link = response.local_link
            assert local_link.type == LinkTypes.DHCP
            continue
        elif isinstance(response, network.network.GetP2PResponse):
            info = response.info
            assert info.uid
            continue
        elif isinstance(response, alarm.alarm.GetMotionStateResponse):
            assert response.state is not None
            continue
        elif isinstance(response, ai.ai.GetAiConfigResponse):
            config = response.config
            assert config
            continue
        elif isinstance(response, ai.ai.GetAiStateResponse):
            state = response.state
            assert state
            continue
        elif isinstance(response, ai.ai.GetAiStateResponse):
            state = response.state
            assert state
            continue
        elif isinstance(response, ptz.commands.GetAutoFocusResponse):
            assert response.disabled is not None
            continue
        elif isinstance(response, ptz.commands.GetZoomFocusResponse):
            state = response.state
            assert state.focus is not None
            assert state.zoom is not None
            continue
        elif isinstance(response, ptz.commands.GetPatrolResponse):
            assert response.channel_id is not None
            patrols = response.patrols
            assert patrols is not None
            assert len(patrols) == 6
            patrol = patrols[1]
            assert patrol is not None
            assert patrol.id == 1
            presets = patrol.presets
            assert presets is not None
            assert len(presets) == 0
            continue
        else:
            assert False
