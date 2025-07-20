class Sujeto:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self):
        pass

    def notificar(self, *args):
        for observador in self.observadores:
            observador.update(args)

class TemaConcreto(Sujeto):
    
    def __init__(self):
        self.estado = None

    def get_estado(self):
        return self.estado

    def set_estado(self, valor):
        self.estado = valor
        self.notificar()

class Observador:
    
    def update():
        raise NotImplementedError("Delegación de actualización")
    
class ObservadorConcretoA(Observador):
    
    def __init__(self, obj):
        self.observador_a = obj
        self.observador_a.agregar(self)
    
    def update(self, *args):
        print("Actualización dentro de Observador ObservadorConcretoA")
        print("Parametros:", args)