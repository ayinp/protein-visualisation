TEMPLATE = app

CONFIG +=  c++20
#CONFIG -= app_bundle
CONFIG -= qt
CONFIG -= console

INCLUDEPATH += nanovg
INCLUDEPATH += include
INCLUDEPATH += soloud/include

DEFINES += WITH_MINIAUDIO

QMAKE_CXXFLAGS += -msse3

QMAKE_CFLAGS += \
-Wno-misleading-indentation \
-Wno-shift-negative-value \
-Wno-cast-function-type \
-Wno-implicit-fallthrough \
-Wno-unused-parameter \
-Wno-missing-field-initializers

QMAKE_CXXFLAGS += -isystem $$PWD/soloud/

SOURCES += \
        glfw_src/context.c \
        glfw_src/init.c \
        glfw_src/input.c \
        glfw_src/monitor.c \
        glfw_src/vulkan.c \
        glfw_src/window.c \
        main.cpp \
        nanovg/nanovg.c \
        soloud/src/audiosource/wav/dr_impl.cpp \
        soloud/src/audiosource/wav/soloud_wav.cpp \
        soloud/src/audiosource/wav/soloud_wavstream.cpp \
        soloud/src/audiosource/wav/stb_vorbis.c \
        soloud/src/backend/miniaudio/soloud_miniaudio.cpp \
        soloud/src/core/soloud.cpp \
        soloud/src/core/soloud_audiosource.cpp \
        soloud/src/core/soloud_bus.cpp \
        soloud/src/core/soloud_core_3d.cpp \
        soloud/src/core/soloud_core_basicops.cpp \
        soloud/src/core/soloud_core_faderops.cpp \
        soloud/src/core/soloud_core_filterops.cpp \
        soloud/src/core/soloud_core_getters.cpp \
        soloud/src/core/soloud_core_setters.cpp \
        soloud/src/core/soloud_core_voicegroup.cpp \
        soloud/src/core/soloud_core_voiceops.cpp \
        soloud/src/core/soloud_fader.cpp \
        soloud/src/core/soloud_fft.cpp \
        soloud/src/core/soloud_fft_lut.cpp \
        soloud/src/core/soloud_file.cpp \
        soloud/src/core/soloud_filter.cpp \
        soloud/src/core/soloud_misc.cpp \
        soloud/src/core/soloud_queue.cpp \
        soloud/src/core/soloud_thread.cpp \
        src/graphics.cpp \
        src/vec2d.cpp \
        src/whereami.c

macos {
    LIBS += -framework Cocoa -framework IOKit -framework OpenGL

    DEFINES += _GLFW_COCOA

    HEADERS += \
        glfw_src/cocoa_platform.h \
        glfw_src/cocoa_joystick.h \
        glfw_src/posix_thread.h   \
        glfw_src/nsgl_context.h   \
        glfw_src/egl_context.h    \
        glfw_src/osmesa_context.h

    SOURCES += \
        glfw_src/cocoa_init.m     \
        glfw_src/cocoa_joystick.m \
        glfw_src/cocoa_monitor.m  \
        glfw_src/cocoa_window.m   \
        glfw_src/cocoa_time.c     \
        glfw_src/posix_thread.c   \
        glfw_src/nsgl_context.m   \
        glfw_src/egl_context.c    \
        glfw_src/osmesa_context.c
}

windows {
    LIBS += -lopengl32 -lgdi32

    DEFINES += _GLFW_WIN32 NANOVG_GLEW GLEW_STATIC


    HEADERS += \
        glfw_src/win32_platform.h \
        glfw_src/win32_joystick.h \
        glfw_src/wgl_context.h    \
        glfw_src/egl_context.h    \
        glfw_src/osmesa_context.h \
        include/GL/eglew.h \
        include/GL/glxew.h \
        include/GL/wglew.h \
        include/GL/glew.h

    SOURCES += \
        glfw_src/win32_init.c     \
        glfw_src/win32_joystick.c \
        glfw_src/win32_monitor.c  \
        glfw_src/win32_time.c     \
        glfw_src/win32_thread.c   \
        glfw_src/win32_window.c   \
        glfw_src/wgl_context.c    \
        glfw_src/egl_context.c    \
        glfw_src/osmesa_context.c \
        src/glew.c
}

