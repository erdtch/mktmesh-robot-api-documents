import crython

# ref https://github.com/ahawker/crython
@crython.job(second='*/5')
def foo():
    print("Hello World")


if __name__ == '__main__':
    crython.start()
    input("Press Enter to exit...\n")