<h1 align="center">
  <br>
  <a href="https://github.com/veilwr4ith/RevShellz2.0"><img src="https://github.com/veilwr4ith/RevShellz2.0/blob/main/banner.png" alt="RevShellz
"></a>
</h1>

# RevShellz2.0
Initially developed by mkdirlove and enhanced by me (veilwr4ith), is a reverse shell payload generator compatible with Linux, Windows, and macOS. The updated version includes new features such as Base64 and URL encoding for payloads, which helps avoid straightforward detection by making them less immediately recognizable. This is particularly useful for Capture The Flag (CTF) challenges with payload restrictions. Additionally, I've incorporated various payloads into the tool's dictionary, including Python-based payloads, Lua, and msfvenom options for Metasploit.


## [+] Installation

Copy-paste this into your terminal:

```sh
git clone https://github.com/veilwr4ith/RevShellz
```
```
cd RevShellz
```
```
chmod +x revshellz2.0.py
```
```
python3 revshellz2.0.py
```
or
```
./revshellz2.0.py 
```

## [+] Usage
``` 
   _ \                  ___|   |            |  |
  |   |   _ \ \ \   / \___ \   __ \    _ \  |  | _  /
  __ <    __/  \ \ /        |  | | |   __/  |  |   /
 _| \_\ \___|   \_/   _____/  _| |_| \___| _| _| ___|v2.0
                            mkdirlove & veilwr4ith

usage: revshellz2.0.py [-h] [-ip IPADDRESS] [-p PORT] [-os OPERATING_SYSTEM] [-pl PAYLOAD] [-l LIST] [-enc ENCODE]

RevShellz: Yet another reverse shell generator written in Python.

options:
  -h, --help            show this help message and exit
  -ip IPADDRESS, --ipaddress IPADDRESS
                        Target IP address
  -p PORT, --port PORT  Target port number
  -os OPERATING_SYSTEM, --operating-system OPERATING_SYSTEM
                        Target operating system (linux, windows, macos)
  -pl PAYLOAD, --payload PAYLOAD
                        Payload for reverse shell
  -l LIST, --list LIST  List available reverse shell payload types for the specified OS
  -enc ENCODE, --encode ENCODE
                        Encode the payload in Base64 or URL

```
## [+] Example

Listing reverse shells
```
python3 revshellz2.0.py -l linux, windows, macos
```

Generating reverse shell for Linux
```
python3 revshellz2.0.py -ip 10.10.10.1 -p 1337 -rs 'bash -i' -os linux
```

Generating reverse shell for Windows
```
python3 revshellz2.0.py -ip 10.10.10.1 -p 1337 -rs 'powershell #1' -os windows
```

Generating reverse shell for MacOS
```
python3 revshellz2.0.py -ip 10.10.10.1 -p 1337 -rs 'nc mkfifo' -os macos
```

Generating reverse shell with Base64 Encoding
```
python3 revshellz2.0.py -ip 10.10.10.1 -p 1337 -rs 'bash -i' -os linux -enc base64
```

Generating reverse shell with URL Encoding
```
python3 revshellz2.0.py -ip 10.10.10.1 -p 1337 -rs 'bash -i' -os linux -enc url
```
