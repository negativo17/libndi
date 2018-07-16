Name:     libndi
Version:  20180625.r90694
Release:  1%{?dist}
Summary:  NewTek NDI SDK      
License:  Proprietary    
URL:      https://www.newtek.com/ndi/sdk/

ExclusiveArch: i686 x86_64 armv7hl

Source0:  %{name}-%{version}.tar.xz
Source1:  %{name}-generate-tarball.sh

BuildRequires: sed

%description
This SDK provides the tools and resources developers and manufacturers need to
integrate NDI, NewTek's innovative Network Device Interface technology, into
their own systems, devices and applications.

%package        devel
Summary:        Development package for %{name}
Requires:       %{name}%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
This SDK provides the tools and resources developers and manufacturers need to
integrate NDI, NewTek's innovative Network Device Interface technology, into
their own systems, devices and applications.

This package contains development files for %{name}.

%prep
%autosetup
mkdir -p .%{_prefix}

%ifarch x86_64
mv lib/x86_64-linux-gnu .%{_libdir}
%endif
%ifarch i686
mv lib/i686-linux-gnu .%{_libdir}
%endif
%ifarch armv7hl
mv lib/arm-linux-gnueabihf .%{_libdir}
%endif

pushd ./%{_libdir}
  ln -sf libndi.so.* libndi.so
  ldconfig -vn .
popd

%install
mkdir -p %{buildroot}%{_prefix}

cp -a include .%{_libdir} %{buildroot}%{_prefix}/

%files
%license "NDI License Agreement.pdf"
%{_libdir}/libndi.so.*

%files devel
%doc Version.txt examples documentation/*
%{_includedir}/*
%{_libdir}/libndi.so

%changelog
* Mon Jul 16 2018 Simone Caronni <negativo17@gmail.com> - 20180625.r90694-1
- Update to version 3.5.

* Fri Jan 19 2018 Simone Caronni <negativo17@gmail.com> - 20171009.r82134-1
- First build.
