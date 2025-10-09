import cryptography
import os
import logging
import base64

from typing import Optional, Dict, Any, List

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# RSA-OAEP Encrypting and decrypting
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64decode,b64encode
pubkey_dictionary: Dict[str, str] = {
	"jan": "AAAAB3NzaC1yc2EAAAADAQABAAABAQCiPUtYIclTqvZMJsXaWke9y6oOVjeRut7On00DzNaeZoQcIkSrh/uSu3UPHm9mV8+zG/qH0hdvs1sIVePLR2IqzYJG0LXyMSRQkQA9Fijbj9fCB3pRC2BHgITimao9i9aSQ1CmMaC5GPn3dYYHq4ux+y8Pz7CCNbiMQDVbBcI12TwbedZ1PQKon3xyGuHHxOujPJoFmAeg2OKd3oss9qJc6r/7azl2tR6yuDuviMPw4H61Keoqaay8QiK4zRHcAtTUuhCKpjGoNGVAgUr/WhO0AzzluWuJo/1UaEdLSkYduEaJ2MFVyuFjfoJZT2RwConSMs3pGvcih8KzKWaKa8Sv",
    "moi": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDJg5LXenZuapjn4LkuXwroYdesf7+5yqgfLXkLkcyL4yJ1PIoTfIQxxHxTOg0OaR5YD2ZqUv+R2FewgOUYPsOLU7O6vWz1BD/NnzpjYKLhuzPz5bUB8u/nBEq2U3ExEGBUlPsm3EIVrY7eJ2bXMNRtMqzwHx6A+7GnblcM0sDUglTOVC3zb8U+/IRi1tbwzlJd3l+NLeW2tvUqp9lB+maUH4JwNyyJen9Dkj34EVa8uybpSjqIVrNYl7dxBxA4RbMdADwFqp1JDaM8uazH/MI4RaGhKt4cxXSlif3ngkzL80i0CUxgaDbaZ8V7z25nDO53J8uS5yx8HttbDA8IXXMaLXRWB12zWLISpR24KjA+Soy49TVay5q0S5Iew6nbuapyXfQaieJhjsGblli6apYgA58WtFHUGx9vGcL0F0H8+yzdSfarHnQhNNYDLh/917X90il2fYnVTd9qysq+cD9vAbHz3nt+BeGxqCbIoXHlncG/HP/YUQWWoLMf+B1YlDs=",
    "cfd": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDF1QRyEFDV9GYiTTAsi0bx2SCIQrsUxCRzxcXQ6BTyQjNaImuUF1cbZ/JHPNeBAz6epLmnE/CjzEpgOfYyfnQrQXsts5gwnZL77h+iNX2fhYNhQ5w8R5KuAqRM38YncZpbFeJ/fzXmgxzOfbI9lP1KRxgtlO8bAT3/IVxdepIhtQl+AID+xwEnrgWwqPW5CYtgM7f6iMpsRIY6RyIfdaRvfR3yTOUIqQME7dlq0/ouGMEEKUDw2n5vcNQOd6ecxmVh7Eko6C6EHTXfnd+mKPP5JQHbH336vuprW2wndVCDsoP5TqeZOlKLy5jJ2/B1x2LpHH1YucL49oUX68F8H+D7",
    "hfb": "AAAAB3NzaC1yc2EAAAADAQABAAACAQDBUj2bKEyrOIuW9rxHuEvWN9uHX2PzdjzwsbP9deGOz5hQFzVjcvqRqwczfmQdvY6z3jNEzJdenGWQgpkrS6equwvVZ5D7Zl1kk13T8vaE51qGsUF7Hcc6mUxCv7KIsXMNgcouze6c4QD/MMH/0US+Qnsrp1yzCjz5S4fTLl8+Nfe62dkPCXaloLOnWv3wgMdTxm13oSHANuSTB36vXwdHA1FWJknXTiYVPnW6LG10UwHbzgR1SmBaKC7ROp745QkLkFeGXtGXuDjaKmf0Ldh1Lfrl7K4JxDEgJwGxYhSQnxdTyffPqNCQp+5OKGJBBW29lz4t2Ozv68oBcaGkgCU1xbqOc0CZ7vmlAQIbC4DcJGmlkYIHuFWAAhKrvEC/g4gvQrrYJri5rZiHT68Uy/L9+rXyq+dLGzCPqr9RhDCnU5XOer+IAywTkP0F4IhJ6PJCwPBGKYk3nXPgrqcreRt/ujq7mYz9WYk2Kd53EdME8IBAn2DQIo4nXY+YwL/3FfEAdXimrbo6cYuu/WwgXCCRbmnJrgaShsYNw1WSVJKx1sVY5gUQfs5dn4C5RxTXrH1SJXXH0gDt73DASmfuUlPUnb+zUao4CjdJ/hTQZ+lD7SwRWqNl9rvah9s3ivFyG3YghdUlaaSaHQr5FNqIe692Dlr3RbJCMkWSFD/BlcGe3Q==",
    "DPM": "AAAAB3NzaC1yc2EAAAADAQABAAACAQDFb5/oUQYem2KyGzRHWSL0Hk4BmMXphSA0BWVA6tPdq2siJLW2j8duRWUi8futB0j3b5dp+Y4vKdXXmQpWRnkn9OruB+PZxVn2/LN73ASPSpuXhHJgiAtlHGCKb6QQQOmPPpPcT1RbTEWLZIe2v7OfnF2qm9dGP5/46jphTUc2gh7rHKuhtNO44JnSscWi6wKdOz02qONm2IrGJ/sPzL7zZAfQxPMu5oMSooNWV6gvEdpfuGCmXlDjqDrEAts+SQcaa/dA8g0pTIJbfHMzgkcvkCoRfTPsl1CTTevjRZI40/sRIpSV9JPXJmxQLyMS3MdVjLM7g/KuRspkjXkSx7S0yDN4nX/k1t4PFLLJxcI3XNBV+gvs6gN3Rk8XjaOdO0zB3kl3olOhUyMpMR7X3nSr9ErIeV6kjiJG+rIDmrhqLdVq0FmI+6JuIZwy0pSYAA9YPVYmHvUX6aEWDLXGOdfle1dbm0PVeS2rEek9VQUWJ6UoD9eI9pj1ulcPno5ojZlUvtIF01wboDWWE2rV3KW1sGOkF/uThJ4BK5LYxL+jxMgDEWOnhZ1gLwkdkpzhqwwhBy9rI5M5tGNanxGyESFsvUSkZF7GoAtoaa3hQ2eaTZrNExqxZ/du3uo+gKXP0RyaMApaEdSHdZx4pAngFoGxCovYFQXjg9Y5cTciqrfYYw==",
    "pdiz": "AAAAB3NzaC1yc2EAAAADAQABAAACAQC5tzSLIVHbdPvf3jUxFROf5wL7dHPlCTfsXMazniwz1GpBEbUuA6amZkY3mF7kdahKl1mh9+DsPOEZ/+GAfwsu55u1fye0XQGC0vXhiUBS1E3BtWKhFHUuQNkfniOWLPAZn/CUGqROcY5z0vWBdMbnCijI+UBgBVXImAZyjTHftlCuInsWS15J0EHousGWVI+Af6mx8ttUe9cTqS7KEkik8CWmmN3q1cVXzeSnXo1hsUlX+TGUdoXs4qYEJZi4hwAZtvtowoWz6zsr9z5LqkF2GNWvRzW/TqUYozPfOS66EK/xzsOeAZVTUy7GYT1TYYaVkzH1Go80nGfKf5Io2F2ubxNq4mI8IH+h+25rhjQJc/G1z8qkMo4y3DC4x2wJYVhO0EyK3nGBZCOmCWBJNDxRdd1X4JPRsRXq9h33KRmvqXOv18ID/JSlC3p60yjfXg/CNjTnvptT34hD01dVHnI8bLBCffm3v5WFhVwOIBKnG9Lzvuuzx2hJVC77rh4Q2VQXzLB+D9G7o1L7poSPaFzC7aIJmh+zmt4KsuXrMsIyIi9fhr7NCWG6zUsZlWSLoxnv+Mp6cWSh5nI+ka/FVtp7K3oervG0ciP1YRScxdap7q9KwYcgjfijFbNm0GZB+jGVWq0V+sT66Fg8X/lJuRqwDu3D1Butc7hDy+yvwQlYXQ==",
    "YCR": "AAAAB3NzaC1yc2EAAAADAQABAAABAQCm/ovE3Y3aWnKcQcfCgqO2GpMCgFb8mOwrH3E2nR+potPwwCTNBjIaIejyt8f2cStWtOFaCufeKrO6TNnxJX8Mv994wD++T/EfzgiK1tCHvvz0cLDOMUQ5e99RtFFl+6R/T6hLNogCP12GFkwLpEjm4Cyu4v5hHgnGWdJpZf8q1rdRVIawiLjLoWW7GIkkD2HdDmkhkSe/0XlyEzx3b1DOB+YaNtk9c8F12wLa6xveu8ITsfn0lyeNZN0GZHZoFvEYSUtk0+Fs2nT7kQvYPJkMhuJaLib6qObEypms6OL8N0FqWOHNO1iQ62npAfTuBOe9dZaKprz/8TCUi5qs6RW9",
    "essb": "AAAAB3NzaC1yc2EAAAADAQABAAABgQCxsf09LfbHOcq+qPOBg8BBZeDov9cQkFEufCQps7BWOJKB79bRYNkuGK7oHRuhpl7rxohKDUyxqTiVCo0byw4dkcUPhXfrdrafg1VzPmFlNOlQr0xD1oAUnX2ttJWIXIqOimoswBgJXWlmyfuiXaRyc2S14Y7NE6QHb9eDpND2/LWUTNTcgEtBQyKEQa5WnaaC32cHMc94zvG9zVz+0ClQygQS0viZ7TYJjYcohKxGLtgNzncVxbGUf8tNjkOY8ccWUIgzWMhArC0he6XU59B1Uc/YLW9O0bHAeRdPnqvSy8W2vpIjrBQeRe5EL78prDHc4K2PpU69ZK1HoOolzpwmf/OZXjgF9mk5DQQJD+6b4RDGDNlaKK6Z/+ZbZzsztSEaj3Skmep9hYeyW24uYv+R1GXX1qD4DpWxdC+eA/PYNe8At4TQTo+mowIYh1up7/FXz3to0XH7knq77H6qdxOgA0vuD4C60LgYOAYxYUY1CuIGpkS40XCiBgj9Y1cQKW0=",
    "ppp": "AAAAC3NzaC1lZDI1NTE5AAAAIJA68flI4WBO3ssrvF24UOM08vWq93Lh5jzDQ9Ra2RJO perez@LAPTOP-VHSTDKRR",
    "VONX": "AAAAB3NzaC1yc2EAAAADAQABAAABgQCigLNV1Dc4+rkVnt/CfpTvK3ILqEE0RXVgb5H9yTFof0p5cp9HLlkV7JQqvK7gGqR3YSkC1kgZvKAiMG+21DrzINvVLsxuKvzDTP3RHHlz0uTLlczkOY/VeZ+JjhPBjlGX0n0Fl8wpGIzrnVKe6NZ9/J5ebgioADMVmjfik0W5yM7xgj0rpKrPggROiLC1glGYRMRNPmm0jI9CxUca4pAdaM2UFJRUuL9qyr96L9xjLWmDqLDLA7bPPtc2PKNxUhneYG87lh1FpCNKhX0lcH8dBZbaVEvS2QJN9dij3Y3jt14uASQkLM2gqMLNqmASaH17ExUYqWcwhWeIJQOx/injnS3UQxIo8zHVowZ6PPcRq2PBWPySiQZVt66PrWuVlb1D6tTcBt8VSNwGMdq5uT8ThJgYa7A8WLD9XMu+K/KVKY564l553LeMtAsDwd30nGiYKHR1Bud1tVUWK7bgDKsbxvnnnXlePbIUEOjGdB75dk4v5LR3XzfZNl53jM83lis=",
    "MAKI": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDCY5Y7vMq6jsBpcjDSCjKm/ft7OBIwpPb47Zlv4Y89NvVIcz/vppvbMH6Gp6ueeal8qnyHw0nP21MQvcIujw23/OaqbQ/wyCR0yTz/q+QfahgyJJKmIn44rtC/gJrhmgR7Q93Xjp68qja6FpHMiXGWM1/tl7DL1kFNc8Phg66MAFD26QzXz3RZxA+Eac6GT0ld1B852/4YPBz2YAsglws7WnEZvukLWGQj/F5gB+vYDipTEn9uk8vJEjOLbMxDOqTjDX0s+o7qBoMbO8Mr2v0BYYBwnZAdYGfUYzQgO0FLHRoLbcoM0He8FJp8z/giCOupSjsXS+h17YTWwl21naHekz0QwpOB0k/FOQHt/Sk1CAQDE0KErleoOskmps/eALXjjGrf3psLU8BJnel11rioIyHxrcS/ZkAqGrd+28kCrS/vz/8eBXSVBnzvk6LLxEBMWtwmInENpaEWZKGGOmLKTcaU1lTyqi3un6H07bZ/4h57dp9yUN9Mva9cwkmGwj8=",
    "jesu": "AAAAC3NzaC1lZDI1NTE5AAAAIG5zFL1i0u4ehyqK1pkb7cthEae9ZOcqmrNCwwxp+1LK",
    "chr": "AAAAC3NzaC1lZDI1NTE5AAAAIFFAjOVjVJjOOVjR8S8zJl3iBAwqlueEK3sFKVBjOOZz",
    "acu": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDRg7v4tXPEuZB+5EWkSFM1vNK0p1535yoaV6FFUh6TK1eWWp+bZ+6ZPadh8TrdVRJugtOs9UdpaKu195sbRTNkU6OsaifTykmooDs4pYrQb6pMZuXB8eOIaEJtWjaXpmAyxPeS45hlFM4uHl+kh0XJTuMjcqPkbyn2W5haE8D+cFAvncBe/d7EjXVDZPM/pxKRtv9BtaC1rCSya6jTbo32tFI3OKMNrU4n5PA2Fzp5GnWfRweGuoKifiyFXzRC9lkuNDw6I8Or3j1G6dj7ftBTngQwmHDvz73RBO0BHMnJZg50BFVry1hmV5CnO/x5nsIb1flbgcGLI+BZouVQpTGeGZqAbEOYlFctiRp0ggv53jM8G+FzJ6oIkKUmnAw9NCVWXwNd+X+7WWYSNW3aes0GfbOmhb639XPQemX2Erf7REqQZclHLHswI4KUfl8zDUtsQiYcYBSOzuUAtG0hRQofg8GevOZ6ZdRwyoaedfZvvWzmKatO+ITXNjWIiOsjI4c=",
    "bge": "AAAAB3NzaC1yc2EAAAADAQABAAABgQC0Ocfswr8gBMjdOhvmKdGAQy2qJdT7nDAfn5OF3/eFdSp8lKihn7AjoXTTueQRvBgQCd4nv1uL6ie9qi7bP2MYG2c4i3XhjP82WlgqSekqyqrWDYVAsPdagwRSl6udF18f5DjSy6GdiQCCDeCrR13io1k0+bIsMvKV9lgnRKYakSn4F9UJZ0D9xySXfekkVwlZ9LIemEoNKL+3JLIG/GASPAkxbRFBWV03DJ8fuxj6FOFv+g+cI+1DfMyFzsReKwfkmLnoOJy3vhn1YxsKNJ5M2kh2ZEs/zgc3wCfTia12RkXbip1rRmeeTV8nJpFYWmklbHRxPtiBIwYejetMo71aMNhIsdOr+QaF5XRaUOVhoLpc2SNCBZu2N2w7qn2pI1SAfwVMvaZC2ZNgY/fkeeQGytBt0igm4HGea+e/wZ/s48xUO4DpHB5m5sCaAPiDSc+GlLVlsIkh8KUg7/LMOg9s7el9syFobI2adYkWEK6sMxNE+hPwSZVwh28Bsr2mnLk=",
    "len": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDHBQFA2TIgrLuLNcHvt3AbUk5qsZKSz3Cq2+jGNrNLe/Z3VG9Ead76muR4F+JMU2sEHQx2oVYjz86s6fFvqB8+n2/N3YKaTg0e4KMVIIvvlydCGsE3itzqapDEOoGEdg0d8WJ/F4xbW42Baf4GUl1jiwq9ZZQuMsN6BveOQwbmv4LtCjhOQrh/wKAaeHjoi0RUudtsHlLMsU2uwacKuQu7RKPVQ0famAn4JEri3gbncrEr/P3yFw+hXYNvrY73BVa1dBrqxNZpqQ3cBCELxh2vEewWLpYfkl+rTOeUm583NjkcDW6GqN2AhcK858LqH6vjcsowdp5DD6poRfei6CVH",
    "ra8": "AAAAC3NzaC1lZDI1NTE5AAAAIAkPlmf9T/aFRtGOL4+xUjdy/aNjc88rCTey1fU9X2/x",
    "dopa": "AAAAB3NzaC1yc2EAAAADAQABAAACAQDROPpSMOr+xL6/ahHBrD5ZbFeoQo0G3BTbC0ylFjboR8mobsRHNTmuHf7j0hU4uJ5imL5ioZqgFBLKNoeTI7vHmoG7Sifim1D71iiORMeKHMPJw/4KHdbhkiFkaMNlxYAbGOE9lJPlisbLkn+XVsOPoJ0b2NabBWzkhgbac/EH4yXX+NTUPg/xjZf5j2uc3CgGLc1ACRt1cpR/FjAG1vO+tYNgUm00LOjxGqtrgdqJM+DQmOnBwK1QhWokvpoWk18rdK8rAAb1Vi00dB3fDU7L330h4U0sSFALpweRlXMkJbN0+1KFrheVc4lUpr7Aoar4KzHKBA4k3h9rLtYdM2RnU3nRBveudRKUrHSNvJrPFGZkk+27byFdMicQbOb6NHDum5DP8ZAzBuzPeSslH2os9nxRbNkDa4r0x1LSEHO0DYvMmfJPlZrpUUXkY5cfDwbyrMIY5sAliK2QZcY+UWLr9FYC6qq5iLF26ig3uxceVj5bpg5baJh+OswG2C6oj830PaVCEpu9CQORr8ywZ8WFziGb7vu0Phk6Y0uAqICoGSRHqw/jF7HbLbVDkMwTkYBTGdkccMFF+tYMHPWGpydVmwKsOHDrVa7p5GClHakGydW+7vm0F2U+czU+GooEHDay7690IPK1BnllCRVjMUaFRVTIDjL9IE5G5WJUNFotBQ==",
    "mnv": "AAAAB3NzaC1yc2EAAAADAQABAAACAQCtKJ3+lmBdpX0Sf7DZOSADrgM3kttPYe+krbAxUzAnA0EsDRi/QFU3cN2h0RAi15kKEmXhQ0q029YCq4yrOCM7j8vF8F9tgDHkB3LOycgWJNbxoVQ0lwfqq5lx/C8YmOgh9F4bA1cvX9kQfCGDZtvjiVfKm2uSX9foblbNTklk8DGpScWE/QB0xEDPGy4SlX6TczfEUKlAbcvjNK0Nx7hppCLyUZIaGCPtFoFD82t8pKFakKRMtV7PD43qqY+4EV3x4AQHuGd3CYZv8unzIUSkgjGbCcJu72GJvmvVSvAswygupgBlNy3OFMZNKPTpWaZUhrK1wr8Cmxg0za2D2ncxJtdN1SB5QzPz2k1Rc6zTKfjbO5qdsK7pFTxyW6stNKPTOo5pX0KldT2pDHjgh+INATB8VAQklZ/XUS4vB9rsLgmQmyZ8oemZYvBBDvd8IUSdPm4mManABvDvoxpfbqsmgK36QPo7P50VaFbGu1luiQ83k5jL0Qmz1tJrF3a2Ii6mFabuOrRdvXgaVWvN/YyZtx/0u+WdoWVLmG0r5yELbUKjwLLKABfSvoAun/oztoXj5RjEctv8F4KSoa6XpgF2tOfeZETlqA+g+Uo8ao8eBrONbzVJC+fpalit6Xav1w04e1WoOD15ohaZQ+l2YysEbjr8dgxHPThp17ret+xxkQ==",
    "mrt": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDImH7y0oPtihTWN37l3Y0Gj9x61/kukPZ+TN5CPcRiRQDine21Q+4vHbRaOOOx1caMGQ1llsZTHvclYJS6n818KolrCiidDazLa01SoSDkUSiRwTp4pwlxcSvH4znIH6DrNTVyEZVwYpSqABfc1IoJf8ykHLENOU12XMy9S2DDY2QfF5rNtx17gCxAYwOY+t4x9Nti3gtflVpK3uegAvfX1Xbp5SeorlWwGgSJDmXeAZhPm3r13CsoANR5IJ3V6Cxm+Hkbbf7BwNi3h5tw0DtBUEIo3d80jeCZSUyRcC43hzaqtoyYyo0hg5t0CjCBWENbh2UFmZpMtF9+9Hjet7Q3",
    "bor": "AAAAB3NzaC1yc2EAAAADAQABAAABgQC2NhkF537K56UFvMWeU+7gcWNJHJM3dOQPq8elAF1rhDNF/DbP6McUAeLor+0yENbrby2IUt6ZFoh23nps32e4W1A365wiNi8hmv0luAR49s9NIhQolDnmSWnJTyjhrsFJtEncxjT1RVcBcN3Pj0+fy7JiuvWE6b8Gsc7t8EXJJs+XO+MP5oxH//VePv4ed9bkh89rLTfPlWZRbxCn66uDCZer9pSLIpMB5nmGH5f8H6sFwa+dZdFtYpd6LFFN8WEvgvMWul/9hV9STyxQjp8KvzlvijqqTV124R07s1weMxLWdc6CK80KWIdyrwg3GbKqfiWyW/8gA/5LYKb4eV/bccRK/RCqLRp/S0/3H2GveQWp6JGAfTcFv7SdUzHRsvdOjJH4KmGC3V9EB/96A8x5k2cjj2mEefFzoE7o8jqZ5IfxTDi3LCmcx9PDyglFh0jKCZBo5h+0hWgir2cOSg2m4SYsqE2dT/BCIRIADVLTw8pL4ZTnojMTg+kLdGjm8Jc=",
    "leo": "AAAAC3NzaC1lZDI1NTE5AAAAIGTqEltHTljSySg8iY8+bDuCDDP3Tsa4KgYfIOTEsySG",
    "cas": "AAAAC3NzaC1lZDI1NTE5AAAAIPzmM7Bm47BQ4800ezR1gekNVItJmlSNR3/FQvClj8kl usuario@DESKTOP-RM793UE",
    "svf": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDaHf/C9KxwNyNNSFYrYnmeWoL0YfKgVCQCZaTG4gXoi0pqstL6dA0TyYwGxP72P5jnC2mpmK0eLKrCs3woKf0PLQHyBX/GEzuH2Brd6MwrJi7cx7KC4+RxfDMLVjNdftQKe8Zih3QFe7l6hc63zTqiwmyp4o7/ar9ZQ4qk/Zbuk+qveZlQv3X45Txp+ScLxxpOp9rcrvm9HiWGu9oZsyepUA+oBtw6BfaPbg9Hp1VHQ1lmJ3IcSqpboYqdzPlpMifPbgtGhK57SnZ58OdSGRg+ZpIdl94ewb0gw6Aqpx9misWcZJovQ0uRqWGBQv8kgQBLLYXB8yLphPdnbcsK/s2J usuario@LAPTOP-91MFJ80N",
    "slm": "AAAAB3NzaC1yc2EAAAADAQABAAACAQCsa86kw3+MKDZZEe7qHgTmbv3aV+edGoY6Gy25Eg3Oap/lA9QfZebZtS46zs5pms5AXmrqtjG7Fg9MzYzpqo5LymUeajiqnF5vbEf3xCR/anrbDShPkp1aNxl9KYMvcr/KetuhFHw6vMn/aJ2wdka31RB+Ri3dcpoOj11aLci7f2Lj/USSPtGpTtRvc/w2GVbqCnHuNmnGCzXrc70t71Ehir27SMhLyM99wIP+Vz+f6rrJqWjUEPSN6XoPRf9q6S/9B4KOetoAB7Hj0/q206g0BAoJipb+baHKRMe87C3seCkI0Q5eWknjv8FRf0VQg+mLsdOWGK67I3tnm+d/mQuiPjZHkaAx4ZAh7KDvTPoFQu+nfJR07GOUoOviKnQUyujb/t56jxxQTx2NgYKUgnBcuYfnPq7kvHSusTSo2bZs4/O0ZtA7jUWuKl7nYU/cg37XJ4nHGIGouT/ztZwFooJzco8g8jsfoSOsXX8+2ZhhezC7hvUGr+HVMLZKHXc1S/wz/KDlJJy10IzfCZpxHevgYVIlZDnioYbmPlbFdypgyeLtPECgRgWRVMfCXRpG3GXEOAL0n3F5RnO0eAeAFXxcgyT/qnNrHZeUDwyfh1JDLwVY1fEWwJUWE3v761AaIOThhqqFwebhl1nM76diqGLONIaQFB3l1EvOZ/9iMPPV+Q==",
    "lbc": "xJiiQJkjTk1oYXbvJOliTTY6TbxyJf99EW6y2HLkDgU",
    "svr": "AAAAB3NzaC1yc2EAAAADAQABAAABAQCn59WnCmhdrqpd9ejqKD2A29eCYxyP6KYPK1De1im+ZiYHa5ZlXJT86/MfBsmEXsUd1EjxtJcDCYXvwSHjrHJ6c38NpiR9o5wNutyTjQO00ko+QNjR8qAM+iWoulyDc0OcCkVf0A4JdCslQrpWczlBbXYVLTf7APcOaxuyV5qkuuS3gjOYGou4csUFJ7YTfHyUC/dTGYOed/jUasJyGsXCqCAEnUEjXjv9VxxnxILVRVhYwWz5yk+j2R6MGDo3xyYdpDpqrkAqUmfspVLibv39RnJOl49gzsU2VBpV0kTA9Fx6kVeyL1UkETGPR3gpP3Jo/u4yUIKhByM1JAaXK09b",
    "OJGC": "AAAAB3NzaC1yc2EAAAADAQABAAABAQCcq+0l6xCdvBeFUrAsRErYP8PSp8HtYr61S2NISl3upjpldPPPaZap9PfO4Mwc5yO0iOpThoxcaYx5twvQ11sSTWl7zQVcRCY3ch7t9dLPcT99u1TDByc3u3LMtwYWaC05NRTayoXP8RznyCYAzu9RlM+1CaVEqvSN7/sFEbCqq/ibGdvZzfhoUDlRF4jiY8aeQslgcjaa6Cl1F/H5jGpNrruHth6WQI6csF0R5iQfPECwEU2Cav5hsfm9nHuKVBtMK2zTujm1FMQ4CMLtahpeFl0TwMlsivPEB83nGOHjhGM3zetzUlZGOeaak2z6Lwu8NLnsCZqk5lwxzNH7Qx71",
    "ancr": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDWYXDNQ5gzhjf7fzwKzRfnN7/x7oiN8pcd6a8XzcEw3VhteAW7l+Ne27dYpNacyt+9h1Jfe7vAz+YLTPcZhqPxAilCZm9IliFEdAB3lYnjvHGTK4dJMhEcGa1cQJdop/jEqOhBcun2dWaJLKk9UDlke29l/UFjMdlUG1AEZUlzqWZ7aW/he/kf8DdTmc5/JDtCZZloH8fBUR+kWePBm/SZjnad0V4dFpFjsSvCH99v+9bhvek3o/eOINahvpQpnJHvN4QlMU4duWxiO/EPU1Wb9cuEMUqrU6sn65MtmS4jfJa4qCKxXVQ3OR3RMsTwTdKd0z/EKMpLLS/XvdHQC2//YSxChHm+YFGjs5JUlD1CUB1EKNsxkOJmC25XJ3LyVyGv8C2dHioQ8UVxvidt77cDqBuKGViwXrmKouYFo+065d2eG0JfuNF55tphlcA2jG9aXgyNsG+oEfbXBRkZvjpWhYRAstntB4QpOEw+oLYEoNt5OWPdvvqcAjKrP1OG1GU=",
    "moi": "AAAAB3NzaC1yc2EAAAADAQABAAACAQC9u9eGkYLOh5ClqZhDO5KeDGPvxTLU4wpCm8q2JdhS+hVlEtvLS5DuouKD2P9Zv5dGa5ekYmxdM/J9Tw/8sRx6drQGBmMZUnlTvvWmfUkeP3f31YbGvvrYk7lQ/6S7uddgEh+o8PCh9LBtXc9kmL5nlqC1XvIvoG2a+II0q2Pnop+1kTSQERLLR14rnQIH7/YSb6XBceRrI68yssUxTWlCTqaLxgX85Z/RMNM2abBIRFsbVc1OPZinn8Cv7VxhXtaqWOsUGdXhuC6ctmeKn8n3haW1BlaNpv0kCh/HO8Xy/ng9uZ2uDSXkomXoL9g5nfnK1DSmfnORA6lo1BpZh+bm+gKZykr9uJhA5IweNfAspNBOTUp073H/hubjk9u39Od3KzTx9fKQt3kb1lmN/hvr2QGMiRV9sGDxmKlB4nNseTBB72QGHwWnnuKj2oiDqlU3h/VgzwDjXoJMSPLmPOBn2h3AllOsGsupM0MTiFuy6YsgYLQ07HAsZgLuwf3C2h+LE9QhVffOVzpPcqTQwsDk7zWmTKWng/59DKn5boT15d4sbJxIV4L3BfDO1t5vZMvGjBWgKlv5PWF+1xTsAxrfuBU5lHNT+8jl9bhHjQH7aaVjF2gVsUkRXVXg0mSC2bHYb8JpdEMe+50S9lapAt3iWG91B6rHpt2YeMdWpxpXsw==",
    "mmlp": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDLDk1a0Z6wk/tib6jyaUROSAsSTg94r9Gp1SEKayA+K+wQU41rLvXbi/c9QcJBWyYkK86ojpKz6b6jrjCzuYxGo4HwlPN43EkUmGM7OTdUaBUAEn6RKEi0CjoywyrNZqmvFZ+oXMS2dw4CX6OK6PeBGHPYtm8O7L6wYpe11OjPXGJW/DjxorPi8c8MpiAMFBgpnMVeqaonm3fIP9nXKpFANt6mXjTPU+T2p+SNxqLz6Qf2O7R+2X8J06xNdxlklPR3ymC4tfv5fYGFblZvG6xOUoEfggARdWFtjWvXTTBcwwN2duP/mVSeK6iRj0EtXufa9t+ULvJu88dXmTxR/JQp",
    "roi": "AAAAB3NzaC1yc2EAAAADAQABAAABAQCeF811gbUKrX5XwEwlRq2bWrzEwqhzjtzGCyRoI5FYVQGkLOw+8PXk0g8glzVW3NWNiPwGwpABiLy8e8WLkPWeiUmXzC7n+u3pv2LgP0rv2akXfwmbN1Lp8kZMbFbxHvr2qQMoVa5VetzZOaKv163pdyZ6UTMLUKwI39e34SDzWDGR79OzThmRbICFBAp/xolRblWSsYb+Z6gwRVSM5bGUvef5Ejn3CpBI7WvL58FSO40BAWsGHcn1qcpc7TV2dKs/qBU8xS9s1yE54f6xpeU+mIn1QGhGgQM3q3shGgt5QmOkXoHKCqGdz73XoD7htfWWEXGbs7+CKFGKjoNCqC2n"
}

