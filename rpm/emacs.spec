%global _hardened_build 1
%define mainversion 29.1

# This file is encoded in UTF-8.  -*- coding: utf-8 -*-
Summary:       GNU Emacs text editor
Name:          emacs
Epoch:         1
Version:       %{mainversion}
Release:       1%{?dist}
License:       GPLv3+ and CC0-1.0
URL:           http://www.gnu.org/software/emacs/
Group:         Applications/Editors
Source0:       %{name}-%{version}.tar.xz

BuildRequires: make
BuildRequires: autoconf
BuildRequires: texinfo
BuildRequires: gcc
BuildRequires: dbus-devel
BuildRequires: glibc-devel
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
BuildRequires: gnutls37-devel
BuildRequires: libxml2-devel
BuildRequires: systemd-devel
BuildRequires: gmp-devel
BuildRequires: bzip2
BuildRequires: gzip
BuildRequires: git

Requires(preun): /sbin/install-info
Requires(post): /sbin/install-info
Provides: emacs(bin) = %{epoch}:%{version}-%{release}

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package provides an emacs binary with no X windows support for running
on a terminal.

Type: console-application
Categories:
  - Development
  - Office
  - TextEditor
Custom:
  Repo: https://github.com/sailfishos-chum/emacs
Icon: https://www.gnu.org/software/emacs/images/emacs.png
Screenshots:
  - https://www.gnu.org/software/emacs/images/teaser.png

%prep
%setup -q -n %{name}-%{version}/emacs

%build
./autogen.sh
%configure --with-x-toolkit=no --with-modules
make %{?_smp_mflags} bootstrap

# Sorted list of info files
%define info_files ada-mode auth autotype bovine calc ccmode cl dbus dired-x ebrowse ede ediff edt efaq efaq-w32 eieio eintr elisp emacs-gnutls emacs emacs-mime epa erc ert eshell eudc eww flymake forms gnus htmlfontify idlwave ido info mairix-el message mh-e newsticker nxml-mode octave-mode org pcl-cvs pgg rcirc reftex remember sasl sc semantic ses sieve smtpmail speedbar srecode todo-mode tramp url vhdl-mode viper vip widget wisent woman

# Since the list of info files has to be maintained, check if all info files
# from the upstream tarball are actually present in %%info_files.
cd info
fs=( $(ls *.info) )
is=( %info_files  )
files=$(echo ${fs[*]} | sed 's/\.info//'g | sort | tr -d '\n')
for i in $(seq 0 $(( ${#fs[*]} - 1 ))); do
    if test "${fs[$i]}" != "${is[$i]}.info"; then
        echo Please update %%info_files: ${fs[$i]} != ${is[$i]}.info >&2
        break
    fi
done
cd ..

%install
make install DESTDIR=%{buildroot}
for i in $(find %{buildroot} -name "*.elc"); do
    touch $i
done
mkdir -p %{buildroot}%{_includedir}
cp src/emacs-module.h %{buildroot}%{_includedir}
rm -f %{buildroot}%{_infodir}/info.info.gz
rm -f %{buildroot}%{_infodir}/dir
rm %{buildroot}%{_datadir}/applications/emacs.desktop
rm -rf %{buildroot}%{_datadir}/icons
rm %{buildroot}%{_libdir}/systemd/user/emacs.service

%post
for f in %{info_files}; do
    /sbin/install-info %{_infodir}/%f.info.gz %{_infodir}/dir 2> /dev/null || :
done

%preun
for f in %{info_files}; do
    /sbin/install-info --delete %{_infodir}/%f.info.gz %{_infodir}/dir 2> /dev/null || :
done

%files
%{_bindir}/emacs-%{mainversion}
%{_bindir}/emacs

%license etc/COPYING
%doc etc/NEWS BUGS README
%{_bindir}/ctags
%{_bindir}/ebrowse
%{_bindir}/emacsclient
%{_bindir}/etags
%{_mandir}/*/*
%{_infodir}/*
%dir %{_datadir}/emacs/%{mainversion}
%{_datadir}/emacs/%{mainversion}/etc
%{_datadir}/emacs/%{mainversion}/lisp
%{_datadir}/emacs/%{mainversion}/site-lisp
%{_datadir}/emacs/site-lisp
%{_datadir}/applications/emacs-mail.desktop
%{_datadir}/applications/emacsclient-mail.desktop
%{_datadir}/applications/emacsclient.desktop
%{_datadir}/metainfo/emacs.metainfo.xml
%{_libexecdir}/emacs
%{_includedir}/emacs-module.h

%changelog
* Mon Sep 25 2023 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 1:29.1-1
- New upstream release
* Sat Sep 17 2022 Renaud Casenave-Péré < renaud@casenave-pere.fr> - 1:28.2-1
- New upstream release
* Tue Apr 5 2022 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 1:28.1-1
- New upstream release
* Wed Jul 21 2021 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 1:27.2-2
- Integrate build into OBS
* Sun Mar 28 2021 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 1:27.2-1
- New upstream release
* Mon Dec 7 2020 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 1:27.1-1
- New upstream release
* Sun Sep 8 2019 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 1:26.3-1
- New upstream release
* Sat Apr 20 2019 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 1:26.2-1
- New upstream release
* Wed Jan 23 2019 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 1:26.1-2
- Fix timestamp of precompiled lisp files.
* Sun Jan 06 2019 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 1:26.1-1
- Initial release for sailfishos
