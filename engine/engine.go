package engine

import (
	"github.com/brotherdetjr/prj001/chronos"
	"github.com/rs/zerolog"
	"os"
	"os/signal"
	"syscall"
	"time"
)

type Engine struct {
	Logger  *zerolog.Logger
	Chronos chronos.Chronos
}

func New(logger *zerolog.Logger, chronos chronos.Chronos) *Engine {
	var engine = Engine{
		Logger:  logger,
		Chronos: chronos,
	}
	go engine.run()
	return &engine
}

func (e *Engine) AwaitShutdown() *Engine {
	var shutdownCh = make(chan os.Signal, 1)
	signal.Notify(shutdownCh, syscall.SIGINT, syscall.SIGTERM)
	sig := <-shutdownCh
	e.Logger.Info().
		Str("signal", sig.String()).
		Msg("Shutting down")
	// here we will be closing open connections et al
	return e
}

func (e *Engine) run() {
	for {
		e.Logger.Info().Msg("Engine is running...")
		time.Sleep(1 * time.Second)
	}
}

type World struct {
	Engine Engine
	//CreatedNano uint64
	//Parent           *World
	//ParentTick       int64
	StateUpdateC chan *Item
	//IntentionChannel chan
	//Cells []Cell
}

type Cell struct {
	ObstacleCount uint16
	Items         map[uint16]*Item
}

func (w *World) run() {
	for {
		select {
		case item := <-w.StateUpdateC:
			processItem(item)
		}
	}
}

func processItem(item *Item) {
	world := item.World
	engine := world.Engine
	for _, subsequentRequest := range item.Type.UpdateState(item, engine.Chronos.NowNano()) {
		go func(r StateUpdateRequest) {
			engine.Chronos.Sleep(r.ScheduleIn)
			world.StateUpdateC <- r.Item
		}(subsequentRequest)
	}
}

type StateUpdateRequest struct {
	ScheduleIn time.Duration
	Item       *Item
}

type ItemType struct {
	UpdateState func(item *Item, nowNano int64) []StateUpdateRequest

	//Obstacle bool
	//Sprite   string
}

type Item struct {
	World *World
	Type  *ItemType
}
