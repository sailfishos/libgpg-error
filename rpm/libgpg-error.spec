Summary: Library for error values used by GnuPG components
Name: libgpg-error
Version: 1.42
Release: 1
URL: https://github.com/sailfishos/libgpg-error
Source0: %{name}-%{version}.tar.bz2
License: LGPLv2+
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
Requires: %{name} = %{version}-%{release}

%description devel
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future. This package
contains files necessary to develop applications using libgpg-error.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

%description doc
Man and info pages for %{name}.

%prep
%autosetup -n %{name}-%{version}/%{name}
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

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m0644 -t $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
        AUTHORS README NEWS ChangeLog

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post doc
if [ -f %{_infodir}/gpgrt.info.gz ]; then
    /sbin/install-info %{_infodir}/gpgrt.info.gz %{_infodir}/dir || :
fi

%preun doc
if [ $1 = 0 -a -f %{_infodir}/gpgrt.info.gz ]; then
   /sbin/install-info --delete %{_infodir}/gpgrt.info.gz %{_infodir}/dir || :
fi

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING COPYING.LIB
%{_bindir}/gpg-error
%{_libdir}/libgpg-error.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/gpg-error-config
%{_bindir}/gpgrt-config
%{_bindir}/yat2m
%{_libdir}/libgpg-error.so
%{_includedir}/gpg-error.h
%{_includedir}/gpgrt.h
%{_datadir}/aclocal/gpgrt.m4
%{_datadir}/aclocal/gpg-error.m4
%{_libdir}/pkgconfig/*.pc
%{_datadir}/%{name}

%files doc
%defattr(-,root,root,-)
%{_infodir}/gpgrt.info.gz
%{_mandir}/man1/gpgrt-config.1.gz
%{_docdir}/%{name}-%{version}
