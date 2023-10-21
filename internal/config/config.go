package config

import (
	"errors"
	"os"
	"strings"

	"github.com/caarlos0/env/v9"
	"github.com/joho/godotenv"
)

type (
	Config struct {
		Port           int    `env:"HTTP_PORT" envDefault:"8080"`
		BasePath       string `env:"HTTP_BASE_PATH" envDefault:""`
		AllowedOrigins string `env:"HTTP_ALLOWED_ORIGINS" envDefault:"*"`
		Host           string `env:"HTTP_HOST" envDefault:"0.0.0.0"`
		LogLevel       string `env:"LOG_LEVEL" envDefault:"INFO"`
		KafkaConfig    KafkaConfig
	}

	KafkaConfig struct {
		Brokers string `env:"KAFKA_BROKERS" envDefault:"localhost:9092"`
	}
)

func NewConfig(configFiles ...string) (Config, error) {
	var c Config
	err := godotenv.Load(configFiles...)
	if err != nil {
		if !errors.Is(err, os.ErrNotExist) {
			return Config{}, err
		}
	}

	err = env.ParseWithOptions(&c, env.Options{RequiredIfNoDef: true})
	if err != nil {
		return Config{}, err
	}

	return c, nil
}

func (c KafkaConfig) GetBrokers() []string {
	brokers := strings.ReplaceAll(c.Brokers, " ", "")

	brokersList := strings.Split(brokers, ",")
	var nonEmptyBrokersList []string

	for _, str := range brokersList {
		if str != "" {
			nonEmptyBrokersList = append(nonEmptyBrokersList, str)
		}
	}

	return nonEmptyBrokersList
}
