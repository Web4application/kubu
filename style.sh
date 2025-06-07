# /usr/local.

export MINT_PATH=Mint

if ! which mint >/dev/null 2>&1; then
  echo "mint is not available, install with 'brew install mint'"
  exit 1
fi

system=$(uname -s)

# Joins the given arguments with the separator given as the first argument.
function join() {
  local IFS="$1"
  shift
  echo "$*"
}

# Rules to disable in swiftformat:
swift_disable=(
  # sortedImports is broken, sorting into the middle of the copyright notice.
  sortedImports

  # Too many of our swift files have simplistic examples. While technically
  # it's correct to remove the unused argument labels, it makes our examples
  # look wrong.
  unusedArguments

  # We prefer trailing braces.
  wrapMultilineStatementBraces
)

swift_options=(
  # Mimic Google style.
  --indent 2
  --maxwidth 100
  --wrapparameters afterfirst
  --disable $(join , "${swift_disable[@]}")
)

if [[ $# -gt 0 && "$1" == "test-only" ]]; then
  test_only=true
  swift_options+=(--dryrun)
  shift
else
  test_only=false
fi

#TODO - Find a way to handle spaces in filenames

files=$(
(
  if [[ $# -gt 0 ]]; then
    if git rev-parse "$1" -- >& /dev/null; then
      # Argument was a branch name show files changed since that branch
      git diff --name-only --relative --diff-filter=ACMR "$1"
    else
      # Otherwise assume the passed things are files or directories
      find "$@" -type f
    fi
  else
    # Do everything by default
    find . -type f
  fi
) | sed -E -n '
# find . includes a leading "./" that git does not include
s%^./%%

# Build outputs
\%^build/% d
\%^Debug/% d
\%^Release/% d
\%^.build/% d
\%^.swiftpm/% d

# Sources controlled outside this tree
\%/third_party/% d

# Sources pulled in by the Mint package manager
\%^mint% d

# Format Swift sources only
\%\.swift$% p
'
)

needs_formatting=false
for f in $files; do
  # Match output that says:
  # 1/1 files would have been formatted.  (with --dryrun)
  # 1/1 files formatted.                  (without --dryrun)
  mint run swiftformat "${swift_options[@]}" "$f" 2>&1 | grep '^1/1 files' > /dev/null
  if [[ "$test_only" == true && $? -ne 1 ]]; then
    echo "$f needs formatting."
    needs_formatting=true
  fi
done

if [[ "$needs_formatting" == true ]]; then
  echo "Proposed commit is not style compliant."
  echo "Run scripts/style.sh and git add the result."
  exit 1
fi
