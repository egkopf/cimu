import argparse
from cimuapp import app
from sys import exit, stderr

def main():

    parser = argparse.ArgumentParser(description='The Cimu application')

    parser.add_argument(
        "port",
        type=int,
        help="the port at which the server is listening")

    parser.allow_abbrev = False

    argv = parser.parse_args()

    try:
        app.run(host='0.0.0.0', port=argv.port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

# if __name__ == '__main__':
#     main()
