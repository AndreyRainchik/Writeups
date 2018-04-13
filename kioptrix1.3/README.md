# Kioptrix 1.3 Writeup

This vulnerable virtual machine was obtained from [VulnHub](https://www.vulnhub.com/entry/kioptrix-level-13-4,25/ "URL for kioptrix 1.3"). The kioptrix series are intended for use with VMWare, but by following the instructions found [here](http://hypn.za.net/blog/2017/07/15/running-kioptrix-level-1-and-others-in-virtualbox/ "running kioptrix in VirtualBox"), you can get the virtual machines to work with VirtualBox.

## Information gathering

By now, we know that our attacker's IP address is 10.0.2.5 from the result of the `ifconfig` command. To find the IP of the target, we'll scan the local subnet with `nmap -sn 10.0.2.0/24` to find what hosts are on the network.

![](images/ping.png "nmap -sn 10.0.2.0/24 shows us that there are four possible IP addresses for our target")

The two VirtualBox hosts are `10.0.2.3` and `10.0.2.8`, and VirtualBox uses the former for its nameserver, so our target is `10.0.2.8`.

## Scanning

Now, we'll use `nmap -sV 10.0.2.8` to enumerate the services running on the target, and this will provide an attack surface for us.

![](images/nmap.png "nmap -sV 10.0.2.8 tells us the services runnning on the target")

We see that the target has several ports open, and we'll go down the list to find an exploitable one.

## Gaining access

From previous engagements with the past Kioptrix virtual machines, I know that the version of OpenSSH running is not one that we can easily exploit. You can look through my previous writeups to see how I came to that conclusion, or you can run `searchsploit openssh` and see that none of the available exploits are that useful for us.

Instead, we'll target port 80, which is running the http service, meaning that if we go to http://10.0.2.8 in a web browser, we'll get a web page back.

![](images/front.png "Front page of http://10.0.2.8")

We can also run an application called OWASP ZAP which will inform us of any vulnerabilities in the web app. Loading up ZAP and putting http://10.0.2.8 into the target field will perform a scan of the web application, and we can see the results.

![](images/zap.png "Result of running OWASP ZAP")

It looks like the checklogin.php page is vulnerable to an SQL injection. Looking at the request sent, we can see that the HTTP POST method is used with parameters of "myusername", "mypassword", and "Login". We can take this information and use another tool, sqlmap, to perform automated SQL injections so that we can find valid usernames and passwords. We run this tool with the command `sqlmap -u "http://10.0.2.8/checklogin.php" --data "myusername=test&mypassword=test&Submit=login" --dump --level=5 --risk=3`. This tells sqlmap to target the checklogin.php page on 10.0.2.8, using the data string provided in an HTTP POST request, dump the resulting database table entries, and operate with high-level and high-risk tests.

![](images/sqlmap.png "Result of the sqlmap attack")

The resulting attack gives us the usernames and passwords of two users, john and robert. Logging in to the web page as either user just displays the username and password, so instead, we'll use SSH to connect to the vulnerable machine with the command `ssh john@10.0.2.8` and entering the password when prompted.

## Elevating Access

!
