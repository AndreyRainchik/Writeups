# Kioptrix 1.1 Writeup
---
## Information gathering

After booting up the attacker and vulnerable virtual machines, we can use the `ifconfig` and `netdiscover` commands to find the IP address of both of them. Running `ifconfig` will get us the IP address of the attacker machine, and from that, we can scan the local subnet with `netdiscover -i eth0 -r 10.0.2.0/24` to find the IP address of the vulnerable machine. The arguments to the `netdiscover` command specify that 

![](images/ifconfig.png "ifconfig shows us that our attacker's IP address is 10.0.2.5")

![](images/netdiscover.png "netdiscover -i eth0 -r 10.0.2.0/24 shows us that there are four possible IP addresses for our target")

