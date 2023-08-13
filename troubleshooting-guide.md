# Troubleshooting guide

## /usr/include/stdlib.h:26:10: fatal error: bits/libc-header-start.h: No such file or directory
Also ``/usr/include/math.h:27:10: fatal error: bits/libc-header-start.h: No such file or directory``

Run ``sudo apt-get install gcc-multilib``
See this [stackoverflow answer](https://stackoverflow.com/a/54082790/).
---
In case of other errors, feel free to open a nwe issue, containing the error, system info or anything else that could help resolve this issue. 