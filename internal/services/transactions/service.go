package transactions

import (
	"scam-master/internal/app"
	"scam-master/internal/transport/kafka"

	"go.uber.org/zap"
)

type transactionsService struct {
	l            *zap.SugaredLogger
	kafkaService kafka.KafkaService
}

func NewService(l *zap.SugaredLogger, kafkaService kafka.KafkaService) app.TransactionService {
	return &transactionsService{
		l:            l,
		kafkaService: kafkaService,
	}
}
