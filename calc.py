def calculate(string):
    if not string:
        return 0
        
    string = string.replace(" ", "")
    if string == "":
        return 0
        
    num, index, valid_equation, error_reason = equation(string, 0)
    if not valid_equation:
        return error_reason
        
    if num % 1 > 0:
        return num
    else:
        return int(num)

def equation(string, i, open_parenthesis = False):
    stack = []
    current_num = ''
    operation = '+'
    close_parenthesis = False
    while i < len(string):
        char = string[i]
            
        if not char.isdigit() and char != '.' and char != '(' and char != '+' and char != '-' and char != '*' and char != '/' and char != ')':
            return None, None, False, "Invalid Input"   #if invalid char, return False
            
        if char.isdigit() or char == '.':
            current_num += char
            
        elif char == '(':
            num, index, valid_equation, error_reason = equation(string, i+1, open_parenthesis = True)    #get the result in the parentheses and index of ')'
            if not valid_equation:
                return None, None, False, error_reason  #if not valid equation, return the error msg
                
            current_num = str(num)
            i = index
            
        if char == '+' or char == '-' or char == '*' or char =='/' or i == len(string)-1 or char == ')':
            #when encountering an operater, push the number before that operater into the stack
            if current_num:
                if current_num == '-':
                    return None, None, False, 'Syntax Error'    #if there is '-' in front, no more operater is allowed
            
                num = float(current_num)
                if operation == '-':
                    stack.append(-num)
                    
                elif operation == '+':
                    stack.append(num)
                    
                elif operation == '*':  #for * or /, multiply or divide the last number in the stack with the number. And push the result into the stack
                    stack.append(stack.pop() * num)
                    
                elif operation == '/':
                    stack.append(stack.pop() / num)
                
                operation = char
                current_num = ''
            else:
                if char == '-':
                    current_num +=  char
                
                else:
                    return None, None, False, 'Syntax Error'    #after the operater current_num becomes '', only '-' can be the first char of current_num
            
            if char == ')':
                close_parenthesis = True
                break
            
        i+=1
        
    if open_parenthesis and not close_parenthesis or not open_parenthesis and close_parenthesis:
        return None, None, False, 'Syntax Error'    #if there is open parenthesis but no close parenthesis and vice versa, return error msg
    #print(stack)
    result = 0
    while stack:
        result += stack.pop()
        
    return result, i, True, None

def testing():
    input = ["", "1 + 2", "4*5/2", "-5+-8--11*2", "-.32       /.5", "(4-2)*3.5", "2+-+-4", "19 + cinnamon", "(1+(3-2)", "(1+4*9)", "(3-4) * ((16+4)/2)"]
    expected = [0, 3, 10, 9, -0.64, 7, "Syntax Error", "Invalid Input", "Syntax Error", 37, -10]
    for i in range(len(input)):
        result = calculate(input[i])
        if result != expected[i]:
            return False
            
    return True