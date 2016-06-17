#!/bin/bash


# clono icaro
git clone https://github.com/valentinbasel/icaro.git



#copio el spec al ~/rpmbuild/SPEC

cp icaro.spec ~/rpmbuild/SPECS/

# entro en la carpeta de git

# tomo el SHA del ultimo commit 
cd icaro/
git checkout master
git=$(git rev-parse HEAD)

# borro el rpm y voy al SOURCE
rm -rf ~/rpmbuild/RPMS/noarch/
cd ~/rpmbuild/SOURCES

# borro todo para dejar el SOURCE limpio
rm *.tar.gz

# descargo el git con el ultimo commit
github="https://github.com/valentinbasel/icaro/archive/"
icaro=$github$git".zip"
file="icaro-"$git".tar.gz"
wget $icaro -O $pwd $file

# armo el RPM
commit="%global commit "$git 
cd ~/rpmbuild/SPECS

# borro la linea commit y la remplazo con el SHA nuevo
sed -i "s/\%global commit .*/$commit/" icaro.spec

rpmbuild -ba icaro.spec


