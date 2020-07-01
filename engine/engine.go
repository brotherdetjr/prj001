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
	Engine *Engine
	//CreatedNano uint64
	//Parent           *World
	//ParentTick       int64
	StateUpdateCh chan *Item
	PoisonCh      chan int8
	//IntentionChannel chan
	//Cells []Cell
}

type Cell struct {
	ObstacleCount uint16
	Items         map[uint16]*Item
}

func (w *World) Run() {
	run := true
	for run {
		select {
		case item := <-w.StateUpdateCh:
			item.Type.UpdateState(item, w.Engine.Chronos.NowNano())
		case <-w.PoisonCh:
			run = false
		}
	}
}

type ItemType struct {
	UpdateState func(item *Item, nowNano time.Duration)

	//Obstacle bool
	//Sprite   string
}

type Item struct {
	World *World
	Type  *ItemType
	State interface{}
}

func (i *Item) ScheduleStateUpdate(interval time.Duration) {
	go func() {
		i.World.Engine.Chronos.Sleep(interval)
		i.World.StateUpdateCh <- i
	}()
}
