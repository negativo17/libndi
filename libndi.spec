%global debug_package %{nil}

Name:           libndi
Epoch:          1
Version:        6.0.1
Release:        1%{?dist}
Summary:        NewTek NDI SDK
License:        NewTek’s NDI® Software Development Kit (SDK) License Agreement
URL:            https://ndi.tv/sdk/
ExclusiveArch:  i686 x86_64 armv7hl aarch64

Source0:        https://downloads.ndi.tv/SDK/NDI_SDK_Linux/Install_NDI_SDK_v%(echo %{version} | cut -f1 -d '.')_Linux.tar.gz#/ndi-sdk-%{version}.tar.gz

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

mv lib/arm-rpi4-linux-gnueabihf ./lib/armv7hl-linux-gnu
mv bin/arm-rpi4-linux-gnueabihf ./bin/armv7hl-linux-gnu

mv lib/aarch64-rpi4-linux-gnueabi ./lib/aarch64-linux-gnu
mv bin/aarch64-rpi4-linux-gnueabi ./bin/aarch64-linux-gnu

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
%{_bindir}/ndi-benchmark
%{_bindir}/ndi-directory-service
%{_bindir}/ndi-free-audio
%{_bindir}/ndi-record
%{_libdir}/libndi.so.%(echo %{version} | cut -f1 -d '.')
%{_libdir}/libndi.so.%{version}

%files devel
%{_includedir}/*
%{_libdir}/libndi.so

%files docs
%license "NDI SDK License Agreement.pdf" licenses/libndi_licenses.txt
%doc Version.txt documentation/* examples

%changelog
* Fri Sep 27 2024 Simone Caronni <negativo17@gmail.com> - 1:6.0.1-1
- Update to 6.0.1.
- Trim changelog.

* Mon Oct 02 2023 Simone Caronni <negativo17@gmail.com> - 1:5.6.0-1
- Update to 5.6.0.

* Sat Mar 11 2023 Simone Caronni <negativo17@gmail.com> - 1:5.5.3-1
- Update to version 5.5.3.

* Sun Mar 13 2022 Simone Caronni <negativo17@gmail.com> - 1:5.1.1-1
- Update to 5.1.1 (NDI 2022-02-10 r129281 v5.1.1)
- Enable aarch64 support.
