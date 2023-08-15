# Troubleshooting guide

## /usr/include/stdlib.h:26:10: fatal error: bits/libc-header-start.h: No such file or directory
Also ``/usr/include/math.h:27:10: fatal error: bits/libc-header-start.h: No such file or directory``

Run ``sudo apt-get install gcc-multilib``
See this [stackoverflow answer](https://stackoverflow.com/a/54082790/).

## /usr/bin/ld: cannot find dummy/path: No such file or directory collect2: error: ld returned 1 exit status
This should not happen. Please share how you managed to accomplish this. 

## Builder script returned non-zero ([code]) error code. For troubleshooting guide, go to [...]
This can be caused by variety of issues, please look up in the console output, to which category your case applies:

### Couldn't detect any supported C compilers on your system. Check if your compiler is on the system PATH.
Make sure that you have GCC/NinGW/MSVC compiler installed on your machine. This error shows up because, there's no binary release for your system,
so automatic building program tries to build from source. Without proper c compiler installed, it fails.

## No built binaries found for architecture [architecture]. For troubleshooting guide, go to [...]
nova_builder.py script currently only builds for x86/x86_64. You can also try to build Nova Physics from source, clone this repository and put the binary in nova-binaries/ using proper path format:
``nova-binaries/[operating system]/lib/[architecture]/libnova.*``

---
In case of other errors, feel free to open a nwe issue, containing the error, system info or anything else that could help resolve this issue. 