# ---------------------------
# ! Variables utiles
# ---------------------------
K_LEN = 16          # 128 bits para k
AES_TAG_LEN = 16  # tag GCM de 16 bytes

# ---------------------------
# ! Carga de claves locales
# ---------------------------
# Intento cargar la clave privada (archivo id_rsaSIsamu) y la pública.
# Si no existen, private_key / public_key quedarán a None y las funciones que dependan fallarán.
try:
    with open("id_rsaSIsamu", "rb") as kf:
        private_key = serialization.load_pem_private_key(
            kf.read(),
            password=None,
            backend=default_backend()
        )
except FileNotFoundError:
    private_key = None
    logging.warning("Private key file not found.")
    
try:
    with open("id_rsaSIsamu.pub", "rb") as kf:
        public_key = serialization.load_ssh_public_key(
            kf.read(),
            backend=default_backend()
        )
except FileNotFoundError:
    public_key = None
    logging.warning("Public key file not found.")

# ---------------------------
# ! Formateo / padding de user-id
# ---------------------------
# Esta función toma un identificador en bytes y lo deja con 5 bytes exactos
# rellenando con ceros por la DERECHA.
def pad_userid(uId: bytes) -> bytes:
    """Rellenar a la derecha con '\x00' hasta 5. Trunca si es mayor."""
    if not isinstance(uId, (bytes, bytearray)):
        raise TypeError("pad_userid espera bytes")
    if len(uId) >= 5:
        return uId[:5]
    return uId + b"\x00" * (5 - len(uId))

