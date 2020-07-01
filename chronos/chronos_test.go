package chronos

import (
	"github.com/stretchr/testify/assert"
	"testing"
	"time"
)

func TestMock(t *testing.T) {
	chronos := Mock()

	assert.Equal(t, 0*time.Nanosecond, chronos.NowNano())
	assert.False(t, chronos.Forward())

	ch := make(chan bool)

	go func() {
		chronos.Sleep(2 * time.Second)
		ch <- true
	}()

	chronos.WaitForSleep()
	assert.True(t, chronos.Forward())
	assert.False(t, chronos.Forward())

	assert.True(t, <-ch)
	assert.Equal(t, 2*time.Second, chronos.NowNano())

	go func() {
		chronos.Sleep(3 * time.Second)
		ch <- true
	}()

	go func() {
		chronos.Sleep(2 * time.Second)
		ch <- true
	}()

	chronos.WaitForSleeps(2)

	assert.True(t, chronos.Forward())

	assert.True(t, <-ch)
	assert.Equal(t, 4*time.Second, chronos.NowNano())

	assert.True(t, chronos.Forward())

	assert.True(t, <-ch)
	assert.Equal(t, 5*time.Second, chronos.NowNano())

	assert.False(t, chronos.Forward())

}
