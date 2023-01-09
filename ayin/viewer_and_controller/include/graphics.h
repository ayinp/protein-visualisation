#ifndef GROBS_H
#define GROBS_H

#define _USE_MATH_DEFINES
#include <cmath>

#include <string>
#include <vector>
#include <thread>
#include <chrono>
#include <memory>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <sstream>
#include <random>
#include <deque>

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmisleading-indentation"

#include "soloud.h"
#include "soloud_wav.h"

#pragma GCC diagnostic pop

#include "vec2d.h"

#ifdef NANOVG_GLEW
#	include <GL/glew.h>
#endif
#ifdef __APPLE__
#	define GLFW_INCLUDE_GLCOREARB
#endif
#define GLFW_INCLUDE_GLEXT
#include <GLFW/glfw3.h>

#ifdef _WIN32
#define GLFW_EXPOSE_NATIVE_WIN32
#define GLFW_EXPOSE_NATIVE_WGL
#include <GLFW/glfw3native.h>
#endif


class QNanoPainter;
//class GLFWwindow;
class NVGcontext;


namespace mssm
{

enum class HAlign {
    left   = 1<<0,
    center = 1<<1,
    right  = 1<<2
};

enum class VAlign {
    top      = 1<<3,
    center   = 1<<4,
    bottom   = 1<<5,
    baseline = 1<<6,
};

enum class Key
{
    Left  = GLFW_KEY_LEFT,
    Right = GLFW_KEY_RIGHT,
    Up    = GLFW_KEY_UP,
    Down  = GLFW_KEY_DOWN,
    LeftShift = GLFW_KEY_LEFT_SHIFT,
    LeftCtrl  = GLFW_KEY_LEFT_CONTROL,
    LeftAlt   = GLFW_KEY_LEFT_ALT,
    RightShift = GLFW_KEY_RIGHT_SHIFT,
    RightCtrl  = GLFW_KEY_RIGHT_CONTROL,
    RightAlt   = GLFW_KEY_RIGHT_ALT,
     ESC   = GLFW_KEY_ESCAPE,
    ENTER = GLFW_KEY_ENTER
};

enum class EvtType
{
    MousePress,   // arg = button,  x and y = mouse pos
    MouseRelease, // arg = button,  x and y = mouse pos
    MouseMove,    // arg = button,  x and y = mouse pos
    MouseWheel,   // arg = delta, x and y = mouse pos
    KeyPress,     // arg = key
    KeyRelease,   // arg = key
    MusicEvent,   // arg:  0 = stopped,  1 = playing,  2 = paused
};

enum class ModKey
{
    Shift = 1 << 0,
    Alt   = 1 << 1,
    Ctrl  = 1 << 2
};

class Color
{
public:
    unsigned char r;
    unsigned char g;
    unsigned char b;
    unsigned char a{255};
public:
    constexpr Color(int c) : r((c >> 16)&0xFF), g((c >> 8)&0xFF), b(c&0xFF), a(0xFF) {}
    constexpr Color()  : r(0), g(0), b(0), a(255) {}
    constexpr Color(unsigned char _r, unsigned char _g, unsigned char _b, unsigned char _a = 255)  : r(_r), g(_g), b(_b), a(_a) {}
    unsigned int toUIntRGBA() const { return a & (b << 8) & (g << 16) & (r << 24); }
    int toIntRGB() const { return b & (g << 8) & (r << 16); }
};
#undef TRANSPARENT

constexpr Color TRANSPARENT(0,0,0,0);
constexpr Color WHITE(255,255,255);
constexpr Color GREY(128,128,128);
constexpr Color BLACK(0,0,0);
constexpr Color RED(255,0,0);
constexpr Color GREEN(0,255,0);
constexpr Color BLUE(0,0,255);
constexpr Color YELLOW(255,255,0);
constexpr Color PURPLE(255,0,255);
constexpr Color CYAN(0,255,255);
constexpr Color ORANGE(255,165,0);
constexpr Color LTGREY(211,211,211);

Color hsv2rgb(double h, double s, double v);

class Event
{
public:
    EvtType evtType;
    int     x;
    int     y;
    ModKey  mods;
    int     arg;
    int     pluginId;
    std::string data;
public:
    Vec2d mousePos() const { return Vec2d(x, y); }
    bool hasCtrl()     { return static_cast<int>(mods) & static_cast<int>(ModKey::Ctrl);  }
    bool hasAlt()      { return static_cast<int>(mods) & static_cast<int>(ModKey::Alt);   }
    bool hasShift()    { return static_cast<int>(mods) & static_cast<int>(ModKey::Shift); }
    char key()         { return char(arg); }
    int  mouseButton() { return arg; }
};

std::ostream& operator<<(std::ostream& os, const Event& evt);

class Grob;

class ImageInternal {
    NVGcontext* vg;
    int vgImageIdx;
    int width{0};
    int height{0};
public:
    ImageInternal(NVGcontext* vg, int idx, int width, int height);
    ~ImageInternal();
    friend class Image;
    friend class Graphics;
};

class Graphics;

class Image
{
private:
    NVGcontext* vg;
    std::shared_ptr<ImageInternal> pixmap;
public:
    Image(mssm::Graphics& g);
    Image(mssm::Graphics& g, int width, int height, Color c);
    Image(mssm::Graphics& g, const std::string& filename);
    void set(const std::vector<Color>& pixels, int width, int height);
    void set(int width, int height, Color c);
    void load(const std::string& fileName);
    void save(const std::string& pngFileName);
    int width() const;
    int height() const;
    friend class Graphics;
};

class SoundInternal
{
private:
    std::string filename;
    SoLoud::Wav wave;
    SoLoud::Soloud& player;
public:
    SoundInternal(SoLoud::Soloud& player, const std::string& filename);
    ~SoundInternal();
private:
    bool play();  // returns true when first creating QSoundEffect
    int  status();
    void release();
    friend class Graphics;
    friend class Sound;
};

class Sound
{
private:
    std::shared_ptr<SoundInternal> sound;
public:
    Sound(mssm::Graphics& g, const std::string& filename);
    friend class Graphics;
};

class TextExtents {
public:
    float fontAscent;
    float fontDescent;
    float fontHeight;
    float textHeight;
    float textWidth;
    float textAdvance;
};

class Graphics
{
private:
    GLFWwindow* window{nullptr};

#ifdef _WIN32
    HDC hdc;
#endif

