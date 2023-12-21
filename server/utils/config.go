package utils

import (
	"fmt"
	"log"
	"os"

	"github.com/fernet/fernet-go"
)

type Config struct {
	MongoUri  string        `mapstructure:"MONGO_URI"`
	Key       string        `mapstructure:"KEY"`
	FernetKey []*fernet.Key `mapstructure:"FERNET_KEY"`
}

func LoadConfig(path string) (config Config, err error) {
	config.MongoUri, err = getEnvVar("MONGO_URI")
	if err != nil {
		return 
	}

	config.Key, err = getEnvVar("KEY")
	if err != nil {
		return
	}

	config.FernetKey = fernet.MustDecodeKeys(config.Key)

	return
}

func getEnvVar(key string) (string, error) {
	value := os.Getenv(key)
	if value == "" {
		return "", fmt.Errorf("%s environment variable not set", key)
	}
	log.Println("getEnvVar:", key, value)
	return value, nil
}