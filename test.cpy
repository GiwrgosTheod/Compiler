## DIMITRIOS GOGOS, 5085 ##
## GEORGIOS THEODOROPOULOS, 4967 ##

#int moon
#int counterFunctionCalls, earth

def max3(x,y,z):
#{
    #int m
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if x>y and x>z:
        m = x
    elif y>x and y>z:
        m = y
    else:
        m = z
    return 0

## nested function sqr ##

    def sqr(x):
    #{
        ## body of sqr ##
        global counterFunctionCalls
        counterFunctionCalls = counterFunctionCalls + 1
        return x*x
    #}

#}

def leap(year):

#{
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if year==0 and earth>=0 or year==20:
        return 1
    else:
        return 0 
#}        

   
#def main
#int i
counterFunctionCalls = 0

i = int(input())
print(i)


i = 1600
while i<=2000:
#{
    print(sqr(x))
    i = i + 400
#}

print(sqr(x))

i=1
while i<=12:
#{
   
    i = i + 1
#}

print(counterFunctionCalls)

