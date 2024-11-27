# Variables
CC=g++
CFLAGS=-Wall
DEPS = myheader.h
OBJ = main.o myfile.o anotherfile.o

# Target
myprogram: $(OBJ)
    $(CC) -o $@ $^ $(CFLAGS)

# Compile
%.o: %.cpp $(DEPS)
    $(CC) -c -o $@ $< $(CFLAGS)

# Clean
clean:
    rm -f *.o myprogram
