package chronos

import (
	"github.com/emirpasic/gods/maps/treemap"
	"github.com/emirpasic/gods/utils"
	"time"
)

type Chronos interface {
	NowNano() time.Duration
	Sleep(time.Duration)
}

type RealChronos struct {
	CreatedUnixNano int64
}

func (r *RealChronos) NowNano() time.Duration {
	return time.Duration(time.Now().UnixNano() - r.CreatedUnixNano)
}

func (r *RealChronos) Sleep(duration time.Duration) {
	time.Sleep(duration)
}

func New() Chronos {
	return &RealChronos{CreatedUnixNano: time.Now().UnixNano()}
}

func Mock() *MockChronos {
	return &MockChronos{
		waitForSleepCh: make(chan bool),
		nowNano:        0,
		nanoToCh:       treemap.NewWith(utils.Int64Comparator),
	}
}

type MockChronos struct {
	waitForSleepCh chan bool
	nowNano        int64
	nanoToCh       *treemap.Map
}

func (m *MockChronos) NowNano() time.Duration {
	return time.Duration(m.nowNano)
}

func (m *MockChronos) Sleep(duration time.Duration) {
	var ch chan int64
	if duration > 0 {
		ch = make(chan int64)
		m.nanoToCh.Put(m.nowNano+duration.Nanoseconds(), ch)
	}
	m.waitForSleepCh <- true
	if duration > 0 {
		//noinspection GoNilness
		<-ch
	}
}

func (m *MockChronos) Forward() bool {
	if !m.nanoToCh.Empty() {
		newNowNano, ch := m.nanoToCh.Min()
		m.nanoToCh.Remove(newNowNano)
		m.nowNano = newNowNano.(int64)
		ch.(chan int64) <- newNowNano.(int64)
		return true
	} else {
		return false
	}
}

func (m *MockChronos) WaitForSleep() {
	<-m.waitForSleepCh
}

func (m *MockChronos) WaitForSleeps(count int) {
	for i := 0; i < count; i++ {
		m.WaitForSleep()
	}
}
