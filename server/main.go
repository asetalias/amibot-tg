package main

import (
	"amibot-tg/server/api"
	"amibot-tg/server/utils"
	"log"
)

func main() {
	config, err := utils.LoadConfig(".")
	if err != nil {
		log.Fatal("Cannot load config:", err)
	}

	log.Println("config:", config)

	collection, err := utils.ConnectDB(config.MongoUri)
	if err != nil {
		log.Fatal("Cannot connect to MongoDB:", err)
	}

	server := api.NewServer(collection, config)

	err = server.Start()
	if err != nil {
		log.Fatal("Cannot start server:", err)
	}
}
