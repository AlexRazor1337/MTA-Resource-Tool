# MTA Resource Tool

This tool was created to help working with MTA:SA resources. It is written In Python and using only standard libraries.
At the moment it can compile single file or whole resource using **luac_mta.exe**

## Getting Started

1. Download this script
2. [Download luac_mta.exe ](http://luac.mtasa.com/files/windows/x86/luac_mta.exe)
3. Place it in a folder with main script

To compile a resource you must call script with full path of resource folder as argument, see examples.
After compiling, resource will appear at folder Compiled Resources in script directory. If you are compiling single file, then it will appear at script directory.

To generate meta for folder you must call script with full path of resource folder as argument, see examples.
Script will determine file type by few rules: prefixes **c_, s_**, folder name(client, server), file name having client or server in it. If file type cannot be determined it will be set as shared. There is an option of manual type determining, for this set 'manual' to True. In the process of generating you will be asked about file type(it's enough to type **c** or **s**). At the end you will get **meta-generated.xml at folder you have specified to generate meta from**
## Examples

This will compile single resource:
```
 main.py D:\Resources\ResourceToCompile
```

Compiling single file:
```
 main.py D:\Resources\example.lua
```

Generate meta file for folder:
```
 meta.py D:\Resources\ResourceToCompile
```
### Prerequisites

This script should work with any Python 3.*, no non-standard libraries are used.

## Credits

**AlexRazor** - main tool code  
**MTA:SA Team** - luac_mta.exe and of course, [MTA:SA itself](https://github.com/multitheftauto/mtasa-blue)
