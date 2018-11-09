#!/usr/bin/env python3
# bars, for reference
# ▁ ▂ ▃ ▄ ▅ ▆ ▇ █

class Sparkline:
    # width is the size of the sparkline as shown on the terminal

    nullchar = '-'

    # 1 empty/None/Null  + 8 bars
    bars = [ nullchar, '_', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█' ]
    bars = [ nullchar, ' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█' ]


    def float_or_none(self,value):
        try:
            return float(value)
        except ValueError:
            return None


    def __init__(self, data=None, width=20):
        self.spark = [ None ] * width
        self.width = int(width)
        self.min = None
        self.max = None

        if data:
            i = width-len(data)

            self.spark[i:] = list(map(self.float_or_none, data))

            self.max = self.maxNone(self.spark)
            self.min = self.minNone(self.spark)

        #print(self.spark)

    def shift(self,newvalue):
        value = self.float_or_none(newvalue)
        if newvalue is not None:
            if self.min is None or newvalue < self.min:
               self.min = value
            if self.max is None or newvalue > self.max:
                self.max = value

        self.spark[:] = self.spark[1:] + [newvalue]



    def maxNone(self, L):
        return max(x for x in L if x is not None)

    def minNone(self, L):
        return min(x for x in L if x is not None)

    def data(self):
        minmax = '({},{})'.format(self.minNone(self.spark), self.maxNone(self.spark))
        return minmax + '['+ ', '. join( list ( map((lambda x: "None" if x is None else str(x)) ,  self.spark ) )) +']'

        #return '('+ str(min(self.spark)) + ',' +str(max(self.spark)) + ')' \
        #       + '['+ ', '. join( list ( map((lambda x: "None" if x is None else str(x)) ,  self.spark ) )) +']'


    def scale_number(self, unscaled, to_min, to_max, from_min, from_max):
        '''from https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio/42095130#42095130'''
        denom = from_max-from_min
        if denom == 0:
            return 0
        return (to_max-to_min)*(unscaled-from_min)/denom+to_min

    def normalize(self,x):
        '''bins a value based on max/min'''
        if x is None:
            return 0

        div = len(self.bars)-2 # take one off for the 'empty'

        return int(self.scale_number(x, 0, div, self.minNone(self.spark), self.maxNone(self.spark)))+1

    def __str__(self):

        line = []
        for x in self.spark:
            line.append(self.normalize(x))

        output = ''
        #output += '0123456789012345678901234567890\n'
        #output += ''.join(list(map(lambda x: str(x), line))) + "\n"
        output += ''.join(list(map(lambda x: self.bars[x], line)))

        return output


    def show(self, ender='\n', value = False, show_range=False):
        string = self.__str__()
        if value:
            string += ' {:.2f}'.format(self.spark[-1])
        if show_range:
            string += ' ({:.1f}-{:.1f})'.format(self.minNone(self.spark),self.maxNone(self.spark))
        sys.stdout.write(string + '\033[K\r')
        #print(string, end=ender)


    def demo(self, demotype=0):
        import random

        if demotype == 0:
            for i in range(self.width-3):
                self.shift(random.uniform(-4,33))

        elif demotype == 1:
            for i in range(self.width-3):
                self.shift(random.triangular(-4,33))

        elif demotype == 2:
            for i in range(5):
                sparkline.shift(30-i)
            for i in range(5):
                sparkline.shift(i+4)

        elif demotype == 3:
            for i in range(int(self.width/2)):
                if i %2:
                    sparkline.shift(30-i)
                else:
                    sparkline.shift(None)
            for i in range(int(self.width/2)):
                if i %2:
                    sparkline.shift(i*2+4)
                else:
                    sparkline.shift(None)



    #def __repr__(self):
    #    return '['+ ', '.join(self.spark) +']'


if __name__=='__main__':

    import curses
    import sys

    # Is it a pipe?
    # if so,do silly stuff to loop over incoming datastream
    if not sys.stdin.isatty():
        import os 
        showvalue = True
        showwidth=40
        if 'COLUMNS' in os.environ:
            showwidth=os.getenv('COLUMNS') - 10
            if showwidth < 10:
                showvalue = False


        sparkline = Sparkline(width=showwidth)

        #hide cursor
        sys.stdout.write("\033[?25l")
        try:
            while True:
                newdata = sys.stdin.readline()

                sparkline.shift( float(newdata))
                sparkline.show(ender='\r', value = showvalue, show_range=showvalue )

        except KeyboardInterrupt:
            #show cursor again
            sys.stdout.write("\033[?25h")
            #sys.stdout.write("\033[?25l" + '\n')




    # data on the CLI?
    elif len(sys.argv) > 1:
        data = sys.argv[1:]
        sparkline = Sparkline(data, width=len(data))

    # demo otherwise
    else:
        sparkline = Sparkline(width=20)
        sparkline.demo(demotype=3)

    #print(sparkline.data())
    print(sparkline)
