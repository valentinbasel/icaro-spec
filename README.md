### icaro-spec
Spec de prueba, para generar el paquete RPM de icaro (no es el SPEC oficial de FEDORA)

## preparando el sistema

luego de clonar el repositorio, hay que instalar las siguientes dependencias:

    sudo dnf install -y wget @development-tools fedora-packager

## librerias

    sudo dnf install -y python2-devl sugar-toolkit 

## preparando la instalación

    rpmdev-setuptree

Este comando creara la carpeta rpmbuilds donde se creara el paquete RPM de icaro

## creando el rpm

para crear el rpm, usar el script "crear_rpm.sh", que se encarga de clonar icaro, buscar el ultimo commit de la rama devel, y ejecutar el comando rpmbuild para hacer el .rpm

Una ves instalado, agregar al usuario a los grupos microchip y dialup

    sudo groupadd microchip
    sudo usermod -a -G microchip $USER
    sudo usermod -a -G dialout $USER

Esto es solo una prueba para poder istalar la ultima version de la rama DEVEL de icaro, no es el RPM ofcial, mantenido por eduardo Echeverria (A.K.A echevemaster).


