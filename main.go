package main

import (
	"flag"
	"github.com/brotherdetjr/prj001/chronos"
	"github.com/brotherdetjr/prj001/engine"
	"github.com/brotherdetjr/prj001/util"
)

type Args struct {
	PrettyLogging bool
	Debug         bool
}

func main() {
	args := parseArgs()
	logger := util.CreateLogger(args.PrettyLogging, args.Debug)
	logger.Info().Msg("Starting prj001...")
	engine.New(logger, chronos.New()).AwaitShutdown()
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
