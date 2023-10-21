package logger

import (
	"strings"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

const (
	LevelInfo    = "info"
	LevelWarning = "warning"
	LevelError   = "error"
)

func NewLogger(level string) (l *zap.SugaredLogger, err error) {
	cfg := zap.NewProductionConfig()
	cfg.DisableCaller = true

	switch strings.ToLower(level) {
	case LevelInfo:
		cfg.Level = zap.NewAtomicLevelAt(zap.InfoLevel)
	case LevelWarning:
		cfg.Level = zap.NewAtomicLevelAt(zap.WarnLevel)
	case LevelError:
		cfg.Level = zap.NewAtomicLevelAt(zap.ErrorLevel)
	default:
		cfg = zap.NewDevelopmentConfig()
		cfg.EncoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder
	}

	basicLogger, err := cfg.Build()
	l = basicLogger.Sugar()

	return
}
