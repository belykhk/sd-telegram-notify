# Simple notification scripts for Manage Engine Service Desk - Telegram
Notifications from ManageEngine Service Desk tickets to telegram chats and personal notifications about replies with SOCKS proxy support

### Examples
Sending messages to group chat with short info about new ticket:

![Group Messages](https://i.imgur.com/pmVXxFI.jpg)

Personal notifications of new replies:

![Personal notifications](https://i.imgur.com/c1pjSXS.jpg)

### Preparations
Scripts is designed to work with **Python 2.7** (sorry, no Python 3 support). You can check which version you have by running:
```
python -V
>Python 2.7.14
```

You also need install additional modules, this is **required** for operation.
```
pip install requests
pip install pysocks
```

### Installation & Configuraion
 - Clone repo to your local machine
```
git clone https://github.com/belykhk/sd-telegram-notify
```
 - Copy `settings-example.py` to `settings.py` and edit `settings.py` for youself
 - Put `Posttotg.py`, `Posttotgpersonal.py` and `settings.py` to
```
{ManageEngineSDInstallDir}/integration/custom_scripts/
```
 - Edit your settings in Service Desk in Custom scripts menu. Something like that:
 
Send message to group chat then ticket is created:
![Send to group chat](https://i.imgur.com/lxzhTXg.png)
Send personal message then reply from author received:
![Send personal notifications](https://i.imgur.com/MwVyHPS.png)

___

You can find additional info [here](https://medium.com/@gofys_/%D0%BE%D0%BF%D0%BE%D0%B2%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B8%D0%B7-manageengine-service-desk-plus-%D0%B2-telegram-5d3be05b56e2) (Russian)
