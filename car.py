import RPi.GPIO as gpio
import time, pygame, random, sys
import cv2
import threading


#global variables, being used by both threads
onLeft = False
onRight = False
detect = False

class Car:
    '''Main class to control the car'''
    
    def __init__(self):
        '''init pygame and set up gpio in rpi'''
        pygame.init()
        self.screen = pygame.display.set_mode([100, 100])
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
            self._check_detection()

    def _check_detection(self):
        '''read variables updated by CV thread'''
        if detect == True:
            if onLeft == True:
                self._counterclk()                 
                self._stop()
                time.sleep(0.05)
            elif onRight == True:
                self._clk()                
                self._stop()
                time.sleep(0.05)
            elif (onLeft and onRight) == False:
                self._stop()


  
    def _check_events(self):
        '''Determine what key is pressed and change position'''
        for event  in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    '''turn right'''
                    self._clk()                                        
                elif event.key == pygame.K_a:
                    '''turn left'''
                    self._counterclk()                                       
                elif event.key == pygame.K_w:
                    '''move forward'''
                    self._forward()                   
                elif event.key == pygame.K_s:
                    '''move backwards'''
                    self._backward()                                        
                elif event.key == pygame.K_q:
                    '''quit'''
                    gpio.cleanup()
                    sys.exit()                    
                elif event.key == pygame.K_e:
                    '''stop'''
                    self._stop()
                    
                    


    def _forward(self):
        gpio.output(7, True)
        gpio.output(11, False)
        gpio.output(13, False)
        gpio.output(15, True)
        
    def _backward(self):
        gpio.output(7, False)
        gpio.output(11, True)
        gpio.output(13, True)
        gpio.output(15, False)
          
    def _counterclk(self):
        gpio.output(7, True)
        gpio.output(11, False)
        gpio.output(13, True)
        gpio.output(15, True)
          
    def _clk(self):
        gpio.output(7,True)
        gpio.output(11, True)
        gpio.output(13, False)
        gpio.output(15, True)

    def _stop(self):
        gpio.output(7,True)
        gpio.output(11, True)
        gpio.output(13, True)
        gpio.output(15, True)      
        

def cv():
    global onLeft, onRight, detect
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('hand.xml')
    width = cap.get(3)
    height = cap.get(4)
    #creates center region with width 60 pixel if detected midpoint falls within this region it is considered centered. 
    left_thresh = width/2 + 30 
    right_thresh = width/2 - 30

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hand = face_cascade.detectMultiScale(gray, 1.3, 3)
        if len(faces) > 0:
            detect = True
            for x,y,w,h in hand:
                midpoint = x + w/2 #middle x coord of detected rectangle
                cv2.rectangle(frame,(x,y),(x+w, y+h),(255,0,0), 2)
                if midpoint > left_thresh:
                    onRight = True
                    onLeft = False                    
                elif midpoint < right_thresh:
                    onLeft = True
                    onRight = False
                elif midpoint > right_thresh and midpoint < left_thresh:
                    '''centered'''
                    onLeft = False
                    onRight = False
        else:
            detect = False
            onLeft = False
            onRight = False     
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

try:
    if __name__ == "__main__":
        x = threading.Thread(target=cv, daemon=True)
        x.start()
        car1 = Car()
        car = threading.Thread(target=car1.run_car())
        car.start()
except KeyboardInterrupt:
    gpio.cleanup()
    sys.exit()
    cap.release()
    cv2.destroyAllWindows()
