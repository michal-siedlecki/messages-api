import os
import secrets as s

import config

clients = config.clients_num
base_dir = config.basedir
token_file_path = os.path.join(base_dir, "tokens.txt")

tokens = [s.token_urlsafe(25) for c in range(clients)]

with open(token_file_path, 'w') as f:
    f.write("\n".join(tokens))




