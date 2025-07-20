import sqlite3
import re

class BaseDeDatos():

    con = sqlite3.connect("modelo/mibase.db")

    def crear_tabla(self):
        con = self.con
        try:
            cursor = con.cursor()
            sql = """CREATE TABLE contactos (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                nombre text,
                apellido text,
                telefono integer,
                mail text)"""
            cursor.execute(sql)
            con.commit()
            msg = "Se ha creado la tabla 'contactos'."
            return msg
        except sqlite3.OperationalError:
            msg = "La tabla 'contactos' ya se encuentra creada"
            return msg
        
class Registros(BaseDeDatos):

    def __init__(self, nombre, apellido, telefono, mail):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.mail = mail
        
    def ver():
        con = Registros.con
        cursor = con.cursor()
        sql = "SELECT * FROM contactos"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def alta_datos(self):
        con = self.con
        exp = re.compile("^[a-zA-Z]+[^0-9]$")
        if exp.match(self.nombre) != None:
            cursor = con.cursor()
            data = (self.nombre, self.apellido, self.telefono, self.mail)
            sql = """INSERT INTO contactos (
                nombre,
                apellido, 
                telefono, 
                mail
            ) VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, data)
            con.commit()
            msg = f"Se dio de alta al contacto {self.nombre} {self.apellido}"
            return msg, True
        else:
            msg = "El nombre ingresado no es valido. Intente nuevamente"
            return msg, False
        
    def baja_datos(id):
        con = Registros.con
        cursor = con.cursor()
        data = (id, )
        sql = "DELETE FROM contactos WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()

    def modificar_datos(nombre, apellido, telefono, mail, id):
        con = Registros.con
        exp = re.compile("^[a-zA-Z]+[^0-9]$")
        if exp.match(nombre) != None:
            cursor = con.cursor()
            data = (nombre, apellido, telefono, mail, id)
            sql = """UPDATE contactos SET 
                nombre = ?, 
                apellido = ?, 
                telefono = ?, 
                mail = ? 
                WHERE id = ?"""
            cursor.execute(sql, data)
            con.commit()
            return True
        else:
            return False
        
class Auxiliares():
        
    def check_tabla(tree, message):
        base =  BaseDeDatos()
        msg = base.crear_tabla()
        message.set(msg)
        Auxiliares.ver_datos(0, tree)

    def alta(nombre, apellido, telefono, mail, tree, message):
        registro = Registros(nombre.get(), apellido.get(), telefono.get(), mail.get())
        msg, val = registro.alta_datos()
        message.set(msg)
        if val:
            Auxiliares.ver_datos(1, tree)
            for vars in [nombre, apellido, telefono, mail]:
                vars.set("")
        else:
            pass

    def baja(tree, message):
        item = tree.focus()
        id = tree.item(item)["text"]
        msg = f"Se ha eliminado al contacto {tree.item(item)['values'][0]} {tree.item(item)['values'][1]}"
        message.set(msg)
        tree.delete(item)
        Registros.baja_datos(id)

    def modificar(nombre, apellido, telefono, mail, tree, message):
        item = tree.focus()
        id = tree.item(item)["text"]
        val = Registros.modificar_datos(nombre.get(), apellido.get(), telefono.get(), mail.get(), id)
        if val:
            tree.item(item, values=(nombre.get(), apellido.get(), telefono.get(), mail.get()))
            msg = f"Se ha actualizado el contacto {nombre.get()} {apellido.get()}"
            message.set(msg)
            for vars in [nombre, apellido, telefono, mail]:
                vars.set("")
        else:
            msg = "El nombre ingresado no es válido. Intente nuevamente."
            message.set(msg)

    def tomar(nombre, apellido, telefono, mail, tree):
        item = tree.focus()
        nombre.set(tree.item(item)["values"][0])
        apellido.set(tree.item(item)["values"][1])
        telefono.set(tree.item(item)["values"][2])
        mail.set(tree.item(item)["values"][3])

    def ver_datos(check, tree):
        rows = Registros.ver()
        if check == 0:
            for row in rows:
                tree.insert("", "end", text=str(row[0]), 
                    values=(row[1], row[2], row[3], row[4])
            )
        else:
            tree.insert("", "end", text=str(rows[len(rows)-1][0]),
                    values=(rows[len(rows)-1][1],rows[len(rows)-1][2],
                    rows[len(rows)-1][3],rows[len(rows)-1][4])
            )