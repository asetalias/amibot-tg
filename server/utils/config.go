package utils

import (
	"github.com/fernet/fernet-go"
	"github.com/spf13/viper"
)

type Config struct {
	MongoUri      string `mapstructure:"MONGO_URI"`
	ServerAddress string `mapstructure:"SERVER_ADDRESS"`
	GrpcAddress   string `mapstructure:"GRPC_ADDRESS"`
	Key           string `mapstructure:"KEY"`
	FernetKey     []*fernet.Key `mapstructure:"FERNET_KEY"`
}

func LoadConfig(path string) (config Config, err error) {
	viper.AddConfigPath(path)
	viper.SetConfigName("app")
	viper.AutomaticEnv()

	err = viper.ReadInConfig()
	if err != nil {
		return
	}

	err = viper.Unmarshal(&config)
	if err != nil {
		return
	}

	config.GrpcAddress = "amizone.fly.dev:443"
	config.FernetKey = fernet.MustDecodeKeys(config.Key)

	return
}
