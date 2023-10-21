package main

import (
	"log"
	"scam-master/internal/app"
	"scam-master/internal/config"
	"scam-master/internal/pkg/logger"
	"scam-master/internal/services"
	"scam-master/internal/transport/kafka"
	"scam-master/internal/transport/rest"

	"go.uber.org/zap"
)

func main() {
	cfg, err := config.NewConfig()
	if err != nil {
		log.Fatalln("init config: ", err)
	}

	l, err := logger.NewLogger(cfg.LogLevel)
	if err != nil {
		log.Fatalln("init logger: ", err)
	}
	l.Info("logger initialized")

	kafkaService, err := kafka.NewKafkaService(l, cfg.KafkaConfig)
	if err != nil {
		log.Fatalln("init kafka service: ", err)
	}
	defer kafkaService.Close()
	l.Info("connected kafka")

	services := services.NewServices(l, kafkaService)

	errc := make(chan error)
	go runHTTPServer(errc, l, cfg, services)

	err = <-errc
	if err != nil {
		l.Fatalln("http server: ", err)
	}
}

func runHTTPServer(errc chan error, l *zap.SugaredLogger, cfg config.Config, services *app.Services) {
	defer func() {
		if r := recover(); r != nil {
			l.Fatalln("panic: ", r)
		}
	}()

	l.Info("http server started")
	defer l.Info("http server finished")

	server, err := rest.NewServer(l, cfg, services)
	if err != nil {
		l.Fatalln("init http server: ", err)
	}

	errc <- server.Serve()
}
