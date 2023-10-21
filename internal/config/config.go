package config

import (
	"errors"
	"fmt"
	"os"

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
		Port     int    `env:"KAFKA_PORT" envDefault:"8090"`
		Host     string `env:"KAFKA_HOST" envDefault:"localhost"`
		User     string `env:"KAFKA_USER" envDefault:"admin"`
		Password string `env:"KAFKA_PASSWORD" envDefault:"password"`
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

func (c KafkaConfig) DSN() string {
	return fmt.Sprintf("amqp://%s:%s@%s:%d/", c.User, c.Password, c.Host, c.Port)
}
