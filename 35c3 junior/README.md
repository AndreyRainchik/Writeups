# 35C3 Junior CTF

This was a CTF held on December 27-29 2018 by the Chaos Computer Club, and was the first competitive jeopardy-style CTF I've participated in. Individually, I ended up placing 277th out of 520 with three flags, but everyone's gotta start somewhere :)

The challenges and their sources can be found [here](https://junior.35c3ctf.ccc.ac/challenges/ "link to the ctf"), and hopefully everything is still there. The IP addresses and ports for the challenges have changed since the CTF ended, so I'll update any scripts I provide to work for the new information.

## Pwn

### Poet

This flag involved a server hosting a [binary file](./files/poet.bin "The vulnerable binary file") that asks for a one-line poem and a poet, and then will generate a score for that poem. To get the amazing prize, our poem must score exactly 1000000 points, and then we'll get the flag.

```
$ nc 35.207.132.47 22223

**********************************************************
* We are searching for the poet of the year 2018.        *
* Submit your one line poem now to win an amazing prize! *
**********************************************************

Enter the poem here:
> Others have already written what I would like to write.
Who is the author of this poem?
> Joe Brainard

+---------------------------------------------------------------------------+
THE POEM
Others have already written what I would like to write.
SCORED 0 POINTS.

SORRY, THIS POEM IS JUST NOT GOOD ENOUGH.
YOU MUST SCORE EXACTLY 1000000 POINTS.
TRY AGAIN!
+---------------------------------------------------------------------------+
```

As it turns out, the score is not based off of the poem we give the binary. Instead, a vulnerability exists where if we give the poet name as 64 arbitrary characters, the score will be based off of the next few bytes. For example, if we input the name as `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAd`, we'll receive a score of 100 because the ASCII value for `d` is 100.

```
Enter the poem here:
> a
Who is the author of this poem?
> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAd

+---------------------------------------------------------------------------+
THE POEM
a
SCORED 100 POINTS.

SORRY, THIS POEM IS JUST NOT GOOD ENOUGH.
YOU MUST SCORE EXACTLY 1000000 POINTS.
TRY AGAIN!
+---------------------------------------------------------------------------+
```

The scoring works out to be 1 * the ASCII value of the 65th byte + 256 * the ASCII value of the 66th byte + 65536 * the ASCII value of the 67th character. If we want this to equal 1000000, this turns out to be a simple math equation of 1000000 = x + 256y + 65536z. Solving this gives us x=64, y=66, and z=15. Since the ASCII value of 15 corresponds to an unprintable character, we'll use a [Python script](./files/poet.py "Python script to get the flag") to generate our poet name for us and get the flag while we're at it.

Running this script gives us a flag of `35C3_f08b903f48608a14cbfbf73c08d7bdd731a87d39`
## Web
