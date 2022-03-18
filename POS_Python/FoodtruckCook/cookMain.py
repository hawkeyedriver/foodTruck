from posDB import PosDB
from cook import CookApp

def main():
    connection = PosDB()
    connection.connecting()
    cooking = CookApp(connection)

if __name__ == "__main__":
    main() 
