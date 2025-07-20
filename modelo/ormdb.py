from peewee import *
from datetime import datetime
from logs.observer import Sujeto
import re

if __name__ != "__main__":

    try:
        db = SqliteDatabase("modelo/mibase.db")

        class BaseModel(Model):
            class Meta():
                database = db

        class Contactos(BaseModel):
            id = AutoField()
            nombre = CharField(max_length=20)
            apellido = CharField(max_length=20)
            telefono = IntegerField(unique=True)
            mail = CharField(max_length=30)

        db.connect(reuse_if_open=True)
        db.create_tables([Contactos])

    except ConnectionError as error:
        print("Ha ocurrido un error de conexión: ", error)

    else:

        def console_log(func):
            def wrapper(*args):
                with open("logs/logs.txt", "a") as f:
                    if func.__name__ == "baja":
                        f.write(f"""[{datetime.today()}] - Se ha ejecutado el comando: {func.__name__}\n""")
                    else:
                        f.write(f"""[{datetime.today()}] - Se ha ejecutado el comando: {func.__name__, 
                            args[1].get(), args[2].get()}\n""")
                    func(*args)
            return wrapper

        class CRUD(Sujeto):

            @console_log
            def alta(self, nombre, apellido, telefono, mail, tree, message):
                contacto = Contactos()
                contacto.nombre = nombre.get()
                contacto.apellido = apellido.get()
                contacto.telefono = telefono.get()
                contacto.mail = mail.get()
                if self.validar_campo(contacto.nombre):
                    contacto.save()
                    self.actualizar_treeview(tree)
                    msg = f"Se dio de alta al contacto {contacto.nombre} {contacto.apellido}"
                    self.notificar("Alta de contacto" ,contacto.nombre, contacto.apellido)
                    for var in [nombre, apellido, telefono, mail]:
                        var.set("")
                else:
                    msg = "El nombre ingresado no es valido. Intente nuevamente"
                message.set(msg)

            @console_log
            def modificar(self, nombre, apellido, telefono, mail, tree, message):
                item = tree.focus()
                mi_id = tree.item(item)["text"]
                if self.validar_campo(nombre.get()):
                    actualizar = Contactos.update(nombre=nombre.get(),
                        apellido=apellido.get(), telefono=telefono.get(),
                        mail=mail.get()
                    ).where(Contactos.id==mi_id)
                    actualizar.execute()
                    self.actualizar_treeview(tree)
                    msg = f"Se ha actualizado el contacto {nombre.get()} {apellido.get()}"
                    self.notificar("Modificación de contacto" ,nombre.get(), apellido.get())
                    for var in [nombre, apellido, telefono, mail]:
                        var.set("")
                else:
                    msg = "El nombre ingresado no es valido. Intente nuevamente"
                message.set(msg)

            @console_log
            def baja(self, tree, message):
                item = tree.focus()
                mi_id = tree.item(item)["text"]
                borrar = Contactos.get(Contactos.id==mi_id)
                borrar.delete_instance()
                self.notificar("Baja de contacto" , tree.item(item)['values'][0], tree.item(item)['values'][1])
                msg = f"Se ha eliminado al contacto {tree.item(item)['values'][0]} {tree.item(item)['values'][1]}"
                message.set(msg)
                tree.delete(item)
                self.actualizar_treeview(tree)
            
            def tomar(self, nombre, apellido, telefono, mail, tree):
                item = tree.focus()
                nombre.set(tree.item(item)["values"][0])
                apellido.set(tree.item(item)["values"][1])
                telefono.set(tree.item(item)["values"][2])
                mail.set(tree.item(item)["values"][3])

            def actualizar_treeview(self, tree):
                registros = tree.get_children()
                for registro in registros:
                    tree.delete(registro)
                for row in Contactos.select():
                    tree.insert("", "end", text=str(row.id), 
                        values=(row.nombre, row.apellido, row.telefono, row.mail)
                    )

            def validar_campo(self, campo):
                exp = re.compile("^[a-zA-Z]+[^0-9]$")
                return exp.match(campo)