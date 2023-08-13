package api

import (
	"amibot-tg/server/utils"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/mongo"
)

type Server struct {
	router     *gin.Engine
	collection *mongo.Collection
	config     utils.Config
}

func NewServer(collection *mongo.Collection, config utils.Config) *Server {
	server := &Server{collection: collection, config: config}
	server.setupRoutes()
	return server
}

func (s *Server) setupRoutes() {
	r := gin.Default()
	defer func() {
		s.router = r
	}()

	r.GET("/", s.pingPongHandler)
	r.POST("/login", s.loginHandler)
	r.POST("/class_schedule", s.classScheduleHandler)
}

func (s *Server) Start() error {
	return s.router.Run(":3333")
}
