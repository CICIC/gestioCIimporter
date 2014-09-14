#!/bin/bash
path="../gestioCI_butterfly_release/"
input=$1
answer="y"

echo "Possible sql files:"
ls $path*.sql

user="gestioCI"
password="gestioCI"
dbName="gestioCI_butterfly"
host="localhost"

for i in `mysql -u$user -p$password -h $host  $dbName -e "show tables" | grep -v Tables_in` ; do mysql -u$user -p$password -h $host $dbName -e "SET FOREIGN_KEY_CHECKS = 0; drop table $i ; SET FOREIGN_KEY_CHECKS = 1" ; done


while [[ ! -r $input && $input != "q" ]]
  do
    echo "Type a readable SQL file as a parameter or 'q' to quit"
    read input
done

if [ $input != "q" ]
  then
    echo "Updating the database" 
    mysql -u $user -p$password $dbName < $input
fi

#mysql -u $user -p$password $dbName < bdgestiociProduccio.sql 
echo "end of the script"
rm *.log
