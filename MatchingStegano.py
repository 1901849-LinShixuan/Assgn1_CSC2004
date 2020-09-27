# ----------------
# ++ Principles ++
# ----------------
# Lower Significant Bits Matching hides information by comparing the binary code of a cover image and its
# corresponding payload. It randomly +1 / -1 to the LSB (Pixel Value) depending on the binary value of the payload

import sys
import cv2
import numpy as np
import random

# ---- Decryption ----
def extract():
    J = cv2.imread('Stega_Example.png')                         # reads the image
    f = open('output_payload.txt', 'w+', errors = "ignore")     # Outputs secret data

    bitidx = 0
    bitval = 0
    temp = ""                               # Temp stored as decoded data
    stopCondition: bool = False             # Indicator to stop
    for i in range(J.shape[0]):
        if (I[i, 0, 0] == '-'):
            break
        if stopCondition == True:           # Breaks condition when True
            break
        for j in range(J.shape[1]):
            for k in range(3):
                if stopCondition == True:   # Breaks condition when True
                    break
                if (I[i, j, k] == '-'):
                    break
                if bitidx==8:               # Split bit index by 8-bits
                    if bitval in list(all_ascii_data):      # Checks if value matches with ascii data
                        temp+=chr(bitval)
                        bitidx=0
                        bitval=0
                    else:
                        stopCondition = True    # Stops condition when there is no ascii data left
                        break

                bitval |= (J[i,j,k]%2)<<bitidx
                bitidx+= 1

    f.write(temp)       # writes to file
    f.close()

# ---- Encryption ----
bits = []
f = open('payload.txt', 'r')            # secret data that you want to hide
blist = [ord(b) for b in f.read()]

all_ascii_data = []                     # Takes all ASCII values (to filter)
for b in blist:
    all_ascii_data.append(b)            # append into the list before writing
    for i in range(8):
        bits.append((b>>i) & 1)

I = np.asarray(cv2.imread('Example.png')) # Cover Image (to be in directory)

sign = [1, -1]
idx = 0
for i in range(I.shape[0]):
    for j in range(I.shape[1]):
        for k in range(3):
            if idx < len(bits):
                if I[i][j][k] % 2 != bits[idx]:
                    s = sign[random.randint(0, 1)]
                    if I[i][j][k]==0: s=1
                    if I[i][j][k]==255: s=-1
                    I[i][j][k]+=s
                idx += 1

cv2.imwrite('Stega_Example.png', I)     # Stego-Object after embedding (encoded image)

print("Extracting ...")
extract()
print("Completed")
