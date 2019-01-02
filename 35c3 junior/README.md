# 35C3 Junior CTF

This was a CTF held on December 27-29 2018 by the Chaos Computer Club, and was the first competitive jeopardy-style CTF I've participated in. Individually, I ended up placing 277th out of 520 with three flags, but everyone's gotta start somewhere :)

The challenges and their sources can be found [here](https://junior.35c3ctf.ccc.ac/challenges/ "link to the ctf"), and hopefully everything is still there. The IP addresses and ports for the challenges have changed since the CTF ended, so I'll update any scripts I provide to work for the new information.

Many of the challenges in this CTF revolved around a custom web application called [Paperbots](http://35.207.132.47 "The web application") which uses the Wee programming language to allow a user to "write different types of programs, from instructions for a robot, to games and interactive art". The source code for the web application was found at [/pyserver/server.py](./files/wee_server.py "Source code for the web application"). If a particular flag involved this site, I will mention it in the writeup.

## Pwn

### 1996

The first of the pwn challenges was based around a [program](./files/1996 "The binary file") that would give the output of a given environment variable. The source code for the program was [fortunately available](./files/1996.cpp "The source code for the program") for us to look through, and it shows us that there's a function that will run shell commands.

```c++
void spawn_shell() {
    char* args[] = {(char*)"/bin/bash", NULL};
    execve("/bin/bash", args, NULL);
}
```

The program stores input in a 1024 byte buffer but does no checking on the size of the input, so if we give it an input of more than 1024 characters, we can overflow the buffer. By overflowing enough to overwrite important pieces of memory, we can execute the `spawn_shell()` function and then run whatever commands we want.

Doing some testing revealed that if we have an input of 1048 characters, any additional input after that will overwrite the RIP memory register, which tells the computer where to go in memory next to execute the next command. So if we have an input of 1048 A's and 6 B's, the computer will try to go to the command at `0x424242424242`, which is invalid. You can use [gdb-peda](https://github.com/longld/peda "Link for gdb-peda") to see how this interaction works.

```
Stopped reason: SIGSEGV
0x0000424242424242 in ?? ()
gdb-peda$ x/wx $rip
0x424242424242:	Cannot access memory at address 0x424242424242
```

If we can get the memory address of the `spawn_shell()` function, we can tell the computer to go there next, which will run the function. Running `objdump -d 1996` will output the assembly commands for the program, but what we care about is the line `0000000000400897 <_Z11spawn_shellv>:` which tells us that the `spawn_shell()` function is at the memory address `0000000000400897`. It's important to note that your computer is probably little-endian, so we'll essentially need to store the bytes in reverse order, meaning that we can generate our proper input with the Python command 

```python
print '\x41' * 1048 + '\x97\x08\x40\x00\x00\x00'
```

Using [this Python script](./files/1996.py "Python script to get the flag") will connect to a server at 35.207.132.47 port 22227, send the input, and read the flag, which turns out to be `35C3_b29a2800780d85cfc346ce5d64f52e59c8d12c14`

### Poet

This flag involved a server at 35.207.132.47 port 22223 hosting a [binary file](./files/poet.bin "The vulnerable binary file") that asks for a one-line poem and a poet, and then will generate a score for that poem. To get the amazing prize, our poem must score exactly 1000000 points, and then we'll get the flag.

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

### Flags

This challenge works off of a [web server](http://35.207.132.47:84/ "The webserver") with a [script](./files/flags.php "The script served by the webserver") that will display a flag depending on the supplied `HTTP_ACCEPT_LANGUAGE` header given by an HTTP request. The description states that the flag is located at `/flag`, so with the vulnerable code `$c = file_get_contents("flags/$lang");`, we can have an `HTTP_ACCEPT_LANGUAGE` header of `../../../../../../../../flag` and we'll receive our flag.

However, some filtering is in place to prevent this with the line `$lang = str_replace('../', '', $lang);`, which removes every instance of ../ in the header. But if the filter is applied on the string `....//`, it will remove the instance of `../` and give us a result of `../`, which we wanted in the first place. So now if our header is `....//....//....//....//....//....//....//....//flag`, we'll get past the filter and receive our flag encoded in Base64.

With a quick little [Python script](./files/flags.py "Python script to get the flag"), we can request for and decode our flag of `35c3_this_flag_is_the_be5t_fl4g`

### Logged In

As one of the challenges involving the Paperbots application, finding this flag required a user to log in to the app. Unfortunately, registering for an account is supposed to email you with a verification code, but the functionality wasn't implemented in time. Luckily, several functions in the source code allow us to work around this.

Making a POST request to the `/api/signup` endpoint with an email and username will add a user to the user database. Then, another POST request to `/api/verify` with the same email will query the database and return the verification code for the user. Passing this code to `/api/login` with a further POST request will then set a cookie called `logged_in`, which is our flag.

[This Python script](./files/loggedin.py "Python script to get the flag") will automatically perform these actions and print out the flag of `35C3_LOG_ME_IN_LIKE_ONE_OF_YOUR_FRENCH_GIRLS`.

### McDonald

The description for this web challenge was that `Our web admin name's "Mc Donald" and he likes apples and always forgets to throw away his apple cores..`. Going to the web server at `http://35.207.132.47:85` reveals a pretty empty web page that just displays the description. The source code didn't have anything interesting in it, so I checked out the `/robots.txt` file and found an entry of `Disallow: /backup/.DS_Store`. Going to that file downloads a [.DS_Store](./files/DS_Store "The .DS_Store file") file. This file is a special Mac file that contains the metadata for the containing folder, so if we can read it, we'll get information about the backup folder.

Using the [ds_store](https://ds-store.readthedocs.io/en/latest/ "ds_store Python library") Python library, we can get a listing of the folders within `/backup`. We find that there are multiple folders named `/a`, `/b`, and `/c`, and if we go to them, we get an HTTP 403 Forbidden error, meaning that the folder exists but we can't access it. Trying different combinations such as `/a/b/c` continues to give 403 errors, but when you try to go four layers deep, such as `/a/b/c/a`, we end up with HTTP 404 Not Found errors, meaning that we have a maximum depth of 3 and thus 18 potential folders to go through.

I put together a [Python script](./files/mcdonald.py "Python script to get the flag") that will go through each combination of folders until it finds a file called `flag.txt` and then prints out the contents. Running it reveals that the flag is inside `/backup/b/a/c` and is `35c3_Appl3s_H1dden_F1l3s`
