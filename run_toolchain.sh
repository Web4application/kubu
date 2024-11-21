#!/bin/bash

env TESTGO_VERSION=go1.500
env TESTGO_VERSION_SWITCH=switch

# GOTOOLCHAIN=auto runs default toolchain without a go.mod or go.work
env GOTOOLCHAIN=auto
go version

# GOTOOLCHAIN=path runs default toolchain without a go.mod or go.work
env GOTOOLCHAIN=path
go version

# GOTOOLCHAIN=asdf is a syntax error
env GOTOOLCHAIN=asdf
! go version

# GOTOOLCHAIN=version is used directly.
env GOTOOLCHAIN=go1.600
go version

env GOTOOLCHAIN=go1.400
go version

# GOTOOLCHAIN=version+auto sets a minimum.
env GOTOOLCHAIN=go1.600+auto
go version

env GOTOOLCHAIN=go1.400.0+auto
go version

# GOTOOLCHAIN=version+path sets a minimum too.
env GOTOOLCHAIN=go1.600+path
go version

env GOTOOLCHAIN=go1.400+path
go version

# Create a go.mod file and test interactions with auto and path.
env GOTOOLCHAIN=auto
go mod init m
go mod edit -go=1.700 -toolchain=none
go version

go mod edit -go=1.300 -toolchain=none
go version

go mod edit -go=1.700 -toolchain=go1.300
go version

go mod edit -go=1.300 -toolchain=default
go version

go mod edit -go=1.700 -toolchain=default
go version
! go build

# GOTOOLCHAIN=path does the same.
env GOTOOLCHAIN=path
go mod edit -go=1.700 -toolchain=none
go version

go mod edit -go=1.300 -toolchain=none
go version

go mod edit -go=1.700 -toolchain=go1.300
go version

go mod edit -go=1.300 -toolchain=default
go version

go mod edit -go=1.700 -toolchain=default
go version
! go build

# GOTOOLCHAIN=min+auto with toolchain default uses min, not local
env GOTOOLCHAIN=go1.400+auto
go mod edit -go=1.300 -toolchain=default
go version

env GOTOOLCHAIN=go1.600+auto
go mod edit -go=1.300 -toolchain=default
go version

# GOTOOLCHAIN names can have -suffix
env GOTOOLCHAIN=go1.800-bigcorp
go version

env GOTOOLCHAIN=auto
go mod edit -go=1.999 -toolchain=go1.800-bigcorp
go version

go mod edit -go=1.777 -toolchain=go1.800-bigcorp
go version

# go.work takes priority over go.mod
go mod edit -go=1.700 -toolchain=go1.999-wrong
go work init
go work edit -go=1.400 -toolchain=go1.600-right
go version

go work edit -go=1.400 -toolchain=default
go version

# go.work misconfiguration does not break go work edit
env OLD_GOCACHE=$GOCACHE
env GOCACHE=$WORK/cache  # use a fresh cache so that multiple runs of the test don't interfere
go build -x -overlay overlay.json ./test_cache
stderr '(compile|gccgo)( |\.exe).*test_cache.go'
go build -x -overlay overlay.json ./test_cache
! stderr '(compile|gccgo)( |\.exe).*test_cache.go'  # cached
cp overlay/test_cache_different.go overlay/test_cache.go
go build -x -overlay overlay.json ./test_cache
stderr '(compile|gccgo)( |\.exe).*test_cache.go'  # not cached
env GOCACHE=$OLD_GOCACHE

# Run same tests but with gccgo.
env GO111MODULE=off
[!exec:gccgo] stop
[cross] stop  # gccgo can't necessarily cross-compile

! go build -compiler=gccgo .
go build -compiler=gccgo -overlay overlay.json -o main_gccgo$GOEXE .
exec ./main_gccgo$GOEXE
stdout '^hello$'

go build -compiler=gccgo -overlay overlay.json -o print_abspath_gccgo$GOEXE ./printpath
exec ./print_abspath_gccgo$GOEXE
stdout $WORK[/\\]gopath[/\\]src[/\\]m[/\\]printpath[/\\]main.go

go build -compiler=gccgo -overlay overlay.json -o print_trimpath_gccgo$GOEXE -trimpath ./printpath
exec ./print_trimpath_gccgo$GOEXE
stdout ^\.[/\\]printpath[/\\]main.go

go build -compiler=gccgo  -overlay overlay.json -o main_cgo_replace_gccgo$GOEXE ./cgo_hello_replace
exec ./main_cgo_replace_gccgo$GOEXE
stdout '^hello cgo\r?\n'

go build -compiler=gccgo  -overlay overlay.json -o main_cgo_quote_gccgo$GOEXE ./cgo_hello_quote
exec ./main_cgo_quote_gccgo$GOEXE
stdout '^hello cgo\r?\n'

go build -compiler=gccgo  -overlay overlay.json -o main_cgo_angle_gccgo$GOEXE ./cgo_hello_angle
exec ./main_cgo_angle_gccgo$GOEXE
stdout '^hello cgo\r?\n'

go build -compiler=gccgo -overlay overlay.json -o main_call_asm_gccgo$GOEXE ./call_asm
exec ./main_call_asm_gccgo$GOEXE
! stdout .
