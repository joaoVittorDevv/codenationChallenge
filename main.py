import requests as r
import hashlib
import json

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
NOT_CHANGE = [' ','.',',', 1,2,3,4,5,6,7,8,9,0,'1','2','3','4','5','6','7','8','9','0',]
token = 'd4eadd99f7aeac8b8e3abaf1494f3b5a0c1e7fb2'

def request():
    request = r.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=%s' % (token))
    return request.json()

def decrypt(key, message):
    m = ''
    str(message).islower()
    for c in message:
        if c in NOT_CHANGE:
            m += c
        else:
            c_index = ALPHABET.find(c).__index__()
            m += ALPHABET[c_index - key]
    return str(m)

def encrypt(decripted):
    return hashlib.sha1(decripted.encode('utf-8')).hexdigest()

def send(resp):
    json_dump = json.dumps(resp)
    with open("answer.json", "w") as outfile:
        outfile.write(json_dump)
    file = {'answer': open('answer.json', 'rb')}

    response = r.post('https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=%s' % token, files=file)
    return print(response.status_code)

request_json = request()
decripted = decrypt(request_json['numero_casas'],request_json['cifrado'])
encripted_sha1 = encrypt(decripted)

json_resp = {
    "numero_casas": request_json['numero_casas'],
	"token": token,
	"cifrado": request_json['cifrado'],
	"decifrado": decripted,
	"resumo_criptografico": encripted_sha1
}

send(json_resp)