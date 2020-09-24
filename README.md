# PyLoadCentral
Python wrapper for [Loadcentral](http://loadcentral.com.ph/) Loading API

This is based on this LC API wrapper for Node.js [repo](https://github.com/johnbailon/loadcentraljs/blob/master/index.js)

### Basic Usage:
```python
from pyloadcentral import LoadCentral
import os

# Define account costants
UID = os.getenv("UID") 
PASSWORD = os.getenv('PASSWORD')

# Instantiate
lc = LoadCentral(UID, PASSWORD)

# Generate random code
rrn = 'XYZ' + str(math.floor(random() * (10000000000) + 1000))

## TEST

# Sell Load
lc.sell({
  'pcode': 'ZTEST1', # LoadCentral product code (See list of valid codes on their admin dashboard)
  'to': '09231234567', # Load recipient number
  'rrn': rrn
})

# Inquire transaction status using the generated RRN
# This also returns account balance and other info
message = lc.inquire(rrn)
print(message)

# Sample Output
# <RRN>XYZ468024420</RRN><RESP>0</RESP><EBAL>613.4603</EBAL><TID>15871700</TID><RET>0</RET><REF>WB0875250628</REF><EPIN>PIN1 125865 PIN2 656730</EPIN><ERR>Success</ERR>
```

### TODO:
* Parse ```lc.inquire``` return message
