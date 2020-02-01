# MTA Resource Tool

This tool was created to help working with MTA:SA resources. It is written In Python and using only standard libraries.
At the moment it can compile single file or whole resource using **luac_mta.exe**

## Getting Started

1. Download this script
2. Download luac_mta.exe 
3. Place it in a folder with main script

To compile a resource you must call script with full path of resource folder as argument, see examples.

## Examples

This will compile single resource:
```
 main.py D:\Resources\ResourceToCompile
```

Compiling single file:
```
 main.py D:\Resources\example.lua
```
### Prerequisites

This script should work with any Python 3.*, no non-standard libraries are used.

## Credits

**AlexRazor** - main tool code  
**MTA:SA Team** - luac_mta.exe and ofcourse MTA:SA itself
