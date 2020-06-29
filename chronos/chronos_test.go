package chronos

import (
	"github.com/stretchr/testify/assert"
	"runtime"
	"testing"
	"time"
)

func TestMock(t *testing.T) {
	chronos := Mock()

	assert.Equal(t, int64(0), chronos.NowNano())
	assert.False(t, chronos.Forward())

	ch := make(chan bool)

	go func() {
		chronos.Sleep(2 * time.Second)
		ch <- true
	}()

	for !chronos.Forward() {
		runtime.Gosched()
	}

	assert.True(t, <-ch)

}
