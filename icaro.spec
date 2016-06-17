%global  __os_install_post %{nil}
%if 0%{?fedora} >= 18
%global activity TurtleBlocks.activity
%else
%global activity TurtleArt.activity
%endif

%global commit 10165151a5806f3298bec76de66464f90c406b02
%global shortcommit %(c=%{commit}; echo ${c:0:7})
Name:		icaro
Version:	1.0.5
Release:	1%{?dist}
Summary:	Robotic Educational Project
# Icaro is licensed under GPLv3
# Pinguino and puf is licensend under LGPLv2
License:	GPLv3 and LGPLv2
URL:		http://roboticaro.org
Source0:	https://github.com/valentinbasel/icaro/archive/%{commit}/%{name}-%{commit}.tar.gz
# Add README in english
#Source1:	README.ENG
BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	desktop-file-utils
BuildRequires:	sugar-toolkit
Requires:	pycairo
Requires:	pygtk2
Requires:	pywebkitgtk
Requires:	pygtksourceview
Requires:	sdcc
Requires:	gputils
Requires:	pyusb
Requires:	python-tools
Requires:	sugar-turtleart
Requires:	pyserial
Requires:	sugar
#Requires:	hicolor-icon-themei
Requires:	python-matplotlib
#Requires:	gnome-python2-rsvg

%description
An educational robotic software aimed to develop robotic 
and programming fundamentals.

%prep
%setup -q -n %{name}-%{commit}

# sugar-turtleart change paths
#%if 0%{?fedora} >= 18
#sed -i -e 's/TurtleArt.activity/TurtleBlocks.activity/' config.dat 
#%endif


# copy README.ENG file to sources as well.
#cp -a %{SOURCE1} .

#empty files
#echo "# Just a comment" > pic16/np05/tmp/stdout

# fix spurious permissions in this files
#chmod -v 0644 README.md COPYING AUTHORS COPYING-LGPLv2
chmod -v 0644 COPYING AUTHORS COPYING-LGPLv2


%build
#Nothing to build

%install
# ------------- Apicaro -------------------------------------

%{__python2} apicaro/setup.py install --root %{buildroot}


# ------------- Icaro ---------------------------------------
mkdir -p %{buildroot}%{_datadir}/%{name}/

cp -p -a  {hardware,imagenes,locale,paletas,clemente} %{buildroot}%{_datadir}/%{name}/
install -p -m 0644 {*.py,version} %{buildroot}%{_datadir}/%{name}/

# Remove po and pot files
find %{buildroot} -name "*.po" | xargs rm -f
find %{buildroot} -name "*.pot" | xargs rm -f
find %{buildroot} -name "#template.pde#" | xargs rm -f


%find_lang %{name}

