import re


if __name__ == '__main__':
    pattern = r"^([\w]+)\@([\w]+)\.\w{2,3}"
    addr = "mrbob@example.it"
    if re.match(pattern, addr):
        print(True)
    else:
        print(False)
