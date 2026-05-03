from pwn import *

io = remote("localhost", 7001)
io.recvuntil(b">> ")
io.sendline(b'1')
io.recvline()
flagct = io.recvline().strip().decode()
print(flagct)

io.recvuntil(b">> ")
io.sendline(b'3')
io.recvuntil(b"Enter the Human Text: ")
toSend = b"a"*32
io.sendline(toSend.hex().encode())
ct = bytes.fromhex(io.recvline().strip().decode())
iv = xor(xor(b"aaaaaaaaaaaaaaaa", ct[:16]), ct[16:32])
print(iv.hex())

flagct1 = flagct[-32:]
flagct2 = flagct[:-32]

# decrypt just the last block to avoid condition check
io.recvuntil(b">> ")
io.sendline(b'2')
io.recvuntil(b"Enter the Taurusian Text: ")
toSend = flagct1 + iv.hex()
io.sendline(toSend.encode())
pt = eval(io.recvline().strip().decode())
print(pt)

# decrypt the rest of the blocks with recovered pt as iv
io.recvuntil(b">> ")
io.sendline(b'2')
io.recvuntil(b"Enter the Taurusian Text: ")
toSend = flagct2 + pt.hex()
io.sendline(toSend.encode())
pt = io.recvline().strip().decode()
print(pt)
