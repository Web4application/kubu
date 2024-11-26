cd m

# Run basic build
go build .
go build -overlay overlay.json -o main$GOEXE .
./main$GOEXE

# Build and execute with overlay
go build -overlay overlay.json -o print_abspath$GOEXE ./printpath
./print_abspath$GOEXE

go build -overlay overlay.json -o print_trimpath$GOEXE -trimpath ./printpath
./print_trimpath$GOEXE

go build -overlay overlay.json -o print_trimpath_two_files$GOEXE printpath/main.go printpath/other.go
./print_trimpath_two_files$GOEXE

# Test with CGO
go build -overlay overlay.json -o main_cgo_replace$GOEXE ./cgo_hello_replace
./main_cgo_replace$GOEXE

go build -overlay overlay.json -o main_cgo_quote$GOEXE ./cgo_hello_quote
./main_cgo_quote$GOEXE

go build -overlay overlay.json -o main_cgo_angle$GOEXE ./cgo_hello_angle
./main_cgo_angle$GOEXE

# Test with assembler
go build -overlay overlay.json -o main_call_asm$GOEXE ./call_asm
./main_call_asm$GOEXE

# Compile list and verify paths
go list -compiled -overlay overlay.json -f '{{range .CompiledGoFiles}}{{. | printf "%s\n"}}{{end}}' ./cgo_hello_replace
cp stdout compiled_cgo_sources.txt
go run ../print_line_comments.go compiled_cgo_sources.txt
# Cache test
export OLD_GOCACHE=$GOCACHE
export GOCACHE=$WORK/cache  # Use a fresh cache
go build -x -overlay overlay.json ./test_cache
go build -x -overlay overlay.json ./test_cache
cp overlay/test_cache_different.go overlay/test_cache.go
go build -x -overlay overlay.json ./test_cache
export GOCACHE=$OLD_GOCACHE

# Run tests with gccgo
export GO111MODULE=off
! go build -compiler=gccgo .
go build -compiler=gccgo -overlay overlay.json -o main_gccgo$GOEXE .
./main_gccgo$GOEXE

go build -compiler=gccgo -overlay overlay.json -o print_abspath_gccgo$GOEXE ./printpath
./print_abspath_gccgo$GOEXE

go build -compiler=gccgo -overlay overlay.json -o print_trimpath_gccgo$GOEXE -trimpath ./printpath
./print_trimpath_gccgo$GOEXE

go build -compiler=gccgo -overlay overlay.json -o main_cgo_replace_gccgo$GOEXE ./cgo_hello_replace
./main_cgo_replace_gccgo$GOEXE

go build -compiler=gccgo -overlay overlay.json -o main_cgo_quote_gccgo$GOEXE ./cgo_hello_quote
./main_cgo_quote_gccgo$GOEXE

go build -compiler=gccgo -overlay overlay.json -o main_cgo_angle_gccgo$GOEXE ./cgo_hello_angle
./main_cgo_angle_gccgo$GOEXE

go build -compiler=gccgo -overlay overlay.json -o main_call_asm_gccgo$GOEXE ./call_asm
./main_call_asm_gccgo$GOEXE
