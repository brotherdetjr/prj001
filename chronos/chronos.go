package chronos

import (
	"github.com/emirpasic/gods/maps/treemap"
	"github.com/emirpasic/gods/utils"
	"time"
)

type Chronos interface {
	NowNano() int64
	Sleep(time.Duration)
}

type RealChronos struct {
	CreatedUnixNano int64
}

func (r *RealChronos) NowNano() int64 {
	return time.Now().UnixNano() - r.CreatedUnixNano
}

func (r *RealChronos) Sleep(duration time.Duration) {
	time.Sleep(duration)
}

func New() Chronos {
	return &RealChronos{CreatedUnixNano: time.Now().UnixNano()}
}

func Mock() *MockChronos {
	return &MockChronos{
		nowNano: 0,
		nanoToC: treemap.NewWith(utils.Int64Comparator),
	}
}

type MockChronos struct {
	nowNano int64
	nanoToC *treemap.Map
}

func (m *MockChronos) NowNano() int64 {
	return m.nowNano
}

func (m *MockChronos) Sleep(duration time.Duration) {
	ch := make(chan int64)
	m.nanoToC.Put(m.NowNano()+duration.Nanoseconds(), ch)
	<-ch
}

func (m *MockChronos) Forward() bool {
	if !m.nanoToC.Empty() {
		newNowNano, ch := m.nanoToC.Min()
		m.nanoToC.Remove(newNowNano)
		m.nowNano = newNowNano.(int64)
		ch.(chan int64) <- newNowNano.(int64)
		return true
	} else {
		return false
	}
}
