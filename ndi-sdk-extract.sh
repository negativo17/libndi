#!/bin/sh

INSTALLER="InstallNDISDK_v3_Linux.sh"
EXTRACTED_ROOT="NDI SDK for Linux"
PACKAGE_NAME="ndi-sdk"

TARBALL_START=$(($(sed -n '/^__NDI_ARCHIVE_BEGIN__$/=' ${INSTALLER}) + 1))

# Get packaging guidelines compatible version
tail -n +"${TARBALL_START}" ${INSTALLER} | tar -zxf - "${EXTRACTED_ROOT}/Version.txt"
VERSION=$(cat "${EXTRACTED_ROOT}/Version.txt" | sed -e 's/-//g' -e 's/ @ /./g')
rm -fr "${EXTRACTED_ROOT}"

# Create tarball with version
mkdir ${PACKAGE_NAME}-${VERSION}
tail -n +"${TARBALL_START}" ${INSTALLER} | tar --strip-components=1 -zxf - -C ${PACKAGE_NAME}-${VERSION} 
tar --remove-files -cJf ${PACKAGE_NAME}-${VERSION}.tar.xz ${PACKAGE_NAME}-${VERSION}

echo "Version:  ${VERSION}"
