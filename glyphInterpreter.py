import sys

s = {}
emojiNumbers = {"✊" : 0, "☝" : 1, "✌" : 2, "🤟" : 3, "🖖" : 4, "🖐" : 5, "👌" : 6, "🤘" : 7, "🙏" : 8, "🤞" : 9}

ifStatementValues = [] # -1 = There was a false if statment found before, 0 = False, 1 = True, 2 = Our true statement was already executed so skip all this

ifStatementTrue = False

def eval_expr(expr):
    return expr

def varmap(var, s):
    return s[var]

def eval_var(var, s):
    if var in s:
        return varmap(var, s)
    else:
        raise Exception(f"The variable, '{var}', is not defined at line {lineNumber}")

def add(val):
    o1, o2 = val.split('+')

    o1 = o1.strip()
    o2 = o2.strip()

    if not o1.isdigit():
        o1 = eval_var(o1, s)
    if not o2.isdigit():
        o2 = eval_var(o2, s)
    
    return int(o1) + int(o2)

def sub(val):
    o1, o2 = val.split('-')

    o1 = o1.strip()
    o2 = o2.strip()

    if not o1.isdigit():
        o1 = eval_var(o1, s)
    if not o2.isdigit():
        o2 = eval_var(o2, s)
    
    return int(o1) - int(o2)

def divide(val):
    o1, o2 = val.split('/')

    o1 = o1.strip()
    o2 = o2.strip()

    if not o1.isdigit():
        o1 = eval_var(o1, s)
    if not o2.isdigit():
        o2 = eval_var(o2, s)
    
    return int(o1) / int(o2)

def multiply(val):
    o1, o2 = val.split('*')

    o1 = o1.strip()
    o2 = o2.strip()

    if not o1.isdigit():
        o1 = eval_var(o1, s)
    if not o2.isdigit():
        o2 = eval_var(o2, s)
    
    return int(o1) * int(o2)

def mod(val):
    o1, o2 = val.split('%')

    o1 = o1.strip()
    o2 = o2.strip()

    if not o1.isdigit():
        o1 = eval_var(o1, s)
    if not o2.isdigit():
        o2 = eval_var(o2, s)
    
    return int(o1) % int(o2)

def power(val):
    o1, o2 = val.split('^')

    o1 = o1.strip()
    o2 = o2.strip()

    if not o1.isdigit():
        o1 = eval_var(o1, s)
    if not o2.isdigit():
        o2 = eval_var(o2, s)

    return int(o1) ** int(o2)

def equal(o1, o2):
    o1 = o1.strip()
    o2 = o2.strip()

    if not o1.isdigit():
        o1 = eval_var(o1, s)
    if not o2.isdigit:
        o2 = eval_var(o2, s)

    ifStatementTrue = o1 == o2
    if ifStatementTrue == True:
        return 1
    return 0

def greaterThan(o1, o2):
    o1 = o1.strip()
    o2 = o2.strip()

    if not o1.isdigit():
        o1 = eval_var(o1, s)
    if not o2.isdigit:
        o2 = eval_var(o2, s)

    ifStatementTrue = o1 > o2
    if ifStatementTrue == True:
        return 1
    return 0

def lessThan(o1, o2):
    o1 = o1.strip()
    o2 = o2.strip()

    if not o1.isdigit():
        o1 = eval_var(o1, s)
    if not o2.isdigit:
        o2 = eval_var(o2, s)

    ifStatementTrue = o1 < o2
    if ifStatementTrue == True:
        return 1
    return 0

def eval_line(line):
    if '+' in line:
        line = add(line)
    elif '-' in line:
        line = sub(line)
    elif '*' in line:
        line = multiply(line)
    elif '/' in line:
        line = divide(line)
    elif '%' in line:
        line = mod(line)
    elif '^' in line:
        line = power(line)
    return line

arg_file = sys.argv[1]
file = open(arg_file, "r", encoding="utf-8")
lines = file.readlines()

for line in lines:
    lineNumber = lines.index(line) + 1

    for emoji, num in emojiNumbers.items():
        line = line.replace(emoji, str(num))

    print(ifStatementValues)

    # If statement
    if '❓' in line:
        if ifStatementValues and ifStatementValues[-1] == 0:
            continue

        call = line.split("❓(")[1]
        condition = call.split(")")[0]

        # Look for the if statement logic
        # Once found go to the function that corresponds to the logic (> < == != >= <=)
        # Then check each condition and return if it is true or false
        # If it is true then append the true to the array and execute the if statement code and skip all the elifs and else statements until the }}, then pop
        # If it is false then append the false to the array and check the next elif statent and do the same thing
        # If all the elifs are false then execute the else statement
        
        if '==' in condition:
            o1, o2 = condition.split('==')
            ifStatementValues.append(equal(o1, o2))

        elif '>' in condition:
            o1, o2 = condition.split('>')
            ifStatementValues.append(greaterThan(o1, o2))
            
        elif '<' in condition:
            o1, o2 = condition.split('<')
            ifStatementValues.append(lessThan(o1, o2))
        continue

    if '}}' in line:
        if ifStatementValues and ifStatementValues[-1] == 0:
            continue
        ifStatementValues.pop()
        continue

    if ifStatementValues and '}' in line and ifStatementValues[-1] == 1:
        ifStatementValues[-1] = 2
        continue

    if ifStatementValues and '}' in line and ifStatementValues[-1] == 0:
        ifStatementValues[-1] = -1
        continue
    
    if ifStatementValues and ifStatementValues[-1] == 2:
        continue

    if ifStatementValues and ifStatementValues[-1] == 0:
        continue

    if line.startswith("🖨("):
        call = line.split("🖨(")[1]
        val = call.split(")")[0]

        # Printing a string
        if val.startswith('"'):
            string = val.split('"')[1]
            print(string)

        # Printing a number
        elif val.isdigit():
            print(val)
        
        # Printing mathematical operations
        elif '+' in val or '-' in val or '*' in val or '/' in val or '%' in val or '^' in val:
            val = eval_line(val)
            print(val)
        else:
            print(eval_var(val, s))
        
    # Comment
    elif line.startswith("#"):
        continue

    # Elif statement     
    elif '⁉' in line:
        if ifStatementValues and ifStatementValues[-1] == 1:
            continue
        if ifStatementValues and ifStatementValues[-1] == 0:
            continue

        call = line.split("⁉(")[1]
        condition = call.split(")")[0]
        if '==' in condition:
            o1, o2 = condition.split('==')
            ifStatementValues[-1] = equal(o1, o2)

        elif '>' in condition:
            o1, o2 = condition.split('>')
            ifStatementValues[-1] = greaterThan(o1, o2)
            
        elif '<' in condition:
            o1, o2 = condition.split('<')
            ifStatementValues[-1] = lessThan(o1, o2)
    
    # Else statement
    elif '🔀' in line:
        if ifStatementValues and ifStatementValues[-1] == 1:
            continue
        if ifStatementValues and ifStatementValues[-1] == 0:
            continue

        ifStatementValues[-1] = 1

    # Assigning variables
    elif '=' in line:
        var, expr = line.split('=')

        if '+' in expr or '-' in expr or '*' in expr or '/' in expr or '%' in expr or '^' in expr:
            expr = str(eval_line(expr))

        expr = expr.strip()

        if expr.isdigit():
            s[var] = eval_expr(expr)
        else:
            expr = eval_var(expr, s)
            s[var] = eval_expr(expr)

    elif '}' in line:
        continue

    else:
        raise Exception(f"Line {lineNumber}: '{line} is not a valid statement")

