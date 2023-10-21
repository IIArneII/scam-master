package kafka

import (
	"scam-master/internal/config"

	"go.uber.org/zap"
)

type KafkaService interface {
	SendMessage() error
}

type kafkaService struct {
	l *zap.SugaredLogger
}

func NewKafkaService(l *zap.SugaredLogger, cfg config.KafkaConfig) (KafkaService, error) {
	svc := &kafkaService{
		l: l,
	}

	return svc, nil
}

func (svc *kafkaService) SendMessage() error {
	return nil
}