# Tortucaro plugin for sugar
mkdir -p %{buildroot}%{sugaractivitydir}/%{activity}/plugins/icaro/
cp -a plugintortucaro/icaro/* %{buildroot}%{sugaractivitydir}/%{activity}/plugins/icaro/
mkdir -p %{buildroot}%{sugaractivitydir}/%{activity}/plugins/icaro/icons
cp -a plugintortucaro/icaro/icons/* %{buildroot}%{sugaractivitydir}/%{activity}/plugins/icaro/icons


mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d/
install -p -m 0644  udev/* %{buildroot}%{_sysconfdir}/udev/rules.d/

mkdir -p %{buildroot}%{_bindir}

#create executable of program
cat > icaro <<EOF
#! /bin/bash
python /usr/share/icaro/main.py
EOF

install -p -m 0755 icaro %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/

# Icon 
install -p -D -m 0644 imagenes/icarologo.png  %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/

#create desktop file
desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	%{name}.desktop

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
# Changes permissions files (with spaces in the filenames)
for file in `find %{buildroot}/%{_datadir}/%{name} -type f  -perm /a+x `; do
    chmod -v a-x $file
done

# Delete backup files (with spaces in the filenames)
for file in `find %{buildroot}%{_datadir}/%{name} -type f  -name '*~'`; do
    rm -rf $file
done
IFS=$SAVEIFS


for file in `find %{buildroot}%{_datadir}/%{name} -type f  ! -perm /a+x -name '*.py'`; do
    chmod -vR a+x $file
done

for file in `find %{buildroot}/%{python_sitelib}/%{name} -type f  ! -perm /a+x -name '*.py'`; do
    chmod -vR a+x $file
done

for file in `find %{buildroot}/%{python_sitelib}/apicaro -type f  ! -perm /a+x -name '*.py'`; do
    chmod -vR a+x $file
done

find %{buildroot}%{_datadir}/%{name} -name '__init__.py' | xargs chmod 0644

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi
      
%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :



%files -f %{name}.lang
%doc COPYING AUTHORS COPYING-LGPLv2 
#README.ENG 
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*.py*
%{_datadir}/%{name}/version
%dir %{_datadir}/%{name}/hardware/icaro/componentes
%{_datadir}/%{name}/hardware/icaro/componentes/*

%dir %{_datadir}/%{name}/imagenes
%{_datadir}/%{name}/imagenes/*.png

%dir %{_datadir}/%{name}/clemente
%{_datadir}/%{name}/clemente/*.py



%dir %{_datadir}/%{name}/paletas
%{_datadir}/%{name}/paletas/*.gpl

%dir %{_datadir}/%{name}/imagenes/componentes
%{_datadir}/%{name}/imagenes/componentes/*.png

%dir %{_datadir}/%{name}/imagenes/main
%{_datadir}/%{name}/imagenes/main/*.png

%dir %{_datadir}/%{name}/imagenes/mouse
%{_datadir}/%{name}/imagenes/mouse/*.png
%{_datadir}/%{name}/imagenes/mouse/*.svg
%{_datadir}/%{name}/imagenes/gif/*.gif

%dir %{_datadir}/%{name}/hardware/icaro/ejemplos
%{_datadir}/%{name}/hardware/icaro/ejemplos/*

%{_datadir}/%{name}/imagenes/*.svg
# Pinguino Firmware
# Exception granted by fpc
# For more details, see https://fedorahosted.org/fpc/ticket/253

%dir %{_datadir}/%{name}/hardware/icaro/micro/firmware/pic16
%dir %{_datadir}/%{name}/hardware/icaro/micro/firmware/pic16/lib
%{_datadir}/%{name}/hardware/icaro/imagenes/componentes/*.png

%{_datadir}/%{name}/hardware/icaro/imagenes/gif/*.gif
%{_datadir}/%{name}/hardware/icaro/imagenes/*.png

# rpmlint complains for this file. arch-independent-package-contains-binary-or-object error
# Really not intended as a file for be executed in Fedora host.

%{_datadir}/%{name}/hardware/icaro/micro/firmware/pic16/lib/*.lib
%dir %{_datadir}/%{name}/hardware/icaro/micro/firmware/pic16/lkr

%{_datadir}/%{name}/hardware/icaro/micro/firmware/icaro_lib/*.h
%{_datadir}/%{name}/hardware/icaro/micro/firmware/icaro_lib/*.c


%{_datadir}/%{name}/hardware/icaro/micro/firmware/source/pilas/*.c

%{_datadir}/%{name}/hardware/icaro/micro/firmware/source/tortucaro/*.c
%{_datadir}/%{name}/hardware/icaro/micro/firmware/source/icaroblue/*.c


%{_datadir}/%{name}/hardware/icaro/*.py

%{_datadir}/%{name}/hardware/*.py
%{_datadir}/%{name}/hardware/icaro/modulos/*.py
%{_datadir}/%{name}/hardware/icaro/micro/conf/*.ini



%{_datadir}/%{name}/hardware/icaro/micro/firmware/pic16/lkr/*.lkr
%dir %{_datadir}/%{name}/hardware/icaro/micro/firmware/icaro_lib
%dir %{_datadir}/%{name}/hardware/icaro/micro/firmware/source
%{_datadir}/%{name}/hardware/icaro/micro/firmware/source/*.c
%{_datadir}/%{name}/hardware/icaro/micro/firmware/source/*.pde

%dir %{_datadir}/%{name}/hardware/icaro/micro/firmware/non-free/include/pic16
%{_datadir}/%{name}/hardware/icaro/micro/firmware/non-free/include/pic16/*.h

%dir %{_datadir}/%{name}/hardware/icaro/micro/firmware/non-free/lib/pic16
%{_datadir}/%{name}/hardware/icaro/micro/firmware/non-free/lib/pic16/*.lib

%dir %{_datadir}/%{name}/hardware/icaro/micro/firmware/tmp
%{_datadir}/%{name}/hardware/icaro/micro/firmware/tmp/*.c
%{_datadir}/%{name}/hardware/icaro/micro/firmware/tmp/*.h

%dir %{_datadir}/%{name}/hardware/icaro/micro/firmware/tmp/usb
%{_datadir}/%{name}/hardware/icaro/micro/firmware/tmp/usb/*.c
%{_datadir}/%{name}/hardware/icaro/micro/firmware/tmp/usb/*.h


%{_datadir}/%{name}/hardware/icaro/micro/firmware/temporal/
%{_datadir}/%{name}/hardware/icaro/micro/firmware/tmp/stdout

%dir %{_datadir}/%{name}/hardware/icaro/micro/firmware/pic16/obj
%{_datadir}/%{name}/hardware/icaro/micro/firmware/pic16/obj/*.o


# This is not sugar activity, is a plugin for turtleart
# At present yet not there are Fedora guidelines for plugins.
%dir %{sugaractivitydir}/%{activity}/plugins/icaro/
%{sugaractivitydir}/%{activity}/plugins/icaro/*.py*

%dir %{sugaractivitydir}/%{activity}/plugins/icaro/icons/
%{sugaractivitydir}/%{activity}/plugins/icaro/icons/*.svg

%{python_sitelib}/apicaro*egg*
%{python_sitelib}/apicaro/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/48x48/apps/icarologo.png
%config(noreplace) %{_sysconfdir}/udev/rules.d/26-microchip.rules
%config(noreplace) %{_sysconfdir}/udev/rules.d/41-microchip.rules
%config(noreplace) %{_sysconfdir}/udev/rules.d/99-serial.rules
%config(noreplace) %{_sysconfdir}/udev/rules.d/026-microchip.rules
%config(noreplace) %{_sysconfdir}/udev/rules.d/99-mm-usb-device-blacklist.rules

%changelog
* Sat Jan 10 2015 Eduardo Echeverria <echevemaster@gmail.com>  - 1.0.4-1
- Bump to the new upstream version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 08 2013 Eduardo Echeverria <echevemaster@gmail.com>  - 1.0.3-1
- Bump to the new upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 8 2013 Eduardo Echeverria <echevemaster@gmail.com> - 1.0.2-2
- Fix issues with paths

* Sat Jun 8 2013 Eduardo Echeverria <echevemaster@gmail.com> - 1.0.2-1
- Updated to the new upstream version 1.0.2
- Switch from pygame to pycairo

* Sat Mar 30 2013 Eduardo Echeverria <echevemaster@gmail.com> - 1.0.1-1
- Updated to the new upstream version

* Sat Mar 09 2013 Eduardo Echeverria <echevemaster@gmail.com> - 1.0-3
- Added license LGPLv2 for the firmware
- Add missing requires
- Improve find_lang

* Wed Dec 12 2012 Eduardo Echeverria <echevemaster@gmail.com> - 1.0-2
- Add support to languages
- Add scriplets for icons
- Create executables for icaro
- Fix permissions
- Clean spec

* Fri Sep 28 2012 Yader Velasquez <yaderv@fedoraproject.org> - 1.0-1
- First Initial Packaging
