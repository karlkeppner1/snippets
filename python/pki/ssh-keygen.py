import random, string
from cryptography.hazmat.primitives import serialization as serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as default_backend


def gen_password(length = 0):
  '''
  Create alphanumeric password of length <length>.

  Args:
    length (int):
      Length of password to be generated.
      
    Examples:
      - (24)

  Returns:
    :obj:`str`:
      Random alphanumeric password of length <length>.

  Examples:
    - password = gen_password(24)
  '''
  possible_characters = string.ascii_letters + string.digits
  return ''.join(random.choice(possible_characters) for i in range(length))


def gen_keypair():
  '''
  Generate a PEM encoded, OpenSSH formatted public key and passphrase encrypted private key.

  Args:
    None

  Returns:
    :obj:`bytes`:
      PEM encoded, OpenSSH formatted public key.
    :obj:`bytes`:
      PEM encoded, OpenSSH formatted private key.
    :obj:`str`:
      Private key decryption passphrase.

  Examples:
    - pub, prv, passwd = gen_keypair()
  '''
  private_key_password = gen_password(24)
  key = rsa.generate_private_key(
    public_exponent=65537,
    backend=default_backend(),
    key_size=4096
  )
  private_key = key.private_bytes(
    encoding=serialization.Encoding.PEM,  # Change if another 
    format=serialization.PrivateFormat.TraditionalOpenSSL,  # 
    encryption_algorithm=serialization.BestAvailableEncryption(private_key_password.encode('utf-8'))
  )
  public_key = key.public_key().public_bytes(
    encoding=serialization.Encoding.OpenSSH,  # 
    format=serialization.PublicFormat.OpenSSH  # 
  )
  return public_key, private_key, private_key_password