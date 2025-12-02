"""
    IPV4 Validity

Howdy, this module is created to validate ipv4 address and to obtain valid addresses from user input 
"""

def is_valid_ipv4(ip_string):
    """

    This is to check if the string is a valid ipv4 address.


    ipstring (str) = the ipv4 address you want to validate


    returns: true if it is a valid ip or 'localhost', false if not. 
    
    want examples? why not

    >>ipstring (192.168.1.1)
    returns: true
    >>ipstring (270.0.400.1)
    returns: false

    real simple. 

    This is not a tool to determine whether the ip address is being occupied, rather it checks to see if the entered address follows the ipv4 format.

    4 octets of numbers ranging from 0-255 seperated by .'s

    have fun!
    """

    if ip_string == 'localhost':
        return True 

    octets = ip_string.split(".")

    if len(octets) != 4:
        return False 


    if not all(octet.isdigit() for octet in octets):
        return False

    if not all (0 <= int(octet) <= 255 for octet in octets):
        return False 

    return True 


def get_valid_ipv4(prompt = 'Enter your ipv4 address: ',allow_localhost=True):
    """ 

    Prompts user untill a valid IP address is entered.

    prompt(str) = custom prompt message (optional)


    allow_localhost: bool = controles whether or not to allow localhost as a valid input

    Returns:
    str: a valid IP address or 'localhost'

   """ 


    
    while True:
        
        ip_string = input(prompt).strip()

        if ip_string == 'localhost' and allow_localhost:

            return ip_string

        if is_valid_ipv4(ip_string):
            return ip_string
        else:
            print('Please enter a valid ipv4 address.')

def get_ipv4_octets(ip_string):

    """

    This splits an ipv4 address into its four octets and converts to integers.


    Args: 
        ip_string (str): a valid ip address

    Returns:

        list: list of 4 integers, none if invalid.

    """

    if not is_valid_ipv4(ip_string) or ip_string == 'localhost':
        return None
    return [int(octet) for octet in ip_string.split('.')]







if __name__ == "__main__":


    print ('Test code')

    tests = [

        ("192.168.1.1", True),
        ("10.0.0.1", True),
        ("255.255.255.255", True),
        ("0.0.0.0", True),
        ("localhost", True),
        ("256.1.1.1", False),
        ("192.168.1.999", False),
        ("192.168.1", False),
        ("192.168.1.1.1", False),
        ("abc.def.ghi.jkl", False),
        ("192.168.-1.1", False),
    ]


    for ip, expected in tests:

        result = is_valid_ipv4(ip) 
        
        if result == expected:
            status = 'true'
             
        else:
            status = 'false'

        print(f" {status} {ip} >>> {result} (expected {expected})")


    
print("\n" 'Testing get_valid_ipv4, enter some ips')

ip = get_valid_ipv4()

print (f"valid ip entered: {ip}")

if ip != 'localhost': 
   octets = get_ipv4_octets(ip)
   print (f"heres the octets: {octets}")
