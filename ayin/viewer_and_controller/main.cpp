#include <iostream>
#include "graphics.h"

using namespace std;
using namespace mssm;

#pragma GCC diagnostic ignored "-Wsign-compare"

int main()
{
    Graphics g("Test", 1024, 768);

    while (g.draw()) {

        Vec2d p1{50,75};
        Vec2d p2{33,153};

        g.line(p1, p2, ORANGE);

        g.line({10,10}, {100,200}, GREEN);
        g.text({200,200}, 20, "Hello");

        if (g.isKeyPressed(Key::ESC)) {
            break;
        }

        if (g.isKeyPressed(Key::Left)) {
            // g.cout << "Left Key Down" << endl;

        }

        for (const Event& e : g.events()) {
           //  g.cerr << e << endl;

            switch (e.evtType) {
            case EvtType::KeyPress:
                break;
            case EvtType::KeyRelease:
                break;
            case EvtType::MouseMove:
                break;
            case EvtType::MousePress:
                break;
            case EvtType::MouseRelease:
                break;
            default:
                break;
            }
        }
    }

    return 0;
}


