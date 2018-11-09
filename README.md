# spark
My silly attempt at a CLI sparkline application.

Any floating point or integral data should be valid (within more general Python constraints).

The input data will be read and mapped to 'bars' and displayed on the CLI.
Invalid values (i.e. non-numerical) will be mapped to a `-` character
to indicate the absense of valid data.

== Usage ==

Spark works in one of three modes:

=== CLI data ===

Data can be passed directly on the CLI:
    ./spark.py 3 6 3 6 4 2 4 6 foo 7 0   3 3  4  bar 1
    ▃▆▃▆▄▂▄▆-█ ▃▃▄-▁

Note the two `-` values shown:  they are due to the "foo" and "bar" strings in the data.

=== Pipe ===

Spark will attempt to read from a pipe and show a "scrolling" feed of the data.  Any floting point number should be acceptible.  This snippet, for example, dumps ping times into spark, and shows "scrolls" the data with each new datapoint.

    ping -n google.com | awk '/^[0-9]/{sub("time=","",$7); print $7; fflush()}' | ./spark.py
    ▁▁▂▄▃▅▃▃▁▆ ▆▁ ▄▃▄▁▂▂▂▂▅▅▄█▆▅▁▄▄▄▂▅▃▁▇▃▃▂ 3.090

The number at the end is the most recent data entered.


=== Demo ===    
When run without arguments, it will randomly pick one of serveral "demo"
modes to show example data.



== Notes ==
Yes, there are tons of these already.  I wanted to write one on my
own that is self-contained, and didn't want to be bothered to look
at alternatives.

This code is inspired by the 100% *AWESOME*
https://github.com/wavexx/trend program.
