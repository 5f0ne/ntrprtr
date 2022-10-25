# Description

Interpret bytes through different customizable actions

# Configuration

In order to interpet the given bytes, you need to provide a ´.json´ file
with the following structure:

```json
[
    {
        "name": "Enter the name here..",
        "description": "Provide description here..",
        "start": 0,  // The start byte from where you want to interpret
        "end": 10,   // The end byte where interpreting shall stop
        "action": [   
                     // --> Specify as many actions as you want.
                     // --> Each action will be applied to the specified bytes
                     // --> The actions are specified below.
                     // --> You do not need to provide an action.
        ]
    }
]
```
The following actions are available:

```json
// Get the decimal value of the given bytes.
// Specify if you want to interpret it as little or big endian
{
    "type": "decimal",
    "endianess": "little|big" // Default: little
}

// Get the binary value of the given bytes.
// Specify if you want to interpret it as little or big endian
{
    "type": "binary",
    "endianess": "little|big" // Default: little
}

// Get the ascii representation of the given bytes.
// If a non ascii value is there, specify a placeholder
{
    "type": "ascii",
    "nonAsciiPlaceholder": "." // Default: .
}

// Get the unicode representation of the given bytes.
{
    "type": "unicode"
}

// Provides a hexdump for the given bytes
// If a non ascii value is there, specify a placeholder
{
    "type": "hexdump",
    "nonAsciiPlaceholder": "." // Default: .
}

// Compare the given bytes against your own values:
// Specify if you want to interpret it as little or big endian
// Specify a result if there is no match
{
    "type": "equals",
    "endianess": "little|big", // Default: big
    // Add as many objects as you want to the "cmp" list
    "cmp": [{
                // The value you want to compare with the given bytes
                "value": "1D1E", 
                // A description which will be added to the result, 
                // if the given bytes matches "value"         
                "description": "Compare 1"      
            },{
                "value": "1D1",
                "description": "Compare 2"
            }],
    // The result if there was no match 
    "noMatch": "No Match found!" // Default: No match found!
}

// Compare the bits of the given bytes against your own values
// Important: Provide leading zeros
// Specify if you want to interpret it as little or big endian
// Specify a result if there is no match
{
    "type": "bitequals",
    "endianess": "little|big", // Default: big
    // Add as many objects as you want to the "cmp" list
    "cmp": [{
                // The bits you want to compare
                "value": "01110111",
                // Description to be added to the result,
                // if bits machtes "value"
                "description": "Bits are equal"
            }],
    // The result if there was no match 
    "noMatch": "Bits are not equal!" // Default: No match found!
}

// Interprets 2 Bytes as DOS time - format hour:minute:seconds
// Specify if you want to interpret it as little or big endian
{
    "type": "dostime",
    "endianess": "little|big" // Default: little
}

// Interprets 2 Bytes as DOS date - format day.month.year
// Specify if you want to interpret it as little or big endian
{
    "type": "dosdate",
    "endianess": "little|big" // Default: little
}
```

Just add as many interpreting objects as you want to the list. The output is a list of tuples. Look at the example section for an overview.


# Installation

`pip install ntrprtr`

# Example

Given bytes to interpret:

```
00 01 02 03 04 04 06 07 08 09 0A 0B 0C 0D 0E 0F 
68 61 6C 6C 6F 20 77 6F 72 6C 64 1B 1C 1D 1E 1F
43 B7 67 42 00 00 00 00 00 00 00 00 00 00 00 00
79 00 5F 00 30 00 31 00 2E 00 6A 00
```

Use the following `config.json`:

```json
[
    {
        "name": "first-byte-with-no-action",
        "description": "No action",
        "start": 0,
        "end": 2
    },
    {
        "name": "first-bytes",
        "description": "First three bytes",
        "start": 0,
        "end": 2,
        "action":[
            {
                "type": "decimal",
                "endianess": "big"
            }
        ]
    },
    {
        "name": "bin-bytes",
        "description": "Binary bytes",
        "start": 2,
        "end": 3,
        "action": [
            {
                "type": "binary",
                "endianess": "little"
            }
        ]
    },
    {
        "name": "ascii-bytes",
        "description": "Ascii values",
        "start": 16,
        "end": 26,
        "action": [
            {
                "type": "ascii",
                "nonAsciiPlaceholder": "."
            }
        ]
    },
    {
        "name": "hexdump-bytes",
        "description": "Hexdump values",
        "start": 0,
        "end": 3,
        "action": [
            {
                "type": "hexdump",
                "nonAsciiPlaceholder": "."
            }
        ]
    },
    {
        "name": "equals-bytes",
        "description": "Test equals",
        "start": 29,
        "end": 30,
        "action": [
            {
                "type": "equals",
                "endianess": "big",
                "cmp": [
                    {
                        "value": "1D1E",
                        "description": "Compare 1"
                    },
                    {
                        "value": "1D1",
                        "description": "Compare 2"
                    }
                ],
                "noMatch": "No Match found!"
            }
        ]
    },
    {
        "name": "bitEquals",
        "description": "Bit equality",
        "start": 22,
        "end": 22,
        "action": [ 
            // This is an example for multiple actions applied to bytes.
            // It shall first provide the binary value of the given bytes
            // and shall check if they equal to the given bits
            {
                "type": "binary",
                "endianess": "big"
            },
            {
                "type": "bitequals",
                "endianess": "big",
                "cmp": [
                    {
                        "value": "01110111",
                        "description": "Bits are equal!"
                    }
                ],
                "noMatch": "Bits are not equal!"
            }
        ]
    },
    {
        "name": "dos-time-bytes",
        "description": "DOS time bytes",
        "start": 32,
        "end": 33,
        "action": [
            {
                "type": "dostime",
                "endianess": "little"
            }
        ]
    },
    {
        "name": "dos-date-bytes",
        "description": "DOS date bytes",
        "start": 34,
        "end": 35,
        "action": [
            {
                "type": "dosdate",
                "endianess": "little"
            },
            {
                "type": "dostime",
                "endianess": "little"
            }
        ]
    },    
    {
        "name": "unicode-bytes",
        "description": "unicode repr.",
        "start": 48,
        "end": 59,
        "action": [
            {
                "type": "unicode"
            }
        ]
    }
]
```