def unpad_userid(b: bytes) -> bytes:
    """Quita los ceros finales añadidos por pad_userid."""
    return b.rstrip(b"\x00")

# ---------------------------
# ! Buscar clave pública por id
# ---------------------------
# Recupera la parte base64 desde el diccionario y se carga como clave pública OpenSSH.
def find_public_key_by_id(uid: str):
    if uid is None:
        return None
    p = pubkey_dictionary.get(uid)
    if not p:
        return None
    try:
        return serialization.load_ssh_public_key(('ssh-rsa ' + p).encode('ascii'), backend=default_backend())
    except Exception as e:
        logging.exception("Error cargando clave pública %s: %s", uid, e)
        return None
        
# ---------------------------
# ! AES-GCM (uso de la clase AESGCM)
# ---------------------------
# Encrypt el plaintext con la key usando AESGCM cipher
def encrypt_aesgcm(key, plaintext):
    aesgcm = AESGCM(key)
    nonce = key[:16] # para que sea iv = k -> nonce = key[:16]
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return ciphertext
    
# Decrypt el ciphertext con la key usando AESGCM cipher
def decrypt_aesgcm(key, ciphertext):
    aesgcm = AESGCM(key)
    nonce = key[:16]
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext

# ------------------------------------------------------------
# ! RSA-OAEP (Epub / Dpriv) con SHA-256
# ------------------------------------------------------------
# Encrypt el plaintext con la pub_key usando RSA cipher
def rsa_encrypt(pub_key, plaintext: bytes) -> bytes:
    return pub_key.encrypt(
        plaintext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )
    
