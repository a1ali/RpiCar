import RPi.GPIO as gpio
import time, pygame, random, sys


class Car:
    '''Main class to control the car'''

    def __init__(self):
        '''init pygame and set up gpio in rpi'''
        pygame.init()
        self.screen = pygame.display.set_mode((200,200))
        gpio.cleanup()
        self._setpin()
        

    def _setpin(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(7, gpio.OUT)
        gpio.setup(11, gpio.OUT)
        gpio.setup(13, gpio.OUT)
        gpio.setup(15, gpio.OUT)
        
    def run_car(self):
        '''Main loop '''
        while True:
            self._check_events()
            #gpio.cleanup()
            #self._stop()

    def _check_events(self):
        '''Determine what key is pressed and change position'''

        for event  in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    '''turn right'''
                    self._clk()
                    print('d')
                    
                elif event.key == pygame.K_a:
                    '''turn left'''
                    self._counterclk()
                    
                    print('a')
                elif event.key == pygame.K_w:
                    '''move forward'''
                    self._forward()
                    print('w')
                    
                elif event.key == pygame.K_s:
                    '''move backwards'''
                    self._backward()
                    print('s')
                    
                elif event.key == pygame.K_q:
                    '''quit'''
                    gpio.cleanup()
                    sys.exit()
                    #gpio.clean()
                    print('q')

                elif event.key == pygame.K_e:
                    '''stop'''
                    self._stop()
                    print('stopped')
                    
            if len(pygame.key.get_pressed()) == 0:
                self._stop()

    def _forward(self):
        #self._setpin()


        gpio.output(7, True)
        gpio.output(11, False)
        gpio.output(13, False)
        gpio.output(15, True)
        
        #gpio.cleanup()
    
    def _backward(self):
        #self._setpin()
        gpio.output(7, False)
        gpio.output(11, True)
        gpio.output(13, True)
        gpio.output(15, False)
        
        #gpio.cleanup()
    
    def _counterclk(self):
        #self._setpin()
        gpio.output(7, True)
        gpio.output(11, False)
        gpio.output(13, True)
        gpio.output(15, True)
        
        #gpio.cleanup()
    
    def _clk(self):
        #self._setpin()
        gpio.output(7,True)
        gpio.output(11, True)
        gpio.output(13, False)
        gpio.output(15, True)

    def _stop(self):
        #self._setpin()
        gpio.output(7,True)
        gpio.output(11, True)
        gpio.output(13, True)
        gpio.output(15, True)      
        
        #gpio.cleanup()  

try:
    if __name__ == "__main__":
        car1 = Car()
        car1.run_car()
except KeyboardInterrupt:
    gpio.cleanup()
    sys.exit()
