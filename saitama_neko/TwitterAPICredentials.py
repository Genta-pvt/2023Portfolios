import csv


class SaitamaCatInf:
    cre_dict = None
    HEADER = ['consumer_key', 'consumer_secret', 'bearer_token', 'access_token', 'access_secret']
    FILE_NAME = 'Credentials.csv'

    def __init__(self):
        self.exist_check()

    def exist_check(self):
        try:
            with open(self.FILE_NAME, encoding='utf-8') as file:
                if str(next(csv.reader(file))) != str(self.HEADER):
                    raise InvalidHeaderError(InvalidHeaderError.MESSAGE)
                for key in next(csv.reader(file)):
                    if not key:
                        raise InvalidKeyError(InvalidKeyError.MESSAGE)
        except (FileNotFoundError, InvalidHeaderError, InvalidKeyError) as e:
            print(e)
            self.write_csv()
        finally:
            self.cre_dict = self.read_csv()

    def read_csv(self):
        with open(self.FILE_NAME, encoding='utf-8') as file:
            next(csv.reader(file))
            credential_dic = next(csv.DictReader(file, self.HEADER))
            return credential_dic

    def write_csv(self):
        with open(self.FILE_NAME, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.HEADER)
            writer.writerow(self.input_keys())

    def input_keys(self):
        keys = []
        print('Please enter your key information')
        for col in self.HEADER:
            key = input(col + '? : ')
            keys.append(key)
        return keys


class InvalidHeaderError(Exception):
    MESSAGE = 'The CSV file has an invalid heading.'


class InvalidKeyError(Exception):
    MESSAGE = 'Key is an invalid value'


# 単体で実行したときの処理
if __name__ == '__main__':
    test = SaitamaCatInf()
