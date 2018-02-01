#! coding: utf-8
import base64
import rsa
from Crypto.PublicKey import RSA
from  Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

sig = "UrMJ7p1Qm3F4SqECkiQE4ojXKCo0y8pCX6hBOyfna0sGTThe58ATtCNZt0Dg8sFxf89JuuQ3ELFRlzsLmYtMdGwoD8tGp7i0to+OtawSGXa1A+26I6WeA8Y38gpYjWsuOFElyWrjqKJZSKs6anxXXU5NGVlGsrW1LWAuuJRw4n/L8tfDzSmIDATUEDTXLtXkqoKe8MIFlj8gMZENm4/vXrpZGzouGJEct8V+bQNwZf2Pc8MU8rdl/+C6WZ0HKDs+luWHBnV30ZbPao/xeyx5PymUeGznyVmsNGjEZDIFGkhbFUMHdBmnA/DDYbCn+CknDW/aMVv1lUi4tMWIUFvsjA=="

data = "LoginName=lg_zdcRandom=77844c88-0b58-4952-a878-5dd552e89db1LoginTime=20160107184524AppCodes=GZW_001&GZW_002&GZW_003&GZW_006"

pubKey = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAj6/4MaN5tXDvDSMoC3EO
V6pJ2Mkgn7mSmku9c4NDf/spmYUJXzWHzNMdiokBFsDNFHQddKIs78TEcoufr9WT
DFNt7bYK7EbuHn3oHyrk+gcQb5SIgAst4rXMwqi0eQullvLRA93dDl3a6AEDo8ms
G4D0WWJCDabxw2uIrjuMi/eFE8c4jw5K3Y4Zn49KVZ4wh2jr6XV8ajz6qWrE+8OK
OV/J2/U43GkbIqdmIqn/2mqhSosbVTR/sPQVRg/jwURWjmatEauBmHeuWKL3mY/4
SVnEYpOwV2CgtUFtx3oCVTFUX9f2HtVM/LhIOY6GbcCzAmd3IivjIZCVS+Erd5FS
NwIDAQAB
-----END PUBLIC KEY-----
"""

cert = "MIICtjCCAh+gAwIBAgIDD0LAMA0GCSqGSIb3DQEBBQUAMDMxCzAJBgNVBAYTAkNOMRIwEAYDVQQIDAlTaGFuZyBIYWkxEDAOBgNVBAMMB0NsYXNzIDEwHhcNMTUwNDE2MDkyOTIwWhcNMjAwNDE2MDkyOTIwWjAjMQswCQYDVQQGEwJDTjEUMBIGA1UEAwwLd3d3LnNzby5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCPr/gxo3m1cO8NIygLcQ5XqknYySCfuZKaS71zg0N/+ymZhQlfNYfM0x2KiQEWwM0UdB10oizvxMRyi5+v1ZMMU23ttgrsRu4efegfKuT6BxBvlIiACy3itczCqLR5C6WW8tED3d0OXdroAQOjyawbgPRZYkINpvHDa4iuO4yL94UTxziPDkrdjhmfj0pVnjCHaOvpdXxqPPqpasT7w4o5X8nb9TjcaRsip2Yiqf/aaqFKixtVNH+w9BVGD+PBRFaOZq0Rq4GYd65YoveZj/hJWcRik7BXYKC1QW3HegJVMVRf1/Ye1Uz8uEg5joZtwLMCZ3ciK+MhkJVL4St3kVI3AgMBAAGjZDBiMBMGA1UdJQQMMAoGCCsGAQUFBwMIMB8GA1UdIwQYMBaAFHNGarqxA5FkkmSwATXFQQ37wWklMAsGA1UdDwQEAwIGwDAdBgNVHQ4EFgQUvTjY0vUzMUeKhrhub9t5VUU9PKswDQYJKoZIhvcNAQEFBQADgYEAje3e0G/8i2B/ngyEiDee8jUj2AhyJ8AVLWPbhw8i2wp5o7s3DPTKgK2xpxbHBQSHB0xtAvxquc1TeCIBaqc9qWZ0/O4DlkUI1PIgRs7lPx6s2sLqd+Nh3Q/KzYcd2OTVt1k/0kMUFzOxQRrjIugKabuZlgyQL0vlf1rEYNATGpw="
#def verify(data, sig):
#    with open("c:\Users\lrh\Desktop\pubkey.pem", "r") as f:
#        pubKey = f.read()
#    key = RSA.importKey(pubKey)
#    h = SHA.new(data)
#    verifier = PKCS1_v1_5.new(key)
#    if verifier.verify(h, base64.b64decode(sig)):
#        return True
#    else:
#        return False

#def rsa_verify(data, sig):

def form_cert(cert_text):
    """
        处理证书内容，必须每行64个字符
    """
    CERT_LEN = len(cert_text)
    MAX_LEN = 64
    COUNT = CERT_LEN / MAX_LEN
    text_list = []
    text_list.append("-----BEGIN CERTIFICATE-----")
    for n in range(COUNT + 1):
        start = n * MAX_LEN
        end = (n + 1) * MAX_LEN
        text_list.append(cert_text[start:end])
    text_list.append("-----END CERTIFICATE-----")
    text = "\n".join(text_list)
    return text

if __name__ == "__main__":
    #print verify(data, sig)
    #with open("c:\Users\lrh\Desktop\pubkey.pem", "rb") as f:
        #pubKey = f.read()
    print pubKey

    key = rsa.PublicKey.load_pkcs1_openssl_pem(pubKey)

    print rsa.verify(data, base64.b64decode(sig), key)

