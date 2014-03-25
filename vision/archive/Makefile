CC=g++
LIBS=-lopencv_core -lopencv_highgui -lopencv_imgproc

ahr_vision: ahr_vision.o
	$(CC) -o ahr_vision ahr_vision.o $(LIBS)

clean:
	rm -f *.o ahr_vision