# Decrypt el ciphertext con la private_key usando RSA cipher
def rsa_decrypt(ciphertext: bytes) -> bytes:
    if private_key is None:
        raise RuntimeError("Clave privada no cargada")
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )

# ---------------------------
# ! Cifrado híbrido (RSA para la clave, AESGCM para los datos)
# ---------------------------
# Encrypt el plaintext usando cifrado híbrido, primero AESGCM para los datos y luego RSA para la clave AESGCM.
def encrypt_hybrid(pub_key, plaintext: bytes) -> bytes:
    """
    Genera k (16 bytes), cifra plaintext con AES-GCM (iv=k),
    cifra k con RSA-OAEP y devuelve ek || ct || tag.
    """
    k = AESGCM.generate_key(bit_length=128)
    c2 = encrypt_aesgcm(k, plaintext)
    c1 = rsa_encrypt(pub_key, k)
    return c1 + c2

# Decrypt el plaintext usando cifrado híbrido, primero RSA para la clave AESGCM y luego AESGCM para los datos.
def decrypt_hybrid(ciphertext: bytes) -> bytes:
    """
    Separa el bloque RSA (keylen) y el resto (ct||tag), recupera k y descifra.
    Devuelve plaintext bytes o lanza excepciones si falla.
    """
    if private_key is None:
        raise RuntimeError("Clave privada no cargada")
    key_block_len = private_key.key_size // 8
    logging.debug("decrypt_hybrid: key_length=%d total_cipher_len=%d", key_block_len, len(ciphertext))
    if len(ciphertext) <= key_block_len + AES_TAG_LEN:
        raise ValueError("Ciphertext demasiado corto")
    ek = ciphertext[:key_block_len]
    ct_tag = ciphertext[key_block_len:]
    logging.debug("len ek=%d len ct_tag=%d", len(ek), len(ct_tag))
    k = rsa_decrypt(ek)
    pt = decrypt_aesgcm(k, ct_tag)
    return pt

