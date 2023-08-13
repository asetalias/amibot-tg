package api

import (
	"log"
	"net/http"
	"time"

	"github.com/ditsuke/go-amizone/amizone"
	"github.com/fernet/fernet-go"
	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

type request struct {
	Token int `json:"token"`
}

func (s *Server) pingPongHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"ping": "pong",
	})
}

func (s *Server) loginHandler(c *gin.Context) {
	var req request

	err := c.BindJSON(&req)
	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	filter := bson.M{"token": req.Token}
	err = s.collection.FindOne(c, filter).Err()
	if err != nil {
		if err == mongo.ErrNoDocuments {
			c.JSON(http.StatusNotFound, err.Error())
		}
	}

	c.JSON(http.StatusOK, "ok")
}

type userProfile struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

func (s *Server) classScheduleHandler(c *gin.Context) {
	var req request
	var user userProfile

	err := c.BindJSON(&req)
	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	filter := bson.M{"token": req.Token}
	err = s.collection.FindOne(c, filter).Decode(&user)
	if err != nil {
		if err == mongo.ErrNoDocuments {
			c.JSON(http.StatusNotFound, err.Error())
		}
		c.JSON(http.StatusInternalServerError, err.Error())
	}

	user.Password = string(fernet.VerifyAndDecrypt([]byte(user.Password), 0, s.config.FernetKey))

	creds := amizone.Credentials{
		Username: user.Username,
		Password: user.Password,
	}

	amizoneClient, err := amizone.NewClient(creds, nil)
	if err != nil {
		log.Println("Cannot create amizone client: ", err)
		c.JSON(http.StatusInternalServerError, err.Error())
	}

	year, month, day := time.Now().Date()

	schedule, err := amizoneClient.GetClassSchedule(year, month, day)
	if err != nil {
		log.Println("Cannot get class schedule: ", err)
		c.JSON(http.StatusInternalServerError, err.Error())
	}

	c.JSON(http.StatusOK, schedule)
}
