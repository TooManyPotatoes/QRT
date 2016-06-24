INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_WELCHMANAGER WelchManager)

FIND_PATH(
    WELCHMANAGER_INCLUDE_DIRS
    NAMES WelchManager/api.h
    HINTS $ENV{WELCHMANAGER_DIR}/include
        ${PC_WELCHMANAGER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    WELCHMANAGER_LIBRARIES
    NAMES gnuradio-WelchManager
    HINTS $ENV{WELCHMANAGER_DIR}/lib
        ${PC_WELCHMANAGER_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(WELCHMANAGER DEFAULT_MSG WELCHMANAGER_LIBRARIES WELCHMANAGER_INCLUDE_DIRS)
MARK_AS_ADVANCED(WELCHMANAGER_LIBRARIES WELCHMANAGER_INCLUDE_DIRS)