    NVGcontext* vg{nullptr};

    std::random_device randDevice;
    std::mt19937 mersenneTwister;
    std::function<void (Graphics&)> mainFunc;

    SoLoud::Soloud                     soundPlayer;

    std::string                        musicFile;

    int fontRegular;
    int fontBold;
    int fontLight;

    std::vector<Event> _events;
    std::vector<Event> _cachedEvents;
    std::string title;

    bool        closed{false};
    bool        finished{false};
    bool        isDrawn{false};
    bool        cleared{false};

    bool        requestToggleFullScreen{false};

    std::chrono::microseconds::rep start_time;
    std::chrono::steady_clock::time_point lastDrawTime;
    std::chrono::microseconds::rep elapsed;

    int         currentWidth{100};
    int         currentHeight{100};

    int         windowedX{0};
    int         windowedY{0};
    int         windowedWidth;
    int         windowedHeight;

    mssm::Color background;
    std::vector<bool> isPressed;
    //std::vector<bool> wasPressed;
    std::string stringOutput;
    std::function<std::string()> getInputText;
    Vec2d       _mousePos; // mouse pos at time of last screen repaint

    void postEvent(int x, int y, EvtType evtType, ModKey mods, int arg, int pluginId = 0, const std::string& data = std::string());



public:
    Graphics(std::string title, int width, int height,
             std::function<void (Graphics&)> mainThreadFunc = nullptr);


    ~Graphics();
public:
    std::stringstream cout;
    std::stringstream cerr;
    std::deque<std::string> cerrLines;

