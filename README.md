Disclaimer ⚠️

This tool is created for educational and security research purposes only.
Do not use it against domains or systems you do not own or have explicit permission to test.
The author (Mustafa-almohsen) takes no responsibility for misuse or damages caused by this tool.

-----------

DNS Rebinding Checker

A simple Python tool to test domains against potential DNS rebinding attacks
It allows you to check a single domain or a list of domains, and perform multiple resolution attempts to detect if the IP address changes unexpectedly.

---------
The question is --> What is DNS Rebinding?
Well DNS rebinding is an attack that tricks a victim   browser into bypassing the (SOP) Same-Origin Policy.  
It works by making a domain resolve to one IP address first then later resolve to a different IP (example-  internal/private IP) allowing the attacker to interact with internal services through the victim browser.




-----------

 Features
- Test single domain or list of domains  
- Multiple resolution attempts (customizable)  
- Colored output for readability  

---------

Usage

Single Domain:
python3 rebind_checker.py -d example.com -n 5 
#This will check example.com 5 times for DNS rebinding behavior.

List of Domains:
python3 rebind_checker.py -l domains.txt -n 10
#This will check each domain in domains.txt 10 times.

