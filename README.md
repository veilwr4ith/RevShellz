<h1 align="center">
  <br>
  <a href="https://github.com/veilwr4ith/RevShellz2.0"><img src="https://github.com/veilwr4ith/RevShellz2.0/blob/main/logo.png" alt="RevShellz
"></a>
  <br>
  Yet another reverse shell generator written in Python.
  <br>
</h1>

#### Installation

Copy-paste this into your terminal:

```sh
git clone https://github.com/veilwr4ith/RevShellz
```
```
cd RevShellz
```
```
python3 revshellz2.0.py
```
or
```
python3 revshellz2.0.py -h
```
#### Usage
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
#### Example

Listing reverse shells
```
python3 revshellz2.0.py -l linux, windows, macos
```

#### Example

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
