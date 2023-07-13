import unittest
from sqs_fetcher import encrypt, decrypt

class MyTestCase(unittest.TestCase):
    def test_encryption(self):
        key_str = '1234123412341234'
        key = key_str.encode("utf-8")
        ip = '199.172.111.135'
        result_en = encrypt(ip, key)
        self.assertEqual(b'&X*}\x05\x02\xcaX\xe1\xb8\xddk\xca\x89\xaeU', result_en)

    def test_decription(self):
        key_str = '1234123412341234'
        key = key_str.encode("utf-8")
        test_ip = b'&X*}\x05\x02\xcaX\xe1\xb8\xddk\xca\x89\xaeU'
        result_de = decrypt(test_ip, key)
        self.assertEqual('199.172.111.135', result_de)

if __name__ == "__main__":
    unittest.main()
