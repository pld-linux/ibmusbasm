Summary:	IBM Remote Supervisor Adapter (RSA) II daemon
Summary(pl.UTF-8):	Demon IBM Remote Supervisor Adapter (RSA) II
Name:		ibmusbasm
Version:	1.42
Release:	2
License:	GPL
Group:		Applications
Source0:	ftp://ftp.software.ibm.com/systems/support/system_x/ibm_svc_rsa2_hlp242b_linux_32-64.tgz
# Source0-md5:	8b08d5cf722c812e607f99ce852f62f7
Source1:	ibmasm.init
URL:		http://www-304.ibm.com/jct01004c/systems/support/supportsite.wss/docdisplay?lndocid=MIGR-5071676&brandind=5000008
BuildRequires:	libusb-devel >= 0.1.6
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
%ifarch %{x8664}
Requires:	libusb-0.1.so.4()(64bit)
%else
Requires:	libusb-0.1.so.4
%endif
Conflicts:	ibmasm
Conflicts:	ibmasr
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix	/

%description
IBM Remote Supervisor Adapter (RSA) II Daemon package.

%description -l pl.UTF-8
Demon IBM Remote Supervisor Adapter (RSA) II.

%prep
%setup -qc
%ifarch %{ix86}
rpm2cpio SRPMS/ibmusbasm-%{version}-2.src.rpm | cpio -i -d
%{__tar} zxf ibmusbasm-src.tgz
%endif
%ifarch %{x8664}
rpm2cpio SRPMS/ibmusbasm64-%{version}-2.src.rpm | cpio -i -d
%{__tar} zxf ibmusbasm64-src.tgz
mv ibmusbasm{64,}-src
%endif
%{__chmod} -R a+rX ibmusbasm-src
sed -i -e 's/"libusb.so"/"libusb-0.1.so.4"/' ibmusbasm-src/src/ibmasm.c

%build
cd ibmusbasm-src/shlib
%{__cc} %{rpmcflags} -D__IBMLINUX__ -fPIC -shared -I ../src -Wl,-soname -Wl,libsysSp.so.1 -o libsysSp.so.1 uwiapi.c
cd ../src
%{__cc} %{rpmcflags} -I . -o ibmasm ibmasm.c -ldl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_sbindir},%{_sysconfdir},/etc/rc.d/init.d}
install ibmusbasm-src/shlib/libsysSp.so.1 $RPM_BUILD_ROOT%{_libdir}
install ibmusbasm-src/src/ibmasm $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ibmasm
ln -s libsysSp.so.1 $RPM_BUILD_ROOT%{_libdir}/libsysSp.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add ibmasm
%service ibmasm restart

if [ "$1" = "0" ]; then
	%service -q ibmasm stop
	/sbin/chkconfig --del ibmasm
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc readme.txt
%attr(754,root,root) /etc/rc.d/init.d/ibmasm
%attr(755,root,root) %{_libdir}/libsysSp.so
%attr(755,root,root) %{_libdir}/libsysSp.so.1
%attr(755,root,root) %{_sbindir}/ibmasm
