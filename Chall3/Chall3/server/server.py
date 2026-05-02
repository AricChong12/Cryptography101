#!/usr/local/bin/python

from Crypto.Cipher import AES
import secrets
from quotes import QOTD

class bAESics:
    def __init__(self, key: bytes, iv: bytes):
        self.blockCipher = AES.new(key=key, mode=AES.MODE_ECB)
        self.iv = iv
        
    def HumanToTaurusian(self, humantext: bytes):
        humantextblocks = self.blockify(self.padding(humantext))
        taurusianblocks = []
        for i in range(len(humantextblocks)):
            temp = self.blockCipher.encrypt(humantextblocks[i])
            if i < len(humantextblocks)-1:
                temp = self.sorcery(temp, humantextblocks[i+1])
            else:
                temp = self.sorcery(temp, self.iv) 
            
            taurusianblocks.append(temp.hex())
            
        return "".join(taurusianblocks)
            

    def TaurusianToHuman(self, taurusiantext: bytes):
        taurusianblocks = self.blockify(taurusiantext)
        humantextblocks = []
        for i in range(len(taurusianblocks) - 1, -1, -1):
            if i == len(taurusianblocks) - 1:
                temp = self.sorcery(taurusianblocks[i], self.iv)
            else: 
                temp = self.sorcery(taurusianblocks[i], humantextblocks[-1])

            temp = self.blockCipher.decrypt(temp)
            humantextblocks.append(temp)
            
        return b"".join(humantextblocks[::-1])

    def blockify(self, m: bytes):
        return [m[i:i+16] for i in range(0,len(m),16)]
    
    def padding(self, m: bytes):
        if len(m)%16 != 0:
            m += b"\x01"*(16 - len(m)%16)
        return m
    
    def sorcery(self, m1, m2):
        return bytes([a^b for a,b in zip(m1,m2)])
            

def main():
    KEY = secrets.token_bytes(16)
    IV = secrets.token_bytes(16)
    translator = bAESics(KEY, IV)
    quote = translator.HumanToTaurusian(QOTD)
    
    print("Newly Developed Translator for Human Language to Taurusian Language!!! (for Taurusians only btw)")
    print("[1] Get the Taurusian Quote of the Day")
    print("[2] Translate from Taurusian => Human")
    print("[3] Translate from Human => Taurusian")
    print("[4] Quit\n")
    
    while True:
        sel = input(">> ")
        match sel:
            case "1":
                print("We love human quotes but we couldn't come up with one ourselves, but we can just translate human quotes to Taurusian instead!")
                print(quote)
                
            case "2":
                inputText = bytes.fromhex(input("Enter the Taurusian Text: "))
                taurusianText = inputText[:-16]
                iv = inputText[-16:]
                if taurusianText.hex() == quote:
                    print("Wait wait wait, this quote is so famous you wouldn't need the translator do you?")
                    quit()
                else:
                    translator = bAESics(KEY, iv)
                    humanText = translator.TaurusianToHuman(taurusianText)
                    print(humanText)

            case "3":
                inputText = bytes.fromhex(input("Enter the Human Text: "))
                translator = bAESics(KEY, IV)
                print(translator.HumanToTaurusian(inputText))
                               
            case "4":
                exit()
                
            case _:
                exit()


if __name__ == "__main__":  
    main()
    
else:
    raise Exception("Problem Occured")