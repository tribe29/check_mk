rem clang-tidy.exe "C:\z\m\check_mk\agents\wnx\src\engine\cap.cpp" -checks=-*,abseil*,bugprone*,clang-analyzer*,modernize*,performance*,readability*,security*,-readability-braces-around-statements;-modernize-use-trailing-return-type -header-filter="./*.h" -quiet -- -isystem"C:\z\m\check_mk\agents\wnx\src\engine" -isystem"C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Tools\MSVC\14.24.28314\include" -isystem"C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Tools\MSVC\14.24.28314\atlmfc\include" -isystem"C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\VS\include" -isystem"C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\ucrt" -isystem"C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\um" -isystem"C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\shared" -isystem"C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\winrt" -isystem"C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\cppwinrt" -I"C:\z\m\check_mk\agents\wnx\src\engine" -I"C:\z\m\check_mk\agents\wnx\include" -I"C:\z\m\check_mk\agents\wnx\src" -I"C:\z\m\check_mk\agents\wnx\src\engine" -I"C:\z\m\check_mk\agents\wnx\extlibs\asio\include" -I"C:\z\m\check_mk\agents\wnx\extlibs\yaml-cpp\include" -I"C:\z\m\check_mk\agents\wnx\extlibs\fmt\include" -I"C:\z\m\check_mk\agents\wnx\extlibs\simpleini" -std=c++2a -Wall -fms-compatibility-version=19.10 -Wmicrosoft -Wno-invalid-token-paste -Wno-unknown-pragmas -Wno-unused-value "-DUNICODE" "-D_UNICODE" "-D_MT" 
clang-tidy.exe %1 -checks="-*,abseil*,bugprone*,clang-analyzer*,modernize*,performance*,readability*,security*,-readability-braces-around-statements,-modernize-use-trailing-return-type" -header-filter="./*.h" -quiet -- -isystem"C:\z\m\check_mk\agents\wnx\src\engine" -isystem"C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Tools\MSVC\14.24.28314\include" -isystem"C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Tools\MSVC\14.24.28314\atlmfc\include" -isystem"C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\VS\include" -isystem"C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\ucrt" -isystem"C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\um" -isystem"C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\shared" -isystem"C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\winrt" -isystem"C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\cppwinrt" -I"C:\z\m\check_mk\agents\wnx\src\engine" -I"C:\z\m\check_mk\agents\wnx\include" -I"C:\z\m\check_mk\agents\wnx\src" -I"C:\z\m\check_mk\agents\wnx\src\engine" -I"C:\z\m\check_mk\agents\wnx\extlibs\asio\include" -I"C:\z\m\check_mk\agents\wnx\extlibs\yaml-cpp\include" -I"C:\z\m\check_mk\agents\wnx\extlibs\fmt\include" -I"C:\z\m\check_mk\agents\wnx\extlibs\simpleini" -std=c++2a -Wall -fms-compatibility-version=19.10 -Wmicrosoft -Wno-invalid-token-paste -Wno-unknown-pragmas -Wno-unused-value "-DUNICODE" "-D_UNICODE" "-D_MT" 