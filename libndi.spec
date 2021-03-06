%global debug_package %{nil}

Name:           libndi
Epoch:          1
Version:        4.6.2
Release:        1%{?dist}
Summary:        NewTek NDI SDK
License:        NewTek’s NDI® Software Development Kit (SDK) License Agreement
URL:            https://ndi.tv/sdk/
ExclusiveArch:  i686 x86_64 armv7hl

Source0:        https://downloads.ndi.tv/SDK/NDI_SDK_Linux/InstallNDISDK_v4_Linux.tar.gz

BuildRequires:  chrpath
BuildRequires:  sed

%description
This SDK provides the tools and resources developers and manufacturers need to
integrate NDI, NewTek's innovative Network Device Interface technology, into
their own systems, devices and applications.

This package contains the basic libraries and binaries.

%package        devel
Summary:        Development package for %{name}
Requires:       %{name}%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
This package contains development files for %{name}.

%package        docs
Summary:        Documentation for %{name}

%description    docs
This package contains documentation, samples and icons to build solutions based
on the NDI library.

%prep
%autosetup -c

# Unpack makeself
INSTALLER=$(ls *.sh)
TARBALL_START=$(($(sed -n '/^__NDI_ARCHIVE_BEGIN__$/=' ${INSTALLER}) + 1))
tail -n +"${TARBALL_START}" ${INSTALLER} | tar --strip-components=1 -zxf -
cat Version.txt

mv lib/arm-rpi3-linux-gnueabihf ./lib/armv7hl-linux-gnu
mv bin/arm-rpi3-linux-gnueabihf ./bin/armv7hl-linux-gnu

# rpmlint fixes
find . -name "*pp" -exec sed -i -e 's/\r$//' {} \;

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}

install -p -m 0644 include/* %{buildroot}%{_includedir}/

install -p -m 0755 lib/%{_arch}-linux-gnu/* %{buildroot}%{_libdir}/
chrpath -d %{buildroot}%{_libdir}/libndi.so.%{version}
ldconfig -vn %{buildroot}%{_libdir}
ln -sf libndi.so.%{version} %{buildroot}%{_libdir}/libndi.so

install -p -m 0755 bin/%{_arch}-linux-gnu/* %{buildroot}%{_bindir}/

%files
%license "NDI SDK License Agreement.txt" licenses/libndi_licenses.txt
%{_bindir}/ndi-directory-service
%{_bindir}/ndi-record
%{_libdir}/libndi.so.4
%{_libdir}/libndi.so.%{version}

%files devel
%doc examples
%{_includedir}/*
%{_libdir}/libndi.so

%files docs
%license "NDI SDK License Agreement.pdf"
%doc Version.txt documentation/* examples logos

%changelog
* Thu Mar 25 2021 Simone Caronni <negativo17@gmail.com> - 1:4.6.2-1
- Update to 4.6.2, update epoch to match version.
- Revamp SPEC file.

* Mon Oct 15 2018 Simone Caronni <negativo17@gmail.com> - 20181005.r97672-1
- Update to 20181005.r97672 (3.7).

* Mon Jul 16 2018 Simone Caronni <negativo17@gmail.com> - 20180625.r90694-1
- Update to version 3.5.

* Fri Jan 19 2018 Simone Caronni <negativo17@gmail.com> - 20171009.r82134-1
- First build.
