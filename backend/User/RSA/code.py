import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5

# def get_key(key_file):
#     print("ee")
#     with open(key_file) as f:
#         print("ff")
#         data = f.read()  # 获取，密钥信息
#         print("gg")
#         key = RSA.importKey(data)
#         print("kk")
#     return key

# rsa加密(公钥加密)
def rsa_encrypt(message):
    public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmiY4E+dWyz5ybxjthFkz8GQrFZuqiXtQOGl80IIgw9hon/DAXUiE2YvGclZ7x3EMW6xzqshVAv0wI8NGwm7MyAPzlzJ8r7rSDmP2pFXrzO26urPeKoqxbnsX8i0qDzJrUNaI8j7ZN8tzPwIUjWHm3zS7uT/DIfZUCceGd24PIRBaTGShCap22aFCRwd68IplqQXoNcUJj76FkHHbU5Ui2Tfkg2kHPFLGv0+eUe0w7cf05jGmbyCYhLnwRDmhKhpV+xC4PeXdqbl/XhKxLuMzMdkd6LJbICT7x4lPiDsV0MaiIqslz/hTuf2qqyE2kwhZJEUBKOsZ5jLseXn06UhxTQIDAQAB"
    key = '-----BEGIN PUBLIC KEY----- \n' + public_key + '\n-----END PUBLIC KEY-----'
    rsa_key = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)  # 创建用于执行pkcs1_v1_5加密或解密的密码
    cipher_text = base64.b64encode(cipher.encrypt(message.encode("utf-8")))
    return cipher_text.decode("utf-8")