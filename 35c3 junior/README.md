# 35C3 Junior CTF

This was a CTF held on December 27-29 2018 by the Chaos Computer Club, and was the first competitive jeopardy-style CTF I've participated in. Individually, I ended up placing 277th out of 520 with three flags, but everyone's gotta start somewhere 😊

The challenges and their sources can be found [here](https://junior.35c3ctf.ccc.ac/challenges/ "link to the ctf"), and hopefully everything is still there. The IP addresses and ports for the challenges have changed since the CTF ended, so I'll update any scripts I provide to work for the new information.

Many of the challenges in this CTF revolved around a custom web application called [Paperbots](http://35.207.132.47 "The web application") which uses the Wee programming language to allow a user to "write different types of programs, from instructions for a robot, to games and interactive art". The source code for the web application was found at [/pyserver/server.py](./files/ctf_files/wee_server.py "Source code for the web application"). If a particular flag involved this site, I will mention it in the writeup.

## Misc

### Conversion Error

Many of the challenges in the Misc category are about trying to trigger assert statements in the weeterpreter found in the Paperbots application. We can run wee code by sending an HTTP POST request to /wee/run with the code in a `code` json parameter.

```python
@app.route("/wee/run", methods=["POST"])
def weeservice():
    json = request.get_json(force=True)
    wee = json["code"]
    out = runwee(wee)
    return jsonify({"code": wee, "result": out})
```

This then runs the `runwee()` function.

```python
# Wee as a service.
def runwee(wee: string) -> string:
    print("{}: running {}".format(request.remote_addr, wee))
    result = check_output(
        ["ts-node", '--cacheDirectory', os.path.join(WEE_PATH, "__cache__"),
         os.path.join(WEE_PATH, WEETERPRETER), wee], shell=False, stderr=STDOUT, timeout=WEE_TIMEOUT,
        cwd=WEE_PATH).decode("utf-8")
    print("{}: result: {}".format(request.remote_addr, result))
    return result
```

We can see that this function makes an operating system call to run the weeterpreter, and we can find the locations of the `WEE_PATH` and `WEETERPRETER` in the Python server file.

```python
WEE_PATH = "../weelang"
WEETERPRETER = "weeterpreter.ts"
```

Now if we go to [http://35.207.132.47/weelang/weeterpreter.ts](./files/ctf_files/weeterpreter.ts "weeterpreter code"), we can view the code and see how the weeterpreter runs.

```javascript
if (require.main === module) {
    //eval_in_chrome("1+1")
    const wee = process.argv[2];
    //console.log(wee)
    wee_exec(wee)
        .then(_=>browserPromise)
        .then(b=>b.close())
        .then(_=>process.exit())
}
```

Running the weeterpreter will call the `wee_exec()` function on the input code we provided.

```javascript
export async function wee_exec(code: string) {
    try {
        const compiled = compiler.compile(code, get_headless_externals())
        const vm = new VirtualMachine(compiled.functions, compiled.externalFunctions)
        while (vm.state != VirtualMachineState.Completed) {
            vm.run(10000)
            await DoEvents() // Excited about this name! VB6 <3. Nothing beats the good ol' "On Error Resume Next"...
        }
        vm.restart()
    } catch (ex) {
        console.error(ex.message)
    }
}
```

Looks like `wee_exec()` compiles our code and then runs it in a virtual machine. Looking at the `get_headless_externals()` that the compiler uses, we see the assert statements that we'll be triggering. For this flag in particular, we'll look at the `assert_conversion()` statements.

```javascript
externals.addFunction(
    "assert_conversion",
    [{name: "str", type: compiler.StringType}], compiler.StringType,
    false,
    (str: string) => str.length === str + "".length || !/^[1-9]+(\.[1-9]+)?$/.test(str)
        ? "Convert to Pastafarianism" : flags.CONVERSION_ERROR
)
```

Focusing on that last line, we can see how we get our flag. The format of the assert statement boils down to `test ? true : false`, so if we get the test statement of `str.length === +str + "".length || !/^[1-9]+(\.[1-9]+)?$/.test(str)` to be false, we'll get our flag. As this is an OR statement, denoted by the `||`, both of `str.length === +str + "".length` and `!/^[1-9]+(\.[1-9]+)?$/.test(str)` need to be false for the whole thing to be false.

Looking at the statement on the right, it looks to be a regex expression that we can evaluate. The exclamation mark in the front shows that we'll take the inverse of whatever the regex spits out, so we need to find a string that matches the regex in order to get a false value. The regex starts from the start of the string and looks for a single digit between 1 and 9, inclusive. Then it looks for a period and then another digit between 1 and 9, inclusive. So basically, if we have a number between 1 and 9 with a single decimal, we can match the regex and then get an overall value of false for this statement.

Now we need to get the left part of the statement to be false. It takes the length of the string and checks to see if it's equal to the string + 0. When you add a string plus an integer in Javascript, it will just append the integer to the string. So for example, `"1.1" + 0` would turn out to be `1.10`, and we can see that this is not exactly equal to `1.1`, so this statement will always be false. 

Now that both sides of the OR statement are false, the entire thing is false and we'll get our flag. However, we'll need to actually print out our flag because the assertion doesn't actually print anything. Looking at the weeterpreter code further, we see that there are `alert()` functions that we can use.

```javascript
externals.addFunction(
    "alert",
    [{name: "message", type: compiler.StringType}], compiler.NothingType,
    false,
    console.log
)
```

Calling this function will print out what it's given, so if we choose the wee code `alert(assert_conversion("1.1"))`, we can use that in our POST request to `/wee/run` and get our flag.

[This Python script](./files/flag_scripts/conversion.py "Python script to get the flag") will run through this process and print out the flag of `35C3_FLOATING_POINT_PROBLEMS_I_FEEL_B4D_FOR_YOU_SON`

### Equality Error

An additional challenge focusing on assert statements, the `assert_equals()` check makes sure that a number is equal to itself.

```javascript
externals.addFunction(
    "assert_equals",
    [{name: "num", type: compiler.NumberType}], compiler.StringType,
    false,
    (num: number) => num === num
        ? "EQUALITY WORKS" : flags.EQUALITY_ERROR
)
```

Seems like any number would equal itself, but what if we try something that's not a number? In JavaScript, NaN is a value that's Not-a-Number, like the square root of -1 or a division by 0. It also has the property that [NaN is not equal to itself](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NaN#Testing_against_NaN "Documentation showing Nan != NaN"). This means that if we use `alert(assert_equals(0/0))` as the `code` parameter in a POST request to `/wee/run`, the assert will fail and give us the flag.

[This Python script](./files/flag_scripts/equality.py "Python script to get the flag") will run through this process and print out the flag of `35C3_NANNAN_NANNAN_NANNAN_NANNAN_BATM4N`

### Number Error

More assertion shenanigans happen in this challenge. Now, the `assert_number()` statement checks to see if the number that's passed in is valid.

```javascript
externals.addFunction(
    "assert_number",
    [{name: "num", type: compiler.NumberType}], compiler.StringType,
    false,
    (num: number) => !isFinite(num) || isNaN(num) || num !== num + 1
        ? "NUMBERS WORK" : flags.NUMBER_ERROR
)
```

The check makes sure that the number is not infinity, is not NaN, and is not equal to the sum of the number plus 1. To trip up this check, we'll use a number that is equal to the itself plus 1. In JavaScript, the maximum safe integer is `9007199254740991`, as this is 2^(53)-1 and JavaScript stores numbers as floating-points with 52 bits allocated to the part after the decimal. This means that if we add 1 to a number greater than `9007199254740991`, it will be [treated as the same number](https://stackoverflow.com/a/4375743 "StackOverflow post explaining this"). So if we use `alert(assert_number(9007199254740992))` as the `code` parameter in a POST request to `/wee/run`, the assert will fail and give us the flag.

[This Python script](./files/flag_scripts/number.py "Python script to get the flag") will run through this process and print out the flag of `35C3_THE_AMOUNT_OF_INPRECISE_EXCEL_SH33TS`

### Wee R Leet

As another challenge that involves the assert statements in the weeterpreter, we'll run through the same process as the others. The statement for this one is as follows.

```javascript
externals.addFunction(
    "assert_leet",
    [{name: "maybe_leet", type: compiler.NumberType}], compiler.StringType,
    false,
    (maybe_leet: number) => maybe_leet !== 0x1337 ? "WEE AIN'T LEET" : flags.WEE_R_LEET
)
```

To trigger this statement, we need to input a number that corresponds to hexadecimal value `0x1337`. A quick conversion shows that the decimal value for this is 4919, so if we use `alert(assert_leet(1337))` as the value for the `code` parameter in our POST request to `/wee/run`, we'll get our flag.

[This Python script](./files/flag_scripts/leet.py "Python script to get the flag") will run through this process and print out the flag of `35C3_HELLO_WEE_LI77LE_WORLD`

### Wee Token

The last of the assert challenges, this one focuses on the `assert_string()` statement, which checks to see if an input string is actually a string.

```javascript
externals.addFunction(
    // Wee is statically typed. Finding a way to confuse the VM is impossible.
    "assert_string",
    [{name: "str", type: compiler.StringType}], compiler.StringType,
    false,
    (str: string) => typeof str == "string" ? "WEE is statically typed. Sorry, confusing the VM is impossible."
        : flags.WEE_TOKEN
)
```

One option we have is to use the `eval()` JavaScript function to our advantage. This function takes a string input that represents a JavaScript expression, and returns the completion value of evaluating the expression as a string. However, if it's given an empty string as input, it will return `undefined`, which has its own type. So now if we use `alert(assert_string(eval('')))` as the value for the `code` parameter in our POST request to `/wee/run`, we'll get our flag.

[This Python script](./files/flag_scripts/weetoken.py "Python script to get the flag") will run through this process and print out the flag of `35C3_WEE_IS_TINY_AND_SO_CONFU5ED`

### ultra secret

In this challenge, we have to connect to a server at 35.207.132.47 port 1337 and input the correct password to get the flag. We also get a hint that the password is limited to digits and lowercase letters. The source code for the authentication process is also provided for us, and can be found [here](./files/ctf_files/ultra_secret.rs "Source code for authentication process") Looking at it, we get a few important pieces of information. First, we can tell that the authentication process only looks at the first 32 characters of the password.

```rust
let password = &password[0..32];
```

Then, it calls a `hash()` function on the first character of the given password, and if it matches the `hash()` result of the first character of the actual password, it'll move on and do the same for the second character and so on.

```rust
for c in password.chars() {
    let hash =  hash(c);
    if hash != hashes[i] {
        exit(1);
    }
    i += 1;
}
```

The `hash()` function isn't one that's provided by the Rust language used, instead there's a specially defined function that when given a character will then do 1000 rounds of SHA-256 hashing on the character.

```rust
fn hash(c: char) -> String {
    let mut hash = String::new();
    hash.push(c);
    for _ in 0..9999 {
        let mut sha = Sha256::new();
        sha.input_str(&hash);
        hash = sha.result_str();
    }
    hash
}
```

1000 rounds of hashing per character would take a noticeable amount of time for each character, so we can try a timing attack on the password. Essentially, we'll take a possible first character and submit it to see how long it takes to be rejected. Then, we'll try it again for the rest of the possible first characters, working through the entire lowercase alphabet and all 10 digits. Finding the actual first character of the password is done by seeing which character takes the longest to be rejected. This is because once the first character is done being hashed, it will successfully match the first character of the actual password and the authentication process will move on to the next character and hash that. This moving on requires us to have a full 32-character password sent, so we can use a character we know isn't in the password, like a space or hyphen, to fill it out.

A fairly simple [Python script](./files/flag_scripts/ultrasecret.py "Python script to get the flag") will perform this timing attack for us, and then we'll find that the password is `10e004c2e186b4d280fad7f36e779ed4` and submitting it will get our flag of `35C3_timing_attacks_are_fun!_:)`

## Pwn

### 1996

The first of the pwn challenges was based around a [program](./files/ctf_files/1996 "The binary file") that would give the output of a given environment variable. The source code for the program was [fortunately available](./files/ctf_files/1996.cpp "The source code for the program") for us to look through, and it shows us that there's a function that will run shell commands.

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

Using [this Python script](./files/flag_scripts/1996.py "Python script to get the flag") will connect to a server at 35.207.132.47 port 22227, send the input, and read the flag, which turns out to be `35C3_b29a2800780d85cfc346ce5d64f52e59c8d12c14`

### Poet

This flag involved a server at 35.207.132.47 port 22223 hosting a [binary file](./files/ctf_files/poet.bin "The vulnerable binary file") that asks for a one-line poem and a poet, and then will generate a score for that poem. To get the amazing prize, our poem must score exactly 1000000 points, and then we'll get the flag.

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

The scoring works out to be 1 * the ASCII value of the 65th byte + 256 * the ASCII value of the 66th byte + 65536 * the ASCII value of the 67th character. If we want this to equal 1000000, this turns out to be a simple math equation of 1000000 = x + 256y + 65536z. Solving this gives us x=64, y=66, and z=15. Since the ASCII value of 15 corresponds to an unprintable character, we'll use a [Python script](./files/flag_scripts/poet.py "Python script to get the flag") to generate our poet name for us and get the flag while we're at it.

Running this script gives us a flag of `35C3_f08b903f48608a14cbfbf73c08d7bdd731a87d39`

## Web

### Flags

This challenge works off of a [web server](http://35.207.132.47:84/ "The webserver") with a [script](./files/ctf_files/flags.php "The script served by the webserver") that will display a flag depending on the supplied `HTTP_ACCEPT_LANGUAGE` header given by an HTTP request. The description states that the flag is located at `/flag`, so with the vulnerable code `$c = file_get_contents("flags/$lang");`, we can have an `HTTP_ACCEPT_LANGUAGE` header of `../../../../../../../../flag` and we'll receive our flag.

However, some filtering is in place to prevent this with the line `$lang = str_replace('../', '', $lang);`, which removes every instance of ../ in the header. But if the filter is applied on the string `....//`, it will remove the instance of `../` and give us a result of `../`, which we wanted in the first place. So now if our header is `....//....//....//....//....//....//....//....//flag`, we'll get past the filter and receive our flag encoded in Base64.

With a quick little [Python script](./files/flag_scripts/flags.py "Python script to get the flag"), we can request for and decode our flag of `35c3_this_flag_is_the_be5t_fl4g`

### Logged In

As one of the challenges involving the Paperbots application, finding this flag required a user to log in to the app. Unfortunately, registering for an account is supposed to email you with a verification code, but the functionality wasn't implemented in time. Luckily, several functions in the source code allow us to work around this.

Making a POST request to the `/api/signup` endpoint with an email and username will add a user to the user database. Then, another POST request to `/api/verify` with the same email will query the database and return the verification code for the user. Passing this code to `/api/login` with a further POST request will then set a cookie called `logged_in`, which is our flag.

[This Python script](./files/flag_scripts/loggedin.py "Python script to get the flag") will automatically perform these actions and print out the flag of `35C3_LOG_ME_IN_LIKE_ONE_OF_YOUR_FRENCH_GIRLS`.

### DB_Secret

This flag also involves the Paperbots application, and is available to us once we've figured out how to log in successfully. Now, we need to extract a `DB_Secret` from an SQL database that the application uses. The `init_db()` function in the [source code](./files/ctf_files/wee_server.py "Source code for the application") shows that the `DB_SECRET` value is stored into the `secrets` table in the database as the `secret` value.

```python
def init_db():
    with app.app_context():
        db = get_db()
        with open(MIGRATION_PATH, "r") as f:
            db.cursor().executescript(f.read())
        db.execute("CREATE TABLE `secrets`(`id` INTEGER PRIMARY KEY AUTOINCREMENT, `secret` varchar(255) NOT NULL)")
        db.execute("INSERT INTO secrets(secret) values(?)", (DB_SECRET,))
        db.commit()
```

Looking at the `/api/getprojectsadmin` endpoint reveals a possible SQL injection, as an HTTP POST request to this API will take an `offset` value and use it directly in an SQL query without any input validation.

```python
# Admin endpoints
@app.route("/api/getprojectsadmin", methods=["POST"])
def getprojectsadmin():
    # ProjectsRequest request = ctx.bodyAsClass(ProjectsRequest.class);
    # ctx.json(paperbots.getProjectsAdmin(ctx.cookie("token"), request.sorting, request.dateOffset));
    name = request.cookies["name"]
    token = request.cookies["token"]
    user, username, email, usertype = user_by_token(token)

    json = request.get_json(force=True)
    offset = json["offset"]
    sorting = json["sorting"]

    if name != "admin":
        raise Exception("InvalidUserName")

    sortings = {
        "newest": "created DESC",
        "oldest": "created ASC",
        "lastmodified": "lastModified DESC"
    }
    sql_sorting = sortings[sorting]

    if not offset:
        offset = datetime.datetime.now()

    return jsonify_projects(query_db(
        "SELECT code, userName, title, public, type, lastModified, created, content FROM projects WHERE created < '{}' "
        "ORDER BY {} LIMIT 10".format(offset, sql_sorting), one=False), username, "admin")
```

To be able to access this resource, we have to be logged in as admin, so we can use the `/api/login` endpoint to get the verification code for the admin account and then `/api/verify` to get the necessary value for the token cookie. Setting the token cookie and setting the name cookie to "admin" will let us get access to the SQL injection. Now, we need to create the actual string we'll be injecting.

The offset parameter is what we'll be exploiting, since the `sortings` parameter only has three different options, none of which we can define ourselves. As the SQL query used in `api/getprojectsadmin` accesses the `projects` table and we want to get at the `secrets` table, we'll use a `UNION` statement. The `UNION` statement needs the same amount of result columns on both sides of it, so we'll use `UNION SELECT secret, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM secrets` to make the statement valid. Then, we'll add a Python datetime string to the front so that the initial SQL query runs successfully, and we'll add a single quotation mark in between to allow us to escape from the query. Adding `--` to the end will comment out everything after our injection, and we've got a complete SQL injection of `2019-01-03 02:15:00.002180' UNION SELECT secret, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM secrets --`

A [Python script](./files/flag_scripts/dbsecret.py "Python script to get the flag") I wrote will automate this whole process and display our flag of `35C3_ALL_THESE_YEARS_AND_WE_STILL_HAVE_INJECTIONS_EVERYWHERE__HOW???`

### McDonald

The description for this web challenge was that `Our web admin name's "Mc Donald" and he likes apples and always forgets to throw away his apple cores..`. Going to the web server at `http://35.207.132.47:85` reveals a pretty empty web page that just displays the description. The source code didn't have anything interesting in it, so I checked out the `/robots.txt` file and found an entry of `Disallow: /backup/.DS_Store`. Going to that file downloads a [.DS_Store](./files/ctf_files/DS_Store "The .DS_Store file") file. This file is a special Mac file that contains the metadata for the containing folder, so if we can read it, we'll get information about the backup folder.

Using the [ds_store](https://ds-store.readthedocs.io/en/latest/ "ds_store Python library") Python library, we can get a listing of the folders within `/backup`. We find that there are multiple folders named `/a`, `/b`, and `/c`, and if we go to them, we get an HTTP 403 Forbidden error, meaning that the folder exists but we can't access it. Trying different combinations such as `/a/b/c` continues to give 403 errors, but when you try to go four layers deep, such as `/a/b/c/a`, we end up with HTTP 404 Not Found errors, meaning that we have a maximum depth of 3 and thus 18 potential folders to go through.

I put together a [Python script](./files/flag_scripts/mcdonald.py "Python script to get the flag") that will go through each combination of folders until it finds a file called `flag.txt` and then prints out the contents. Running it reveals that the flag is inside `/backup/b/a/c` and is `35c3_Appl3s_H1dden_F1l3s`

### Not(e) accessible

This challenge provides us with a web server at [http://35.207.132.47:90/](http://35.207.132.47:90/ "The web server") that will store text we give it and allow us to view the text stored. We can get the source code for the frontend and backend at the [/src.tgz](http://35.207.132.47:90/src.tgz "Download the source code") file.

Looking through this, we see in the [frontend/index.php](./files/ctf_files/note_index.php "index.php file") file that the ID we get for our note is randomly generated, and that the password for each note is just its MD5 hash.

```php
$id = random_int(PHP_INT_MIN, PHP_INT_MAX);
$pw = md5($note);
        
# Save password so that we can check it later
file_put_contents("./pws/$id.pw", $pw); 

file_get_contents($BACKEND . "store/" . $id . "/" . $note);
```

That `file_get_contents()` call is interesting because to store the note in the backend, the frontend tries to read the contents of a different file. To see how it does so, let's look at the [backend](./files/ctf_files/note_backend.rb "Backend Ruby file")

```ruby
require 'sinatra'
set :bind, '0.0.0.0'

get '/get/:id' do
	File.read("./notes/#{params['id']}.note")
end

get '/store/:id/:note' do 
	File.write("./notes/#{params['id']}.note", params['note'])
	puts "OK"
end 

get '/admin' do
	File.read("flag.txt")
end
```

So it looks like the backend is actually a seperate server that the frontend talks with. If the frontend sends an HTTP GET request to `/store`, the backend will store the note, and a GET request to `/get` will read the contents of the note. To get our flag, we'll need to get the frontend to send a GET request to `/admin` which will read the contents of `flag.txt`.

The [frontend/view.php](./files/ctf_files/note_view.php "view.php file") is where we get our vulnerability.

```php
$id = $_GET['id'];
if(file_exists("./pws/" . (int) $id . ".pw")) {
    if(file_get_contents("./pws/" . (int) $id . ".pw") == $_GET['pw']) {
        echo file_get_contents($BACKEND . "get/" . $id);
```

`view.php` will take the `id` parameter passed in and then check to see if it's a valid ID by casting it to an integer. However, when it callse the backend to read the note, the ID is not cast to an integer, meaning that we can manipulate the ID parameter as we need. In particular, if we take a valid ID, add `/../../admin` to it, the backend will get a request for `/admin`, as seeing `/get/id/../../admin` is equivalent to a request to `/admin` due to the directory traversal we performed with the `../`s.

I put together a [Python script](./files/flag_scripts/note.py "Python script to get the flag") that will get a valid ID and then print out the flag of `35C3_M1Cr0_S3rvices_4R3_FUN!`