linux {
    DEFINES += _GLFW_X11

    HEADERS += \
        glfw_src/x11_platform.h   \
        glfw_src/xkb_unicode.h    \
        glfw_src/posix_time.h     \
        glfw_src/posix_thread.h   \
        glfw_src/glx_context.h    \
        glfw_src/egl_context.h    \
        glfw_src/osmesa_context.h

    SOURCES += \
        glfw_src/x11_init.c       \
        glfw_src/x11_monitor.c    \
        glfw_src/x11_window.c     \
        glfw_src/xkb_unicode.c    \
        glfw_src/posix_time.c     \
        glfw_src/posix_thread.c   \
        glfw_src/glx_context.c    \
        glfw_src/egl_context.c    \
        glfw_src/osmesa_context.c
}

HEADERS += \
    include/GLFW/glfw3.h \
    include/GLFW/glfw3native.h \
    include/ghc/filesystem.hpp \
    include/graphics.h \
    include/vec2d.h \
    include/whereami.h \
    nanovg/fontstash.h \
    nanovg/nanovg.h \
    nanovg/nanovg_gl.h \
    nanovg/nanovg_gl_utils.h \
    nanovg/stb_image.h \
    nanovg/stb_truetype.h \
    soloud/include/audiosource/wav/dr_flac.h \
    soloud/include/audiosource/wav/dr_mp3.h \
    soloud/include/audiosource/wav/dr_wav.h \
    soloud/include/audiosource/wav/stb_vorbis.h \
    soloud/include/backend/miniaudio/miniaudio.h \
    soloud/include/soloud.h \
    soloud/include/soloud_audiosource.h \
    soloud/include/soloud_bassboostfilter.h \
    soloud/include/soloud_biquadresonantfilter.h \
    soloud/include/soloud_bus.h \
    soloud/include/soloud_c.h \
    soloud/include/soloud_dcremovalfilter.h \
    soloud/include/soloud_echofilter.h \
    soloud/include/soloud_error.h \
    soloud/include/soloud_fader.h \
    soloud/include/soloud_fft.h \
    soloud/include/soloud_fftfilter.h \
    soloud/include/soloud_file.h \
    soloud/include/soloud_file_hack_off.h \
    soloud/include/soloud_file_hack_on.h \
    soloud/include/soloud_filter.h \
    soloud/include/soloud_flangerfilter.h \
    soloud/include/soloud_freeverbfilter.h \
    soloud/include/soloud_internal.h \
    soloud/include/soloud_lofifilter.h \
    soloud/include/soloud_misc.h \
    soloud/include/soloud_monotone.h \
    soloud/include/soloud_noise.h \
    soloud/include/soloud_openmpt.h \
    soloud/include/soloud_queue.h \
    soloud/include/soloud_robotizefilter.h \
    soloud/include/soloud_sfxr.h \
    soloud/include/soloud_speech.h \
    soloud/include/soloud_tedsid.h \
    soloud/include/soloud_thread.h \
    soloud/include/soloud_vic.h \
    soloud/include/soloud_vizsn.h \
    soloud/include/soloud_wav.h \
    soloud/include/soloud_waveshaperfilter.h \
    soloud/include/soloud_wavstream.h \
    soloud/src/audiosource/wav/dr_flac.h \
    soloud/src/audiosource/wav/dr_mp3.h \
    soloud/src/audiosource/wav/dr_wav.h \
    soloud/src/audiosource/wav/stb_vorbis.h \
    soloud/src/backend/miniaudio/miniaudio.h



ASSET_SOURCE_PATH = $$shell_path($$clean_path("$$PWD\\Data\\"))

windows {
    specified_configs=$$find(CONFIG, "\b(debug|release)\b")
    build_subdir=$$last(specified_configs)
    message($$specified_configs)
    ASSET_DESTINATION = $$shell_path($$clean_path("$$OUT_PWD\\$$build_subdir\\Data\\"))

    copydata.commands = $(COPY_DIR) \"$$ASSET_SOURCE_PATH\" \"$$ASSET_DESTINATION\"
    first.depends = $(first) copydata
    export(first.depends)
    export(copydata.commands)
    QMAKE_EXTRA_TARGETS += first copydata
}

macos {
    assetFiles.files = $$files($$ASSET_SOURCE_PATH/*)
    assetFiles.path = Contents\MacOs\Data
    QMAKE_BUNDLE_DATA += assetFiles
}