# ------------------------------------------------------------
# ! Nested hybrid encryption (Algorithm 1)
# Entrada: path = [h1, h2, ..., hn] (hn = destinatario)
# sender_id: identificador remitente (str), "none" para anonimato
# message: bytes o str
# ------------------------------------------------------------
def encrypt_nested_hybrid(path: List[str], message: bytes, sender_id: str = "none") -> bytes:
    if not path:
        raise ValueError("path debe contener al menos el destinatario final")
    
    if isinstance(message, str):
        message = message.encode('utf-8')
    sender_b = sender_id.encode('ascii') if isinstance(sender_id, str) else sender_id
    # capa terminal: pad('end') || pad(sender) || message
    terminal_payload = pad_userid(b"end") + pad_userid(sender_b) + message
    # cifrar para el destinatario final (path[-1])
    recipient = path[-1]
    recipient_pub = find_public_key_by_id(recipient)
    if recipient_pub is None:
        raise KeyError(f"No encontré clave pública de '{recipient}'")
    c = encrypt_hybrid(recipient_pub, terminal_payload)
    # envolver desde n-1 hasta 0 (inclusive)
    # en cada paso: payload = pad(next_hop) || inner; luego Encrypt(pk_i, payload)
    for idx in range(len(path) - 2, -1, -1):
        pk_i = find_public_key_by_id(path[idx])
        if pk_i is None:
            raise KeyError(f"No encontré clave pública de '{path[idx]}'")
        next_hop = path[idx + 1]
        next_b = pad_userid(next_hop.encode('ascii') if isinstance(next_hop, str) else next_hop)
        inner = next_b + c
        c = encrypt_hybrid(pk_i, inner)
    return c

# ------------------------------------------------------------
# ! Debug / Descifrado de mensaje recibido y mostrar
# ------------------------------------------------------------
def receive_message_debug(ciphertext: bytes):
    try:
        decrypted = decrypt_hybrid(ciphertext)
    except Exception as e:
        logging.exception("Fallo al descifrar: %s", e)
        return
    if len(decrypted) < 5:
        logging.error("Descifrado demasiado corto (%d bytes)", len(decrypted))
        return
    next_hop = unpad_userid(decrypted[:5]).decode('ascii', errors='ignore')
    inner = decrypted[5:]
    if next_hop.lower() == "end":
        if len(inner) < 5:
            logging.error("Inner demasiado corto para contener sender")
            return
        sender = unpad_userid(inner[:5]).decode('ascii', errors='ignore')
        message_bytes = inner[5:]
        try:
            message_text = message_bytes.decode('utf-8')
        except Exception:
            message_text = message_bytes.decode('utf-8', errors='replace')
        print(f"[DEBUG] Mensaje final — De: {sender} — Contenido: {message_text}")
    else:
        print(f"[DEBUG] Reenvío — next_hop: {next_hop} — inner_bytes_len: {len(inner)}")

