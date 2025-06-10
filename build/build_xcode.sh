set -euo pipefail

if [[ $# -lt 1 ]]; then
  cat 1>&2 <<EOF
USAGE: $0 product [platform] [method]
product can be one of:
  generative-ai-swift
platform can be one of:
  iOS (default)
  iOS-device
  macOS
  tvOS
  watchOS
  catalyst
  visionOS
method can be one of:
  xcodebuild (default)
  unit
  integration
  spm
EOF
  exit 1
fi

product="$1"
platform="$2"
method="$3"

workspace="."
if [[ $# -gt 3 ]]; then
  workspace="$4"
fi

echo "Building $product for $platform using $method"

scripts_dir=$(dirname "${BASH_SOURCE[0]}")

system=$(uname -s)
case "$system" in
  Darwin)
    xcode_version=$(xcodebuild -version | head -n 1)
    xcode_version="${xcode_version/Xcode /}"
    xcode_major="${xcode_version/.*/}"
    ;;
  *)
    xcode_major="0"
    ;;
esac

# Source function to check if CI secrets are available.
source scripts/check_secrets.sh

# Runs xcodebuild with the given flags, piping output to xcpretty
# If xcodebuild fails with known error codes, retries once.
function RunXcodebuild() {
  echo xcodebuild "$@"

  xcpretty_cmd=(xcpretty)

  result=0
  xcodebuild "$@" | tee xcodebuild.log | "${xcpretty_cmd[@]}" || result=$?

  if [[ $result == 65 ]]; then
    ExportLogs "$@"

    echo "xcodebuild exited with 65, retrying" 1>&2
    sleep 5

    result=0
    xcodebuild "$@" | tee xcodebuild.log | "${xcpretty_cmd[@]}" || result=$?
  fi

  if [[ $result != 0 ]]; then
    echo "xcodebuild exited with $result" 1>&2

    ExportLogs "$@"
    return $result
  fi
}

# Exports any logs output captured in the xcresult
function ExportLogs() {
  python3 "${scripts_dir}/xcresult_logs.py" "$@"
}

ios_flags=(
  -sdk 'iphonesimulator'
)

ios_device_flags=(
  -sdk 'iphoneos'
)

ipad_flags=(
  -sdk 'iphonesimulator'
)

macos_flags=(
  -sdk 'macosx'
)
tvos_flags=(
  -sdk "appletvsimulator"
)
watchos_flags=(
)
visionos_flags=(
)
catalyst_flags=(
  ARCHS=x86_64 VALID_ARCHS=x86_64 SUPPORTS_MACCATALYST=YES -sdk macosx
  CODE_SIGN_IDENTITY=- CODE_SIGNING_REQUIRED=NO CODE_SIGNING_ALLOWED=NO
)

destination=

# Compute standard flags for all platforms
case "$platform" in
  iOS)
    xcb_flags=("${ios_flags[@]}")
    gen_platform=ios
    destination="platform=iOS Simulator,name=iPhone EX1"
    ;;

  iOS-device)
    xcb_flags=("${ios_device_flags[@]}")
    gen_platform=ios
    destination='generic/platform=iOS'
    ;;

  iPad)
    xcb_flags=("${ipad_flags[@]}")
    destination='platform=iOS Simulator,name=iPad Pro (9.7-inch)'
  ;;

  macOS)
    xcb_flags=("${macos_flags[@]}")
    gen_platform=macos
    destination="platform=OS X,arch=x86_64"
    ;;

  tvOS)
    xcb_flags=("${tvos_flags[@]}")
    gen_platform=tvos
    destination='platform=tvOS Simulator,name=Apple TV'
    ;;

  watchOS)
    xcb_flags=("${watchos_flags[@]}")
    destination='platform=watchOS Simulator,name=Apple Watch Series 7 (45mm)'
    ;;

  visionOS)
    xcb_flags=("${visionos_flags[@]}")
    destination='platform=visionOS Simulator'
    ;;

  catalyst)
    xcb_flags=("${catalyst_flags[@]}")
    destination='platform="macOS,variant=Mac Catalyst,name=Any Mac'
    ;;

  all)
    xcb_flags=()
    ;;

  Linux)
    xcb_flags=()
    ;;

  *)
    echo "Unknown platform '$platform'" 1>&2
    exit 1
    ;;
esac

xcb_flags+=(
  ONLY_ACTIVE_ARCH=YES
  CODE_SIGNING_REQUIRED=NO
  CODE_SIGNING_ALLOWED=YES
  COMPILER_INDEX_STORE_ENABLE=NO
)

fail_on_warnings=SWIFT_TREAT_WARNINGS_AS_ERRORS=YES

if [[ $workspace = *.xcodeproj ]] ; then
  RunXcodebuild -project $workspace -scheme $product "${xcb_flags[@]}" $fail_on_warnings $method
else
  RunXcodebuild -workspace $workspace -scheme $product -destination "$destination" "${xcb_flags[@]}" $fail_on_warnings $method
fi
