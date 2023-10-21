package services

import (
	"scam-master/internal/app"
	"scam-master/internal/services/transactions"
	"scam-master/internal/transport/kafka"

	"go.uber.org/zap"
)

func NewServices(l *zap.SugaredLogger, kafkaService kafka.KafkaService) *app.Services {
	return &app.Services{
		TransactionService: transactions.NewService(l, kafkaService),
	}
}
