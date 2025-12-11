import hashlib

string_to_hash = "12211BSI276"
sha256_hash = hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest()
month = int(sha256_hash, 16) % 12
print(f"O número do mês (0-11) é: {month}")