package engine

import (
	"github.com/brotherdetjr/prj001/chronos"
	"github.com/brotherdetjr/prj001/util"
	"github.com/stretchr/testify/assert"
	"testing"
	"time"
)

func TestProcessItem(t *testing.T) {
	// given
	ch := make(chan bool)
	chronos := chronos.Mock()
	engine := New(util.CreateLogger(true, true), chronos)
	world := World{Engine: engine, StateUpdateCh: make(chan *Item)}
	itemType := ItemType{UpdateState: func(item *Item, nowNano time.Duration) {
		switch item.State {
		case 1:
			item.State = 2
			item.ScheduleStateUpdate(2 * time.Second)
			item.ScheduleStateUpdate(3 * time.Second)
		case 2:
			item.State = 3
		case 3:
			item.State = 4
		}
		ch <- true
	}}
	item := Item{
		World: &world,
		Type:  &itemType,
		State: 1,
	}

	// when
	go world.Run()

	// then
	assert.Equal(t, 1, item.State)

	// when
	item.ScheduleStateUpdate(0)
	chronos.WaitForSleep()
	chronos.Forward()
	<-ch

	// then
	assert.Equal(t, 2, item.State)

	// when
	//time.Sleep(1 * time.Second)
	chronos.WaitForSleeps(2)
	chronos.Forward()
	<-ch

	// then
	assert.Equal(t, 3, item.State)

	// when
	//time.Sleep(1 * time.Second)
	chronos.Forward()
	<-ch

	// then
	assert.Equal(t, 4, item.State)

}