Use it programmatically:

```python
import json

from ntrprtr.ByteInterpreter import ByteInterpreter
from ntrprtr.printer.Printer import Printer

configPath = "config.json"
pathToFile = "example.dd" # Contains the above bytes


fileHandle = open(pathToFile, "rb")
testBytes = fileHandle.read()

configHandle = open(configPath, encoding="utf8")
config = json.load(configHandle)

b = ByteInterpreter(testBytes, config)
result = b.interpret()

# If you want a standard output use Printer
p = Printer()
p.print(result)
```

The result is a list of tuples:
```python
[
    #       Result: [0] = Name, [1] = Description, [2] = Start Byte, [3] = End Byte, [4] = Bytes, [5] = List(ActionResult)
    # ActionResult: [0] = Type, [1] = Result
    ('first-byte-with-no-action', 'No action', 0, 2, bytearray(b'\x00\x01\x02'), [('None', '-')])
    ('first-bytes', 'First three bytes', 0, 2, bytearray(b'\x00\x01\x02'), [('decimal', 258)]), 
    ('bin-bytes', 'Binary bytes', 2, 3, bytearray(b'\x02\x03'), [('binary', '0000 0011 0000 0010')]), 
    ('ascii-bytes', 'Ascii values', 16, 26, bytearray(b'hallo world'), [('ascii', 'hallo world')]), 
    ('hexdump-bytes', 'Hexdump values', 0, 3, bytearray(b'\x00\x01\x02\x03'), [('hexdump', 'see below')]), 
    ('equals-bytes', 'Test equals', 29, 30, bytearray(b'\x1d\x1e'), [('equals', 'Compare 1')]), 
    ('bitEquals', 'Bit equality', 22, 22, bytearray(b'w'), [('binary', '0111 0111'), ('bitequals', 'Bits are equal!')]), 
    ('dos-time-bytes', 'DOS time bytes', 32, 33, bytearray(b'C\xb7'), [('dostime', '22:58:6')]), 
    ('dos-date-bytes', 'DOS date bytes', 34, 35, bytearray(b'gB'), [('dosdate', '7.3.2013')]), 
    ('unicode-bytes', 'unicode repr.', 48, 59, bytearray(b'y\x00_\x000\x001\x00.\x00j\x00'), [('unicode', 'y_01.j')])]


```
The output from printer looks like the following:

```

--> No action
    --------------
    Start Byte: 0
      End Byte: 2
    --------------
     Bytes: 
            00 01 02
    --------------
    Action: 
            none
    Result: 
            -


--> First three bytes
    --------------
    Start Byte: 0
      End Byte: 2
    --------------
     Bytes: 
            00 01 02
    --------------
    Action: 
            decimal
    Result: 
            258


--> Binary bytes
    --------------
    Start Byte: 2
      End Byte: 3
    --------------
     Bytes: 
            02 03
    --------------
    Action: 
            binary
    Result: 
            0000 0011 0000 0010


--> Ascii values
    --------------
    Start Byte: 16
      End Byte: 26
    --------------
     Bytes: 
            68 61 6C 6C 6F 20 77 6F 72 6C 64
    --------------
    Action: 
            ascii
    Result: 
            hallo world


--> Hexdump values
    --------------
    Start Byte: 0
      End Byte: 3
    --------------
     Bytes: 
            See below
    --------------
    Action: 
            hexdump
    Result: 

              Offset   00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F    ASCII           
            --------   -----------------------------------------------    ---------------- 
                   0   00 01 02 03                                        ....             
            


--> Test equals
    --------------
    Start Byte: 29
      End Byte: 30
    --------------
     Bytes: 
            1D 1E
    --------------
    Action: 
            equals
    Result: 
            Compare 1


--> Bit equality
    --------------
    Start Byte: 22
      End Byte: 22
    --------------
     Bytes: 
            77
    --------------
    Action: 
            binary
    Result: 
            0111 0111
    --------------
    Action: 
            bitequals
    Result: 
            Bits are equal!


--> DOS time bytes
    --------------
    Start Byte: 32
      End Byte: 33
    --------------
     Bytes: 
            43 B7
    --------------
    Action: 
            dostime
    Result: 
            22:58:6


--> DOS date bytes
    --------------
    Start Byte: 34
      End Byte: 35
    --------------
     Bytes: 
            67 42
    --------------
    Action: 
            dosdate
    Result: 
            7.3.2013
    --------------
    Action: 
            dostime
    Result: 
            8:19:14


--> unicode repr.
    --------------
    Start Byte: 48
      End Byte: 59
    --------------
     Bytes: 
            79 00 5F 00 30 00 31 00 2E 00 6A 00
    --------------
    Action: 
            unicode
    Result: 
            y_01.j
```

# License

MIT