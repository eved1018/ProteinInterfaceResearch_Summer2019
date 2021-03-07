CC = g++

all: star clean

star: star.o
	${CC} star.o -o star -lgsl -lgslcblas -lm

star.o: star.cpp star.h
	${CC} -c star.cpp -o star.o

clean:
	\rm *.o

