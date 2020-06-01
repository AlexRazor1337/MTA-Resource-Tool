# MTA Resource Tool

This tool was created to help working with MTA:SA resources. It is written In Python and using only standard libraries.
At the moment it can compile single file or whole resource using **luac_mta.exe** and generate meta files for folders.

## Getting Started

1. Download this script
2. Run install-luac.bat

To compile a resource you must call script with full path of resource folder as argument, see examples.
After compiling, resource will appear at folder Compiled Resources in script directory. If you are compiling single file, then it will appear at script directory.

To generate meta for folder you must call script with full path of resource folder as argument, see examples.
At the end you will get **meta-generated.xml at folder you have specified to generate meta from**.

List of functional:
1. Compile all script files in resource folder and copy all other files if they don't have restricted extension(empty by default). 
  - Automaticly rename all compiled files extension in meta(.lua to .luac)
  - You can change obfuscation level
  - Ignore folders starting with ".", e.g ".git"
  - Use different info levels for information output(where 0 is showing all levels, 1 only important info, 2 is warning and error only)
2. Generate meta file and place it to the folder.
  - Automatic script type determination, by default, based on a few rules: prefixes **c_, s_**, folder name(client, server), file name having "client" or "server" in it. If file type can't be determined, it will be set to "shared".
  - You can add new prefixes and file/folder substrings in a config.
  - Option of manual type determining, for this set 'manual' in config to True. In the process of generating you will be asked about file type(it's enough to type **c** or **s**). 
  - You can add restricted extensions, so files with them won't be added to meta file. 
  - You can add specific files to be ignored.
  - You can set field "author" that will be in meta file.
  - You can enable and disable caching of client script files(disabled by default).
  - You can enable overwriting of old meta file in config(so new file will be named as "meta.xml" and not "meta-generated.xml"), but old meta file still will be saved as ".meta-old xml" + timecode of operation. You will be asked about overriding meta each time because of safety reasons.
  - You can enable force overwrite and it wan't ask you about overwriting meta, useful for automation.
  - You can enable or generating of [exported functions](https://wiki.multitheftauto.com/wiki/Call). For this to work, you must add "--exported" to the function header line, example:
  ```lua
     function foo() --exported
     end
  ```
  - Ignore files and folders starting with ".", e.g ".git"
  - Use different info levels for information output
  - You can create file "resource.json" which contains info about resource and used in meta generation. It's must be placed in resource root folder. Currently supported "oop", "aclrights", "author", "description". Here is example of such file:
```json
     {
      "author": "Default",
      "description": "This is test resource to demonstrate tool functional",
      "oop": true,
      "rights": {
        "general.ModifyOtherObjects": true, 
        "function.startResource": false
      }
    }
```
  
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

Also you can look at example resource in folder "testResource", it contains "resource.json" example and demonstrates all main functional of this tool.

### Prerequisites

This script should work with any Python 3.*, no non-standard libraries are used.

## Credits

**AlexRazor** - main tool code  
**MTA:SA Team** - luac_mta.exe and of course, [MTA:SA itself](https://github.com/multitheftauto/mtasa-blue)
