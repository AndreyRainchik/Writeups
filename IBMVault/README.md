# IBM Vault

This CTF involves finding the keys to six "locks", with only one lock active at a time. The link for the CTF is [here](https://www.ibm.com/employment/vault/ "The link to the CTF"), although registration already closed.

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

The clue we're given to this lock is `fonchzopgemkevclewonvnbwtet`, and additionally we're told that this string contains hidden instructions and that the solution to the previous lock will help us. My guess was that this hint was encrypted in some manner, and the decryption key will be found in the answer to the previous lock. I tried several different encryption algorithms, such as the shift cipher and one-time pads, but I struck gold on the Vigenère cipher. When I used a decryption key of AACRTD, or the first letter of each of the cities, the string we were given decrypted to `followopenthevaultontwitter`. The site that I used for my decryption can be found [here](https://www.dcode.fr/vigenere-cipher "The decryption site I used").

Going over to Twitter, I found the user @open\_the\_vault, who has a single tweet that says `You've found me. You need to follow this user, and mention it using the game hashtag to receive the password for Lock 2 via DM.` After following this user, I tweeted at them with \#IBMvault, and I received a DM that said `Good job. The password to open this lock is: nuwanda`. After inputting `nuwanda` as the key, I successfully completed this lock! At the time of my completion, I was number 14 out of the 288 people who solved lock 1.

## Lock 3

This lock was a bit more of a challenge than the other two. The hint here was that the Twitter account I followed in Lock 2 had posted instructions for this lock. The @open\_the\_vault account put out a message that said `Hidden here: https://www-03.ibm.com/employment/us/entry_level_campus.shtml …`. Going to this site revealed a pretty standard recruitment page, with different sections leading to different job applications. I ran this site through Burp Suite's spider function, and something stood out to me. While most of the images used on the site were descriptive of what was in them, like `consultant700x400.png` or `Website_maelstrom1.jpg`, one of these images didn't follow this convention, `FSiInFCrDy.jpg`.

This was a normal image of two office workers in Dubai, and at first, I thought this was a hint to look at the job postings in that city, but alas, there were none. I pounded my head against this image for a while, trying to unlock its secrets, when the official Twitter account put out another hint. This tweet said `you don't have to be an alchemist to figure this one out. Or maybe yes...🤔`, and that's when it hit me. The name of the image was composed of symbols in the periodic table of elements. Translating these symbols revealed the key to be `Fluorine, Silicon, Indium, Fluorine, Chromium, Dysprosium`. I was now 20th out of the 193 people who solved lock 2. 

## Lock 4

As was stated in the intro video for this lock, the clue is hidden somewhere in the answer to lock 3. In this case, I looked at the atomic numbers for each of the elements in the answer. Fluorine is 9, silicon is 14, indium is 49, chromium is 24, and dysprosium is 66. Putting all of these together, we have `9144992466`. Interestingly enough, this number starts with 914, which is a New York area code, and IBM's corporate phone number is 914-992-1900. This could point to this number being a phone number. I called 914-499-2466, and I was greeted with a voicemail stating that the key for this lock is the meaning of life. This meant that the key for this lock is `42`. Now, I was 22nd out of the 152 people who solved lock 3.

## Lock 5

This was another tricky problem, and I'm not sure how anyone would have been able to solve this without the hints given by the official Twitter account. To start this challenge, the Twitter account @open\_the\_vault posted [this image](https://pbs.twimg.com/media/Dn3GgQrXoAAPHMv.jpg:large "The image posted for this challenge"), stating that some hints for the password were here. I noticed somethin interesting in this image, in particular that the labeling at the top of the rack goes "A B C D E O G H", replacing F with O. Doing a reverse image search, I found an image that looks [remarkably similar](https://cdn-images-1.medium.com/max/1600/1*IFRN25To-SHNq4Q-U6scGw.jpeg "The original image") to what the Twitter account gave us. Some other inconsistencies between the images are that there is an added E on the man's badge and that the L was removed from the keyboard in the rack. This gives us a total of three changed letters, `O, L, and E`.

This is where I got stuck. The video introduction for this lock said that we can use this to find the right IP, so I thought that converting these letters from ascii to decimal might give us an IP address, but we're missing a fourth octet. At this point, the Twitter account posted to `Think about the previous answer, now look at what you've found.` Since the previous answer was `42`, I thought that this was the missing part of the IP address, but that was not the case. Another hint that the Twitter account posted was `Bored? Better play a hangman, it's fun...`, and it clicked for me that the letters that we found were part of the key, and there was no IP address involved at all. Combining this with the previous hint led me to think about important things in the Hitchhiker's Guide to the Galaxy series, and I remembered that you shouldn't go anywhere without your towel. I entered `towel` as the key, and lock 5 was solved. I was now 23 out of the 143 people who solved lock 4.

## Lock 6

The final challenge was a lot more technically involved than the previous ones. This lock presented three possible paths for solving it, each with its own key. Two of these options involved fixing JavaScript web applications, and the third was about working with mainframes. I finished the mainframe key, but it pretty much had the instructions spelled out for you so it's no fun to do a write-up on it. Thus, for fun, I took on one of the web app challenges. A fork of the original web application can be [found here](https://github.com/AndreyRainchik/lock6-fix-1 "The original web application").

I started the web app up with `npm install` and `npm start`, navigated to `http://localhost:3000/explorer` in my web browser, and I noticed that while I could view customer information, I was unauthorized to view the videos section. I went through the code and saw that there was a token for this information in the [datasources.json](https://github.com/AndreyRainchik/lock6-fix-1/blob/master/server/datasources.json "Code for datasources.json") file relating to the video records. Clearly, this token was wrong and would need to be fixed. But how? Going through more of the code revealed a comment in the [test-external-api.js](https://github.com/AndreyRainchik/lock6-fix-1/blob/master/server/boot/test-external-api.js "Code for test-external-api.js") file that pointed to the solution. The comment said:

```
There's something wrong with the authentication for this API.
It's a true enigma.
I got these credentials from the German office:
M3 I/8 II/14 III/12 UKW B
aeybc ciwyg eywqg
```

To me, this meant to look at decoding this with an Enigma machine. I found a decoder [here](https://cryptii.com/pipes/enigma-machine "Enigma machine decoder"), selected the Enigma M3 model, plugged in rotor 1 at I position 8 ring 1, rotor 2 at II position 14 ring 1, rotor 3 at III position 12 ring 1, chose the UKW B reflector, completely cleared the plugboard, and the ciphertext decoded to `super secrt token`. 

Swapping this in for the token in datasources.json allowed me to authenticate to the videos section, and revealed `Available videos: [{"title":"Summer Promotion","url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}]`. However, this video was a dead end as it led to Rick Astley's classic song Never Gonna Give You Up. This was the first rickroll I've gotten in several years. Now, I had to find a different path.

Going back to the datasources.json file, the voicemails section caught my eye. This section wasn't present at all in the web application, the only mention of it was in this file. I decided to modify the web app to shine some light on this section. First, I copied the [videos.json](https://github.com/AndreyRainchik/lock6-fix-1/blob/master/common/models/videos.json "Code for videos.json") file into voicemails.json and replaced the name with "Voicemails". This set up the voicemails model in the web app so that I could access it properly. Next, I added a line in the test-external-api.js file that would call the find() function of the Voicemails model and log it to the console. Then, I copied the videos section in [model-config.json](https://github.com/AndreyRainchik/lock6-fix-1/blob/master/server/model-config.json "Code for model-config.json") and pasted it back into the same file, changing the name of it and making the data source voiceMailsRecords. 

After these changes, I ran the web app again with `npm start` and I was told that I was unauthorized to view the voicemail records. A similar issue to the videos section, I added the same token to voiceMailsRecords in the datasources.json file, and I received a result of

```
Available voicemails: [{"messageNumber":1,"url":"https://ibm-vault-api.mybluemix.net/private/audio/message1.mp3"},{"messageNumber":2,"url":"https://ibm-vault-api.mybluemix.net/private/audio/message2.mp3"},{"messageNumber":3,"url":"https://ibm-vault-api.mybluemix.net/private/audio/message3.mp3"},{"messageNumber":4,"url":"https://ibm-vault-api.mybluemix.net/private/audio/message4.mp3"},{"messageNumber":5,"url":"https://ibm-vault-api.mybluemix.net/private/audio/message5.mp3"},{"messageNumber":6,"url":"https://ibm-vault-api.mybluemix.net/private/audio/message6.mp3"}]
```

Going to the URLs of these voicemails in a web browser gave me an authentication error because I didn't have the right token set, so I used cURL to download them with `curl https://ibm-vault-api.mybluemix.net/private/audio/message1.mp3 --header "Token: super secrt token" -O` I swapped out the filenames so that I downloaded all six voicemails, and they can be found [here](https://github.com/AndreyRainchik/lock6-fix/tree/master/mp3s "The mp3 files I downloaded"). Listening to these files, messages 2 and 5 had Morse code beeping in them. I translated this, and found that message2 was stating "YOU ARE IN DANGER" and message5 was stating "THE SECRET WORD IS ARMOK". I tried `armok` as the key, and it worked! With the conclusion of this last challenge, I was ranked 14th out of the 126 people who solved lock 5, and out of 3093 people total.
