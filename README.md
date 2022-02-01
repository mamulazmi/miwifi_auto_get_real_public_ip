# Intro
For Internet penetration. Only Mi WiFi Router. and Update IP to cloudflare


# Attention
please copy .env.example to .env and populate all information before run this library


# Usage
run `python3 main.py reload` to check if you have public ip, if not router it self will redial pppoe it self and update to cloudflare DNS account

or run `python3 main.py get_ip` to get the ip only once.

# Dependency
`Python 3` and `requests` and `cloudflare` library

`pip3 install requests` for installing `requests`
`pip3 install cloudflare` for installing `cloudflare`

or install using requirement.txt
`pip3 install -r requirement.txt`

# Thanks
[Py Mi WiFi](https://github.com/sbilly/pyMiWiFi)
utils.py partly from this repo.

and thanks for LollipopKit for first developing this libary

# License
```
Apache License 2.0
```