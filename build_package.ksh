#!/usr/bin/ksh
# Modernized AIX Package Build Script
# Usage: ./build_package.ksh /path/to/tempdir

# Enable strict error handling
set -e
trap 'echo "[ERROR] Command failed at line $LINENO." >&2' ERR

# Input validation
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <temp_directory>"
  exit 1
fi

TEMPDIR=$1
BUILD=$(pwd)
. build/aix/pkginfo

# Variables
package=$PKG
name=$NAME
vrmf=$VERSION
descr="$VENDOR $NAME for $ARCH"
INFO=$BUILD/build/aix/.info
template=${INFO}/${PKG}.${NAME}.${vrmf}.template
FILES_TO_PACKAGE="./httpd-root"
LOGFILE=$BUILD/build/aix/package_build.log

mkdir -p $INFO
> $template
echo "[INFO] Build started at $(date)" | tee -a $LOGFILE

cd ${TEMPDIR}

# Clean old metadata dirs (safe cleanup)
rm -rf .info lpp_name tmp

# Directories to measure sizes dynamically
DIRS_TO_MEASURE="etc opt var"
declare -A dir_sizes

for d in $DIRS_TO_MEASURE; do
  target_dir="$d/${NAME}"
  if [ -d "$target_dir" ]; then
    size_blocks=$(du -s "$target_dir" | awk '{print $1}')
    dir_sizes[$d]=$((size_blocks + 1))
    echo "[INFO] Directory $target_dir size: ${dir_sizes[$d]} blocks" | tee -a $LOGFILE
  else
    echo "[WARN] Directory $target_dir does not exist, size set to 0" | tee -a $LOGFILE
    dir_sizes[$d]=0
  fi
done

# Size for /usr/share/man (common for all)
man_dir="usr/share/man"
if [ -d "$man_dir" ]; then
  szman=$(du -s $man_dir | awk '{print $1}')
  szman=$((szman + 1))
  echo "[INFO] Directory $man_dir size: $szman blocks" | tee -a $LOGFILE
else
  echo "[WARN] Directory $man_dir does not exist, size set to 0" | tee -a $LOGFILE
  szman=0
fi

# Fix permissions and ownership for package files
find ${FILES_TO_PACKAGE} -type d -exec chmod og+rx {} \;
chmod -R go+r ${FILES_TO_PACKAGE}
chown -R 0:0 ${FILES_TO_PACKAGE}

# Generate template metadata
cat <<EOF >> $template
Package Name: ${package}.${NAME}
Package VRMF: ${vrmf}.0
Update: N
Fileset
  Fileset Name: ${package}.${NAME}.rte
  Fileset VRMF: ${vrmf}.0
  Fileset Description: ${descr}
  USRLIBLPPFiles
  EOUSRLIBLPPFiles
  Bosboot required: N
  License agreement acceptance required: N
  Include license files in this package: N
  Requisites:
        Upsize: /usr/share/man ${szman};
        Upsize: /etc/${NAME} ${dir_sizes[etc]};
        Upsize: /opt/${NAME} ${dir_sizes[opt]};
        Upsize: /var/${NAME} ${dir_sizes[var]};
  USRFiles
EOF

# Append file list relative to package root
find ${FILES_TO_PACKAGE} | sed -e "s#^${FILES_TO_PACKAGE}##" | sed -e "/^$/d" >> $template

cat <<EOF >> $template
  EOUSRFiles
  ROOT Part: N
  ROOTFiles
  EOROOTFiles
  Relocatable: N
EOFileset
EOF

cp $template ${BUILD}/build/aix

# Build fileset with mkinstallp
mkinstallp -d ${TEMPDIR} -T ${template}

BFF_FILE="${TEMPDIR}/tmp/${PKG}.${NAME}.${VERSION}.0.bff"

if [ ! -f "$BFF_FILE" ]; then
  echo "[ERROR] Fileset creation failed: $BFF_FILE not found" | tee -a $LOGFILE
  exit 1
fi

cp "$BFF_FILE" ${BUILD}/build/aix

cd $BUILD/build/aix

ARCH=$(uname -m)  # dynamically fetch architecture
mv $PKG.$NAME.$VERSION.0.bff $PKG.$NAME.$VERSION.$ARCH.I

rm -f .toc
inutoc .

# Verify package files before install
echo "[INFO] Listing files in package:" | tee -a $LOGFILE
installp -d . -L | tee -a $LOGFILE

echo "[INFO] Applying package install:" | tee -a $LOGFILE
installp -d . -ap ${PKG}.${NAME} | tee -a $LOGFILE

echo "[INFO] Build finished successfully at $(date)" | tee -a $LOGFILE
