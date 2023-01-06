def index():
    with open('templates/index.html', 'r') as template:
        return template.read()

def first():
    with open('templates/first.html', 'r') as template:
        return template.read()

def second():
    with open('templates/second.html', 'r') as template:
        return template.read()
