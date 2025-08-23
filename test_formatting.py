def badly_formatted_function( ):
    x=1+2
    y = 3   +   4
    if x==y:
        print("this has bad formatting")
        return False
    else:
        return True

# This should trigger formatting fixes
