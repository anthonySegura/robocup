

class Controller:
    '''
        Controlador de las acciones del robot.
        Recibe las detecciones de YOLO o comandos de voz y decide que movimiento mandar al carro
        Poner aqui todo lo relacionado a las intrucciones de Bluetooth
    '''
    __instance = None

    # Para instanciar esta clase hacer: controller = Controller.getInstance()
    @staticmethod
    def getInstance():
        if Controller.__instance == None:
            Controller()
        return Controller.__instance 

    def __init__(self):
        '''
            Hacer en este constructor el emparejamiento al bluetooth, la idea es que solo este
            mae se comunique con el carro
        '''
        # La clase es un singleton, la instancia que este en la parte de YOLO y en el 
        # modulo de reconocimiento de voz va a ser la misma
        if Controller.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Controller.__instance = self
            
        self.frame_counter = 0

    def yolo_instruction(self, *args):
        '''
            Esta función recibe los datos de YOLO: distancia, angulos etc, y en base a eso decide que 
            intrucción enviar por Bluetooth
        '''
        # if self.frame_counter % (algun numero) == 0:
        #     hace algo
        self.frame_counter += 1
        pass

    def voice_intruction(self, command):
        pass
