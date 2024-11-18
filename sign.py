"""

Raymond Pridgen Exam 2

Should be everything in here

For question 1

All values hard coded are the ones I used to sign the message. Paper copy turned in with it for validity (signature perhaps)
"""
print("Question 1: RSA Signature\n\n")

# Large primes
p = 6719
q = 3659
n = p * q
phi = (p - 1) * (q - 1)
eA = 0

# Ext euclid
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def modular_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("MI dont exist.")
    return x % phi

eA=15011
while eA < 100000:  
    try:
        gcdVal = extended_gcd(eA, phi)
        modInv = modular_inverse(eA, phi)
        break
    except ValueError:
        eA+=1

plaintext = open("trust.txt").read()

# Convert each character to ASCII, join them into one string
long_number = int("".join(str(ord(char)) for char in plaintext))
rsa = (long_number ** eA) % n
print(f"RSA:\nPublic Key: ({eA}, {n})")
print(f"Signed: {rsa}\n\n")


#For Question 2: ElGamal
print("Question 2: ElGamal\n\n")


def primeFactors(n):
    factors = set()
    while n % 2 == 0:
        factors.add(2)
        n //= 2 # floor division
    # n must be odd at this point, so check for odd factors
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.add(i)
            n //= i
    
    if n > 2:
        factors.add(n)
    return factors

def is_primitive_root(a, p):
    if a <= 1 or a >= p:
        return False
    # what to count to
    order = p - 1
    # Get the prime factors of p - 1
    factors = primeFactors(order)
    # Check if not 1 for a ^ (p-1) / q
    for factor in factors:
        if pow(a, order // factor, p) == 1:
            return False
    return True

def find_primitive_root(p):
    if p <= 1:
        return None
    for a in range(157, p):
        if is_primitive_root(a, p):
            return a
    return None

p2 = 7057 
aProot = find_primitive_root(p2)
print(f"A primitive root of {p2} is: {aProot}")

plaintext = open("trust.txt").read()
m2 = int("".join(str(ord(char)) for char in plaintext))
a = 150
beta = (aProot ** a) % p2

secretK = 431

# Check K
while secretK < 100000:  
    try:
        gcdK = extended_gcd(secretK, (p2 - 1))
        kInv = modular_inverse(secretK, (p2 - 1))
        break
    except ValueError:
        secretK+=1

# Alice does this
#Gives Bob ability to find k 
r = (aProot ** secretK) % p2
#Messgae to send
print(f"Modular Inverse of k: {kInv}\n")
s = kInv * (m2 - (a * r)) % (p2 - 1)
print(f"Public Key: ({p2}, {aProot}, {beta})\nElGamal message: \n({m2}, {r}, {s})\n\n")


"""
For Question 3: Hash Algorithm

"""
print("Question 3: Hash Algorithm\n\n")

plaintext = open("trust.txt").read()
print("Hashing in n=30 size blocks")

plaintextMatrix = []
m3 = "".join(str(bin(ord(char)) for char in plaintext))
tempString = ""
tempList = []
for char in plaintext:
    tempString = tempString.join(str(bin(ord(char)))[2:])
    if len(tempString) >= 30:
        for char in tempString:
            tempList.append(int(char))
        plaintextMatrix.append(tempList)
        tempList = []
        tempString = ""
if tempString: # Remaining padding
    tempString = tempString.ljust(30, '0')  # Pad with zeros if less than 30
    for char in tempString[:30]:
        tempList.append(int(char))
    plaintextMatrix.append(tempList)

i = 0
finalString = ""
while i < len(plaintextMatrix):
    tempXOR = 0
    j = 0
    while j < 30:
        tempXOR = tempXOR ^ plaintextMatrix[i][j]
        j+=1
    finalString += str(tempXOR)
    i+=1
print(f"Hashed message: {finalString}")

asciiString = ''.join(chr(int(finalString[i:i+8], 2)) for i in range(0, len(finalString), 8))

print(f"ASCII String: {asciiString}",end="")