from typing import Text
import paho.mqtt.client as mqtt
import pygame 
from  button import Button


humidade = 0

bomba_modo = "auto"
bomba_status = ""

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("humidade")
    client.subscribe("bomba/modo")
    client.subscribe("bomba/status")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global humidade, bomba_status, bomba_modo
    if msg.topic == "humidade":
  #     print(humidade)

       humidade = int(str(msg.payload) [2:-1])
    elif msg.topic == "bomba/modo":
        bomba_modo = str(msg.payload) [2:-5]
    elif msg.topic == "bomba/status":
        bomba_status = str(msg.payload) [2:-1]
  #      print(bomba_status)
 #   print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.27", 1883, 60)
client.loop_start()


width = 1000 
height = 600


pygame.init() 
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("irrigacao arduino")
font = pygame.font.SysFont(None, 50)
b_width = 230
b_height = 80
spacing = 20
on_button = Button ((75,75,75), width / 2 - b_width / 2, 300, b_width, b_height, "Ligar bomba ", 30)
auto_button = Button ((75,75,75), width / 2 - b_width / 2, 300 + spacing + b_height, b_width, b_height, "Bomba automatica ", 30)
off_button = Button ((75,75,75), width / 2 - b_width / 2, 300 + 2* spacing + 2* b_height, b_width, b_height, "Desligar bomba ", 30)
buttons = {"off" : off_button, "on" : on_button, "auto" : auto_button}
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.loop_stop()
            pygame.quit()
        elif event.type == pygame.MOUSEMOTION:
            for button in buttons.values():       
                button.react_to_mouse(event.pos)  
         
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for mode, button in buttons.items():  
                if button.isOver(event.pos): 
                    print("botao")
                    bomba_modo = mode
                    print(mode) 
                    client.publish("bomba/modo", f"{bomba_modo}\0", retain=True)   
    window.fill((0,0,0))
    text = font.render(f"Humidade: {humidade}%", True, (255,255,80))
    window.blit(text,(width/2-text.get_width()/2,100))
    text2 = font.render("Bomba: "+ str(bomba_status), True, (255,255,80))
    window.blit(text2,(width/2-text2.get_width()/2,200))
    for button in buttons. values():
        button.color = (75,75,75)
    buttons[bomba_modo].color = (0,0,120)
    for button in buttons. values():
        button.draw(window,(180,180,180))
    pygame.display.update()
    
