# sistema citas medicas

from datetime import datetime

class Paciente:
    def __init__(self, nombre, edad, correo):
        self.nombre = nombre
        self.edad = edad
        self.correo = correo
        self.citas = []

    def agendar_cita(self, cita):
        self.citas.append(cita)

    def mostrar_citas(self):
        print(f"\nCitas de {self.nombre}:")
        if not self.citas:
            print("No hay citas agendadas.")
        else:
            for cita in self.citas:
                print(cita)


class Doctor:
    def __init__(self, nombre, especialidad):
        self.nombre = nombre
        self.especialidad = especialidad

    def __str__(self):
        return f"Dr(a). {self.nombre} - {self.especialidad}"


class CitaMedica:
    def __init__(self, paciente, doctor, fecha_hora):
        self.paciente = paciente
        self.doctor = doctor
        self.fecha_hora = fecha_hora

    def __str__(self):
        return f"{self.fecha_hora.strftime('%d/%m/%Y %H:%M')} - {self.paciente.nombre} con {self.doctor.nombre}"


class CentroMedico:
    def __init__(self, nombre):
        self.nombre = nombre
        self.doctores = []
        self.citas = []

    def registrar_doctor(self, doctor):
        self.doctores.append(doctor)

    def mostrar_doctores(self):
        print(f"\nDoctores disponibles en {self.nombre}:")
        for doctor in self.doctores:
            print(doctor)

    def agendar_cita(self, paciente, doctor, fecha_hora):
        cita = CitaMedica(paciente, doctor, fecha_hora)
        self.citas.append(cita)
        paciente.agendar_cita(cita)
        print("Cita agendada correctamente.")

    def mostrar_todas_las_citas(self):
        print(f"\nCitas registradas en {self.nombre}:")
        if not self.citas:
            print("No hay citas agendadas.")
        else:
            for cita in self.citas:
                print(cita)


# ----------- Simulación del sistema -----------

if __name__ == "__main__":
    # Crear el centro médico
    centro = CentroMedico("Centro Salud Total")

    # Registrar doctores
    doctora_gabriela = Doctor("Gabriela Andrade", "Pediatría")
    doctor_cristian = Doctor("Cristian Ruiz", "Medicina Interna")
    centro.registrar_doctor(doctora_gabriela)
    centro.registrar_doctor(doctor_cristian)

    # Mostrar los doctores disponibles
    centro.mostrar_doctores()

    # Crear paciente
    paciente_anita = Paciente("Anita Guzmán", 38, "anita.guzman@example.com")

    # Agendar una cita con el Dr. Cristian Ruiz
    fecha_cita = datetime(2025, 8, 24, 15, 29)
    centro.agendar_cita(paciente_anita, doctor_cristian, fecha_cita)

    # Mostrar citas del paciente
    paciente_anita.mostrar_citas()

    # Mostrar todas las citas registradas en el centro
    centro.mostrar_todas_las_citas()