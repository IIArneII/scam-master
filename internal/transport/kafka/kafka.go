package kafka

import (
	"encoding/json"
	"scam-master/internal/config"
	"scam-master/internal/transport/kafka/entity"

	"github.com/IBM/sarama"
	"go.uber.org/zap"
)

type KafkaService interface {
	SendMessage(msg interface{}, topic entity.Topic) error
	Close()
}

type kafkaService struct {
	l        *zap.SugaredLogger
	producer sarama.SyncProducer
}

func NewKafkaService(l *zap.SugaredLogger, cfg config.KafkaConfig) (KafkaService, error) {
	config := sarama.NewConfig()
	config.Producer.RequiredAcks = sarama.WaitForLocal
	config.Producer.Return.Successes = true
	config.Producer.Return.Errors = true

	producer, err := sarama.NewSyncProducer(cfg.GetBrokers(), config)
	if err != nil {
		return nil, err
	}

	return &kafkaService{
		l:        l,
		producer: producer,
	}, nil
}

func (svc *kafkaService) SendMessage(msg interface{}, topic entity.Topic) error {
	jsonMsg, err := json.Marshal(msg)
	if err != nil {
		return err
	}

	producerMessage := &sarama.ProducerMessage{
		Topic: string(topic),
		Value: sarama.ByteEncoder(jsonMsg),
	}

	_, _, err = svc.producer.SendMessage(producerMessage)
	if err != nil {
		return err
	}

	return nil
}

func (svc *kafkaService) Close() {
	if err := svc.producer.Close(); err != nil {
		svc.l.Error("error closing kafka producer: ", err)
	}
}
