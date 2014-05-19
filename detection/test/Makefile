CC=g++
LIBS=-lopencv_core -lopencv_highgui -lopencv_imgproc

fps_test: fps_test.o
	$(CC) -o fps_test fps_test.o $(LIBS)

clean:
	rm -f *.o fps_test
