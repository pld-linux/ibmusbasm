Summary:	IBM Remote Supervisor Adapter (RSA) II daemon
Name:		ibmusbasm
Version:	1.37
Release:	0.1
License:	GPL
Group:		Applications
Source0:	ftp://ftp.software.ibm.com/systems/support/system_x/ibm_svc_rsa2_hlp237a_linux_32-64.tgz
# Source0-md5:	cf9ff9cdfb702b7c0268fd0bcd29274c
URL:		http://www.ibm.com
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	libusb
Conflicts:	ibmasm
Conflicts:	ibmasr
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix	/

%description
IBM Remote Supervisor Adapter (RSA) II Daemon package.

%prep
%setup -qc
%ifarch %{ix86}
rpm2cpio SRPMS/ibmusbasm-%{version}-2.src.rpm | cpio -i -d
%endif
%ifarch %{x8664}
rpm2cpio SRPMS/ibmusbasm64-%{version}-2.src.rpm | cpio -i -d
%endif
%{__tar} zxf ibmusbasm-src.tgz
chmod -R a+rX ibmusbasm-src

%build
cd ibmusbasm-src/shlib
%{__cc} %{rpmcflags} -D__IBMLINUX__ -fPIC -shared -I ../src -o libsysSp.so.1 uwiapi.c
cd ../src
%{__cc} %{rpmcflags} -I . -o ibmasm ./ibmasm.c -ldl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_sbindir},%{_sysconfdir},/etc/rc.d/init.d}
install ibmusbasm-src/shlib/libsysSp.so.1 $RPM_BUILD_ROOT%{_libdir}
install ibmusbasm-src/src/ibmasm $RPM_BUILD_ROOT%{_sbindir}
install ibmusbasm-src/ibmspup ibmusbasm-src/ibmspdown $RPM_BUILD_ROOT%{_sbindir}
install ibmasm.initscript $RPM_BUILD_ROOT/etc/rc.d/init.d/ibmasm
ln -s libsysSp.so.1 $RPM_BUILD_ROOT%{_libdir}/libsysSp.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc readme.txt
%attr(754,root,root) /etc/rc.d/init.d/ibmasm
%attr(755,root,root) %{_libdir}/libsysSp.so.1
%attr(755,root,root) %{_sbindir}/ibmasm
%attr(755,root,root) %{_sbindir}/ibmspdown
%attr(755,root,root) %{_sbindir}/ibmspup
