# IBM Vault

This CTF involves involves finding the keys to six "locks", with only one lock active at a time. The link for the CTF is [here](https://www.ibm.com/employment/vault/ "The link to the CTF"), although registration already closed.

## Lock 1

The clue we're given to the first lock is `5833372e32313130343936582d3132312e383037303834315833302e34303138333935582d39372e373135353130335834322e3336363531353739393939393939582d37312e3037373231393039393939393938582d32322e39353034383739582d34332e31373730333537303030303030335833352e3637383533333420583133392e37383730383532393939393939345835332e34313838343235582d362e34313833393734`. I noticed that this string included hex digits within the printable ASCII range, so I ran it through a hex-to-ASCII converter found [here](https://www.rapidtables.com/convert/number/hex-to-ascii.html "Hex-to-ASCII converter"), and received a result of `X37.2110496X-121.8070841X30.4018395X-97.7155103X42.36651579999999X-71.07721909999998X-22.9504879X-43.17703570000003X35.6785334 X139.78708529999994X53.4188425X-6.4183974`.

These stood out to me as being possible coordinates, and I separated them into pairs, resulting in 
```
X37.2110496
X-121.8070841

X30.4018395
X-97.7155103

X42.36651579999999
X-71.07721909999998

X-22.9504879
X-43.17703570000003

X35.6785334 
X139.78708529999994

X53.4188425
X-6.4183974
```

Plugging these pairs into a [map](https://www.gps-coordinates.net/ "Link to a map utility"), with the first number of each pair corresponding to the latitude and the second as the longitude revealed that these were the coordinates of several IBM research centers in Almaden, Austin, Cambridge, Rio de Janeiro, Tokyo, and Dublin. On a whim, I input these cities as the key, and it worked! The key to lock 1 is `Almaden, Austin, Cambridge, Rio de Janeiro, Tokyo, Dublin`. At the completion of this lock, I was number 30 out of 3093 people on the leaderboard.

## Lock 2

The clue we're given to this lock is `fonchzopgemkevclewonvnbwtet`, and additionally we're told that this string contains hidden instructions and that the solution to the previous lock will help us. My guess was that this hint was encrypted in some manner, and the decryption key will be found in the answer to the previous lock. I tried several different encryption algorithms, such as the shift cipher and one-time pads, but I struck gold on the Vigenère cipher. When I used a decription key of AACRTD, or the first letter of each of the cities, the string we were given decrypted to `followopenthevaultontwitter`. The site that I used for my decryption can be found [here](https://www.dcode.fr/vigenere-cipher "The decryption site I used").

Going over to Twitter, I found the user @open\_the\_vault, who has a single tweet that says "You've found me. You need to follow this user, and mention it using the game hashtag to receive the password for Lock 2 via DM." After following this user, I tweeted at them with \#IBMvault, and I received a DM that said "Good job. The password to open this lock is: nuwanda". After inputting `nuwanda` as the key, I successfully completed this lock! At the time of my completion, I was number 14 out of the 288 people who solved lock 1.
