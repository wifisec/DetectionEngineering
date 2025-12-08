import re
ip_addresses = ["tomcat" "CAT", "cat", "CaT", "10.3.200.23", "192.168.100.1", "192.168.100.12", "703-622-0467", "123-22-3367"]
re_ip = re.compile(r"^\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}$")
re_phone  = re.compile(r"^(\d{3})\-\d{3}\-\d{4}$")
re_ssn = re.compile(r"^\d{3}\-\d{2}\-\d{4}$")
re_cat = re.compile(r"^\b\w{3}\b$", re.IGNORECASE)
for input in ip_addresses:
    ip_match = re.search(re_ip, input)
    phone_match = re.search(re_phone, input)
    ssn_match = re.search(re_ssn, input)
    cat_match = re.search(re_cat, input)
    if ip_match:
        print(ip_match.group())
    elif phone_match:
        print(phone_match.group())
        print(phone_match.group(1))
    elif ssn_match:
        print(ssn_match.group())
    elif cat_match:
        print(cat_match.group())
#https://www.geeksforgeeks.org/python/re-compile-in-python/
# How \b works:
# Start of a word: \bword matches "word" only when it is at the beginning of a word. For example, \bcat would match "cat" in "catfish" or "a cat", but not in "tomcat" or "catatonic".
# End of a word: word\b matches "word" only when it is at the end of a word. For example, cat\b would match "cat" in "tomcat" or "a cat", but not in "catfish" or "catatonic".
# Whole word: \bword\b matches "word" only when it is a complete, standalone word. For example, \bcat\b would match "cat" in "a black cat" but not in "catfish" or "catatonic". 
