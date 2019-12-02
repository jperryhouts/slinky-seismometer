import gpiozero
import numpy
from datetime import datetime

from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('ggplot')

def shift_append(a, val):
    a[:-1] = a[1:]
    a[-1] = val

with gpiozero.MCP3208(channel=0, differential=True, max_voltage=3.3) as adc:
    dt = 100
    N = int(10 * 1000.0/dt * 1.5)
    print('dt:',dt)
    print('N:',N)
    
    start_time = datetime.now().timestamp()
    
    x = numpy.linspace(-N*dt/1000.0, 0.0, N)
    y = numpy.zeros(N)
    z = numpy.zeros(N)
    window = numpy.zeros(int(numpy.round(1000.0/dt)))
    
    fig, ax = plt.subplots(1,1)
    ln1, = plt.plot(x, y, 'k-')
    ln2, = plt.plot(x, z, 'b-')
    
    def init():
        ax.set_ylim(-1,1)
        ax.set_xlim(-dt/1000.0*N/1.5, 1.0)
        #return ln1,
        return (ln1, ln2)
    
    def update(i):
        window[i%window.size] = 2.0*adc.value - 1.0

        now = datetime.now().timestamp()-start_time
        shift_append(x, now)
        shift_append(y, window.mean())
        shift_append(z, window[i%window.size])
        
        ln1.set_data(x-now, y)
        ln2.set_data(x-now, z)
        #return ln1,
        return (ln1,ln2)
    
    ani = animation.FuncAnimation(fig, update, interval=dt,
                                    init_func=init, blit=True)
    plt.show()
