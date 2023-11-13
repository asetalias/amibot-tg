package utils

import "github.com/fernet/fernet-go"

func Decrypt(a string, key []*fernet.Key) []byte {
	return fernet.VerifyAndDecrypt([]byte(a), 0, key)
}
