#!/bin/sh
awk 'BEGIN{x=0;}END {while (1) {print sin(x); x+=.31415296; system("/bin/sleep .05"); }  }' < /dev/null
