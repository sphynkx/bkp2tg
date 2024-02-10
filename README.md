Snippet for backup system that collect some nesessary dir and files in system, creates dump of mediawiki's DB, extract one page from it. All collected files are archiving, archive split by 500Mb-volumes and send to Telegram channel to store.

## Setup
1. Place files in /opt/lahbkp for example
  chmod +x *.sh *.py
2. Install modules for Python:
  pip install -r requirements.txt
3. Go to https://my.telegram.org/apps , set new app. Set its params 'api_id' and 'api_hash' to config.ini. Next, in the Telegram client create new private channel. From channel settings take invite URL and set it to config.ini also.
4. Check is uploader connects to channel:
   ./sendtotg.py -t "Hello"
At first run the script asks for bot token or mobile number. Enter mobile associated with your Telegram account (bots cannot use some nesessary functions of Telegram API). Check message in Telegram service bot with 5-digital code. Enter this code. Now the message would be appear in channel.
5. Edit files/directory list (files.list) as you need and run backuper:
   ./lahbkp.sh
Progress would be slow.. Finally in channel would be appeared some posts with attached volumes of backups archive.
6. If everything is OK - set cron task:
   0 0 1 * * /opt/lahbkp/lahbkp.sh
