# Kioptrix 1.1 Writeup

This vulnerable virtual machine was obtained from [VulnHub](https://www.vulnhub.com/entry/kioptrix-level-11-2,23/ "URL for kioptrix 1.1")

## Information gathering

After booting up the attacker and vulnerable virtual machines, we can use the `ifconfig` and `netdiscover` commands to find the IP address of both of them. Running `ifconfig` will get us the IP address of the attacker machine, and from that, we can scan the local subnet with `netdiscover -i eth0 -r 10.0.2.0/24` to find the IP address of the vulnerable machine. The arguments to the `netdiscover` command specify that the network device `eth0` should be used for sniffing for ARP packets, and that the range to scan should be the IP addresses included in the `10.0.2.0/24` subnet, which are `10.0.2.1 - 10.0.2.254`.

![](images/ifconfig.png "ifconfig shows us that our attacker's IP address is 10.0.2.5")

![](images/netdiscover.png "netdiscover -i eth0 -r 10.0.2.0/24 shows us that there are four possible IP addresses for our target")

`netdiscover` presents us with four possible IP addresses for our target machine, and now we must narrow down the specific one that we will be exploiting. Since we know that our target is running as virtual machine on VirtualBox, that narrows the options down to `10.0.2.3` and `10.0.2.4`, because VirtualBox typically uses the `08:00:27` MAC address prefix. After `ping`ing both of the addresses, it is determined that `10.0.2.4` is the target, because it replies to the pings.

## Scanning

Now that we know what our target is, we will enumerate the ports that are open to try to see if any of them have vulnerable services running. The tool we'll use for that is `nmap`. Running `nmap -sV 10.0.2.4` will tell us the specific versions of the services running on the TCP ports, if possible, as compared to a normal `nmap 10.0.2.4`, which will just tell us the services that are running.

![](images/nmap.png "nmap -sV 10.0.2.4 shows us which services are running on the machine")

We can see that the target has several ports open, and we'll run down the list to try to see which ones we can exploit.

## Gaining Access

Using the `searchsploit` command, we can look for exploits that the target could be vulnerable to. Running `searchsploit openssh` shows us all of the exploits available for OpenSSH from [exploit-db](https://www.exploit-db.com/ "exploit-db"), but unfortunately, none of them are of interest to us. We're looking for something that can give us remote code execution, and the only one found that does that is for OpenSSH 3.5p1, while the version on the target is more recent than that.

![](images/openssh.png "searchsploit openssh shows us the available exploits for OpenSSH")

Next, since http is running on port 80, we can try to navigate to the IP address in a web browser and see what we can find. Loading up `http://10.0.2.4` in Firefox gives us a login screen for remote system administration. This seems like a promising attack vector.

![](images/login.png "http://10.0.2.4 loaded in Firefox")

Since MySQL is also running on the target machine, it's likely that this login form is using SQL, and we can check to see if it's vulnerable to an SQL injection. A simple login SQL query would be something like `SELECT id FROM Users WHERE Username = 'InputUsername' AND Password = 'InputPassword'`, so we can manipulate the username and password parameters to get a valid SQL statement that will let us log in. If we use `' OR ''='` for both the username and the password, then the SQL query becomes `SELECT id FROM Users WHERE Username = '' OR ''='' AND Password = '' OR ''=''`, which checks to see if there exists a username and password combo that are empty strings, or if `''=''`, which is true. This means that the SQL statement is valid, and it will log us in as the first user in the user table, and we now have access to the administrative console.

![](images/console.png "Using ' OR ''=' for both the username and password logs us in to the admin console")

This console provides a text box where we can input an IP address and the target will ping it and provide the results for us.

![](images/ping.png "Result of putting 8.8.8.8 into the text box and submitting")

Interestingly enough, the results that are provided seem to be the same as if the Unix command `ping -c 3 8.8.8.8` was used. Could it be possible that the web console is just throwing what we type into the text box into the command and executing it on the server? Let's test out this theory by putting `8.8.8.8; whoami` into the field. This will allow us to run the `whoami` command after the server pings 8.8.8.8, and if our hypothesis is correct, we'll see the user that the console is running the command as.

![](images/whoami.png "Result of putting 8.8.8.8; whoami into the text box and submitting")

Looks like the idea was right. We can see that after the ping results, there's a line for "apache," meaning that this is who the commands are running under, and that we have remote command execution on the machine. However, we don't have root access yet, which is our main objective. Additionally, our access is limited to just sending commands, we don't have a completely interactive way of communicating with the target machine. These issues are what we will solve in the next step.

## Elevating access

Let's try to achieve an interactive way to talk to the target machine. Since we can execute a command with the administrative web console, we can use `nc` on both our attacking machine and on the console to start an interactive session. 
