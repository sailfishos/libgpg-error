Summary: Library for error values used by GnuPG components
Name: libgpg-error
Version: 1.27
Release: 1
URL: ftp://ftp.gnupg.org/gcrypt/libgpg-error/
Source0: ftp://ftp.gnupg.org/gcrypt/libgpg-error/%{name}-%{version}.tar.bz2
Patch0: libgpg-error-1.10-adding-pc.patch
Group: System/Libraries
License: LGPLv2+ and GPLv2+
BuildRequires: gawk
BuildRequires: gettext >= 0.19.3
BuildRequires: texinfo
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future. This package
contains files necessary to develop applications using libgpg-error.

%prep
%setup -q -n %{name}-%{version}/%{name}
%patch0 -p1
# The config script already suppresses the -L if it's /usr/lib, so cheat and
# set it to a value which we know will be suppressed.
sed -i -e 's|^libdir=@libdir@$|libdir=@exec_prefix@/lib|g' src/gpg-error-config.in

%build
# The --enable-maintainer-mode is because version.texi file is only generated with that
# See https://www.sourceware.org/ml/guile/2000-01/msg00534.html
%reconfigure --disable-static --enable-maintainer-mode
make

%install
rm -fr $RPM_BUILD_ROOT
%make_install
rm -r $RPM_BUILD_ROOT/%{_datadir}/common-lisp

%find_lang %{name}

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING COPYING.LIB
%{_bindir}/gpg-error
%{_libdir}/libgpg-error.so.*

%files devel
%defattr(-,root,root)
%doc AUTHORS README NEWS ChangeLog
%{_bindir}/gpg-error-config
%{_libdir}/libgpg-error.so
%{_includedir}/gpg-error.h
%{_includedir}/gpgrt.h
%{_datadir}/aclocal/gpg-error.m4
%{_libdir}/pkgconfig/*.pc
%{_datadir}/%{name}/*
%{_datadir}/info/gpgrt.info.gz
%{_datadir}/man/man1/gpg-error-config.1.gz

