package main

import (
	"flag"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"os"
)

type Args struct {
	PrettyLogging bool
	Debug         bool
}

func main() {
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})
	log.Info().Msg("Starting prj001...")
	//engine.New(createLogger(parseArgs())).AwaitShutdown()
}

func parseArgs() Args {
	prettyLogging := flag.Bool(
		"prettyLogging",
		true,
		"Outputs the log prettily printed and colored (slower)")
	debug := flag.Bool("debug", false, "Sets log level to debug")
	flag.Parse()

	return Args{
		PrettyLogging: *prettyLogging,
		Debug:         *debug,
	}
}

func createLogger(args Args) *zerolog.Logger {
	logger := zerolog.New(os.Stdout).With().Timestamp().Logger()
	if args.PrettyLogging {
		logger = logger.Output(zerolog.ConsoleWriter{Out: os.Stderr})
	}
	zerolog.SetGlobalLevel(zerolog.InfoLevel)
	if args.Debug {
		zerolog.SetGlobalLevel(zerolog.DebugLevel)
	}
	return &logger
}
