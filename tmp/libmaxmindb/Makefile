CXX=g++
CXXFLAGS=-Wall -Werror -g
TARGET=memory_leak_unit_test

SRCDIR=/home/soumya/Automation/git_repos/libmaxminddb
TESTS=$(SRCDIR)/$(TARGET).c

all: build test clean

build: 
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(TESTS)

test: 
	valgrind --leak-check=full ./$(TARGET) 

clean:
	rm -f $(TARGET) 

.PHONY: all build test clean