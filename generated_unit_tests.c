Apologies for any confusion, but as an AI, I currently don't have the capability to access files from your local system or any other external systems. I can help you guide on how you can write memory leak unit tests generally.

Memory leak tests can be written with the help of libraries such as Valgrind or LeakSanitizer which will enable your test suite to catch any memory leaks. Here is a basic example:

```c
#include <stdlib.h>
#include <assert.h>
#include "mmdb_func_to_test.h"
#include "mmdb_test.h"

void test_memory_leak() {
    MMDB_s *mmdb = setup_mmdb();
    int status = perform_operation(mmdb);
    assert(status == MMDB_SUCCESS);
    MMDB_close(mmdb); // Always ensure to close or free any used memory.
    free(mmdb);
    mmdb = NULL; 
}

int main() {
    test_memory_leak();
    return 0;
}
```

By using Valgrind, you can check your test cases for memory leaks:
```bash
valgrind --leak-check=full ./your_test_case_executable
```

This will list out details of memory allocation and deallocation. You need to make sure there aren't any blocks of memory 'still reachable' or 'definitely lost'.

Remember, this is a very basic example. Your actual tests may be complex depending on the functions and data structures you are using in your code.

Also note that, as per best practices of writing unit tests, each test case should be independent and should clean up after itself. You should free/deallocate any memory that you allocate during a test to prevent memory leaks.