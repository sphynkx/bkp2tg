#!/bin/sh

SYSBKPDIR=/var/www/wiki/_sysbkp
TOUPLOAD=/opt/toupload
APPDIR=$(dirname $0)
NOW=$(date +"%Y-%m-%d")

## 1. Collect nessesary system files
mkdir -p $SYSBKPDIR
mkdir -p $TOUPLOAD
rsync -rR --files-from=$APPDIR/files.list /  $SYSBKPDIR

## 2. Get Technote wikipage and some info about wiki
php /var/www/wiki/maintenance/dumpBackup.php --current --pagelist=$APPDIR/pages.list > $SYSBKPDIR/Technotes.wikitxt
php /var/www/wiki/maintenance/version.php > $SYSBKPDIR/WikiVersion.wikitxt
php /var/www/wiki/maintenance/showSiteStats.php > $SYSBKPDIR/SiteStats.txt
php /var/www/wiki/maintenance/dumpBackup.php --full --quiet > $SYSBKPDIR/lah_full_dump.xml

## 3. Dump LAHwiki DB
mysqldump lah_wiki -uroot > $SYSBKPDIR/lah_wiki.sql
mysqldump lah_wiki_en -uroot > $SYSBKPDIR/lah_wiki_en.sql

## 4. Archive all and split by volumes
tar chjf $TOUPLOAD/$NOW.tar.bz2 /var/www/wiki
split -b 500M $TOUPLOAD/$NOW.tar.bz2 $TOUPLOAD/$NOW.tar.bz2_part_ -a 4

## 5. Send backups to TG
cd $APPDIR
$APPDIR/sendtotg.py  -t "=============== Start of backup "$NOW" ==============="
for i in `ls $TOUPLOAD/*_part_*` 
    do
	$APPDIR/sendtotg.py $i
    done
$APPDIR/sendtotg.py  -t "=============== End of backup "$NOW" ==============="

## 6. Clean up
rm -rf $TOUPLOAD
rm -rf $SYSBKPDIR