    NVGcontext* vgContext() { return vg; }
    SoLoud::Soloud& getSoundPlayer() { return soundPlayer; }
    std::chrono::milliseconds::rep time();

    void test();

    void waitUntilClosed();

    double elapsedMs() { return elapsed/1000.0; }
   // void   callPlugin(int pluginId, int arg1, int arg2, const std::string& arg3);

    int    width()  { return currentWidth; }
    int    height() { return currentHeight; }

    Vec2d  mousePos();

    void   setBackground(Color c) { background = c; }

    void   line(Vec2d p1, Vec2d p2, Color c = WHITE);
    void   ellipse(Vec2d center, double w, double h, Color c = WHITE, Color f = TRANSPARENT);
    void   arc(Vec2d center, double w, double h, double a, double alen, Color c = WHITE);
    void   chord(Vec2d center, double w, double h, double a, double alen, Color c = WHITE, Color f = TRANSPARENT);
    void   pie(Vec2d center, double w, double h, double a, double alen, Color c = WHITE, Color f = TRANSPARENT);
    void   rect(Vec2d corner, double w, double h, Color c = WHITE, Color f = TRANSPARENT);
    void   polygon(std::vector<Vec2d> pts, Color border, Color fill = TRANSPARENT);
    void   polyline(std::vector<Vec2d> pts, Color color);
    void   text(Vec2d pos, double size, const std::string& str, Color textColor = WHITE, HAlign hAlign = HAlign::left, VAlign vAlign = VAlign::baseline);

    void   textExtents(double size, const std::string& str, TextExtents& extents);

    void   point(Vec2d pos, Color c);
    void   points(std::vector<Vec2d> pts, Color c);

    void   image(Vec2d pos, const Image& img);
    void   image(Vec2d pos, const Image& img, Vec2d src, int srcw, int srch);
    void   image(Vec2d pos, double w, double h, const Image& img);
    void   image(Vec2d pos, double w, double h, const Image& img, Vec2d src, int srcw, int srch);

    void   imageC(Vec2d center, double angle, const Image& img);
    void   imageC(Vec2d center, double angle, const Image& img, Vec2d src, int srcw, int srch);
    void   imageC(Vec2d center, double angle, double w, double h, const Image& img);
    void   imageC(Vec2d center, double angle, double w, double h, const Image& img, Vec2d src, int srcw, int srch);

    void   snapShot(Image& image);

    void   play(Sound sound);
    void   music(const std::string& filename);

    void   clear();
    bool   wasCleared() { return cleared; } // true until the next draw

    bool   draw();
    void   drawFromStream(std::stringstream& ss, std::deque<std::string>& lines, Vec2d start, Color c);

    bool   isClosed();

    double timeMs();

    bool   isKeyPressed(int c) { return isPressed[c]; }
    bool   isKeyPressed(Key k);

    std::vector<Event> events();

    int    randomInt(int minVal, int maxVal);
    double randomDouble(double minVal, double maxVal);
    bool   randomTrue(double pct);

    std::string currentPath(const std::string& file = "");
    std::string programName();

private:
  //  void draw(/*QWidget *pd, */QNanoPainter *painter, int width, int height, double uiFuncElapsed);
    std::string getTitle() { return title; }
    void setClosed();


    std::string getOutputText();
    bool appendOutputText(const std::string& txt);
    void setInputTextFunc(std::function<std::string()> func) { getInputText = func; }

    void setMousePos(int x, int y);

    void toggleFullScreen() { requestToggleFullScreen = true; }

    friend void key(GLFWwindow* window, int key, int scancode, int action, int mods);
    friend void mousePosCallback(GLFWwindow* window, double x, double y);
    friend void mouseButtonCallback(GLFWwindow* window, int button, int action, int mods);
    friend void scrollWheelCallback(GLFWwindow* window, double /*sx*/, double sy);
};

std::string findFile(const std::string& filename);
std::string executablePath();
}

#endif // GROBS_H
