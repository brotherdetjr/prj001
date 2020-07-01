package util

import (
	"github.com/rs/zerolog"
	"os"
)

func CreateLogger(prettyLogging bool, debug bool) *zerolog.Logger {
	logger := zerolog.New(os.Stdout).With().Timestamp().Logger()
	if prettyLogging {
		logger = logger.Output(zerolog.ConsoleWriter{Out: os.Stderr})
	}
	zerolog.SetGlobalLevel(zerolog.InfoLevel)
	if debug {
		zerolog.SetGlobalLevel(zerolog.DebugLevel)
	}
	return &logger
}
