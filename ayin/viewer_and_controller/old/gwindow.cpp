#include "gwindow.h"
#include "graphics.h"

#include <iostream>

#include <QPainter>
#include <QOpenGLPaintDevice>
#include <QTimer>
#include <QSoundEffect>
#include <QThread>

static QString vertexShader =
        //"#version 330\n"
        "\n"
        "attribute highp vec2 position;\n" // just take 2d data for now
        "attribute mediump vec3 color;\n"      // don't use per-vertex color
        "\n"
        "uniform mediump mat4 mvp;\n"
        "\n"
        "varying mediump vec3 v_color;\n"
        "\n"
        "void main()\n"
        "{\n"
        "    v_color = color;\n"
        "    gl_Position = mvp * vec4(position.x, position.y, 0, 1);\n"
        "}\n"
        ;
static QString fragmentShader =
       // "#version 330\n"
        "\n"
        "varying vec3 v_color;\n"
        "\n"
        "void main()\n"
        "{\n"
        "    gl_FragColor = vec4(v_color, 1);\n"
        "}\n"
        ;

struct Vertex {
    GLfloat position[2],
    color[3];
};

void GWindow::appendOutputText(std::string txt)
{
    std::cout << txt << std::endl;
}

GWindow::GWindow(mssm::Graphics& g, std::string title) :
    m_vbo(QOpenGLBuffer::VertexBuffer), g{g}
{
    setTitle(tr(title.c_str()));
    setWidth(g.width());
    setHeight(g.height());

    QSurfaceFormat format;
//    format.setDepthBufferSize(24);
//    format.setStencilBufferSize(8);
    format.setSwapInterval(1);
    setFormat(format);

    std::cout << "GWindow Created: " << QThread::currentThreadId() << std::endl;
}

GWindow::~GWindow()
{
    makeCurrent();

    /*
     * From Qt Documentation
     * Warning: if you have objects wrapping OpenGL resources
     * (such as QOpenGLBuffer, QOpenGLShaderProgram, etc.) as
     *  members of a QOpenGLWindow subclass, you may need to
     * add a call to makeCurrent() in that subclass' destructor as well. .
     */

    std::cout << "GWindow Destroyed: " << QThread::currentThreadId() << std::endl;

}

void GWindow::createShaderProgram()
{
    QOpenGLShader *vshader = new QOpenGLShader(QOpenGLShader::Vertex, this);

    vshader->compileSourceCode(vertexShader);

    QOpenGLShader *fshader = new QOpenGLShader(QOpenGLShader::Fragment, this);

    fshader->compileSourceCode(fragmentShader);

    if ( !m_pgm.addShader(vshader)) {
        qDebug() << "Error in vertex shader:" << m_pgm.log();
        exit(1);
    }
    if ( !m_pgm.addShader(fshader)) {
        qDebug() << "Error in fragment shader:" << m_pgm.log();
        exit(1);
    }
    if ( !m_pgm.link() ) {
        qDebug() << "Error linking shader program:" << m_pgm.log();
        exit(1);
    }
}

void GWindow::createGeometry()
{
    // Initialize and bind the VAO that's going to capture all this vertex state
    m_vao.create();
    m_vao.bind();

    // Put all the attribute data in a FBO
    m_vbo.create();
    m_vbo.setUsagePattern( QOpenGLBuffer::StaticDraw );
    m_vbo.bind();
    // Configure the vertex streams for this attribute data layout
    m_pgm.enableAttributeArray("position");
    m_pgm.setAttributeBuffer("position", GL_FLOAT, offsetof(Vertex, position), 3, sizeof(Vertex) );
    m_pgm.enableAttributeArray("color");
    m_pgm.setAttributeBuffer("color",  GL_FLOAT, offsetof(Vertex, color), 3, sizeof(Vertex) );
    // Okay, we've finished setting up the vao
    m_vao.release();
}

void GWindow::initializeGL()
{
    initializeOpenGLFunctions();

    createShaderProgram();
    m_pgm.bind();
    createGeometry();
    m_view.setToIdentity();
    connect(this, SIGNAL(frameSwapped()), this, SLOT(onFrameSwapped()));
}

void GWindow::resizeGL(int w, int h)
{
    width = w;
    height = h;

    glViewport(0, 0, w, h);
    m_model.setToIdentity();
    m_projection.setToIdentity();
    if (w <= h) {
        m_model.scale(1, float(h)/w, 1);
        m_projection.ortho(-2.f, 2.f, -2.f*h/w, 2.f*h/w, -2.f, 2.f);
    } else {
        m_model.scale(float(w)/h, 1, 1);
        m_projection.ortho(-2.f*w/h, 2.f*w/h, -2.f, 2.f, -2.f, 2.f);
    }
    //   update();
    forceDraw = true;
}

void GWindow::paintGL()
{


    // std::cout << "paintGL()" << std::endl;
    if (g.checkAndClearReadyToDraw() || forceDraw)
    {

        forceDraw = false;
        askedToDraw = true;

       // std::cout << "  Drawing" << std::endl;

        QPainter p;

        p.begin(this);

        p.beginNativePainting();

        mssm::Color bg = g.background;

        glClearColor(bg.toFloatR(), bg.toFloatG(), bg.toFloatB(), 1.0f);

        glClear(GL_COLOR_BUFFER_BIT);
        m_pgm.bind();
        m_pgm.setUniformValue("mvp", m_projection * m_view * m_model);
        m_vao.bind();

        // interleaved data -- https://www.opengl.org/wiki/Vertex_Specification#Interleaved_arrays
        static float x = 0;

        Vertex attribs[3] = {
            { {   -2.0, -2.0,  }, { 1.0, 0.0, 0.0 } },  // left-bottom,  red
            { {    GLfloat(x/10.0f),  2.0, }, { 0.0, 1.0, 0.0 } },  // center-top,   blue
            { {    2.0, -2.0,  }, { 0.0, 0.0, 1.0 } },  // right-bottom, green
        };
        // x += 1;

        m_vbo.bind();
        m_vbo.allocate(attribs, sizeof(attribs));

        //glDrawArrays(GL_TRIANGLES, 0, 3);


        m_vbo.release();
        m_vao.release();
        m_pgm.release();

        p.endNativePainting();

        p.setPen(Qt::white);
//        p.drawText(20,20,QString::fromStdString(std::to_string(paintCount++)));

        g.draw(&p, width, height);

        p.end();
    }
    else {
        //std::cout << "  Nothing to draw" << std::endl;
        g.updateWithoutDraw();
    }

    auto cursorPos = mapFromGlobal(QCursor::pos());
    g.setMousePos(cursorPos.x(), cursorPos.y());

//    if (et > 17) {
//        std::cout << et << std::endl;
//    }
}

void GWindow::onFrameSwapped()
{
 //   std::cout << "  Frame Swapped" << std::endl;
    g.onDrawFinished(askedToDraw); // when frame is finished, signal Graphics to release the blocked Draw() method
    if (askedToDraw) {
        askedToDraw = false;
        update();
    }
}


void GWindow::musicStateChanged(QMediaPlayer::State)
{

}


ModKey cvtMods(Qt::KeyboardModifiers qmods);

void GWindow::wheelEvent(QWheelEvent *event)
{
    g.handleEvent(event->x(), event->y(), EvtType::MouseWheel,
                  cvtMods(event->modifiers()),
                  event->angleDelta().y());
}

void GWindow::mousePressEvent(QMouseEvent * event)
{
    g.handleEvent(event->x(), event->y(), EvtType::MousePress,
                  cvtMods(event->modifiers()),
                  static_cast<int>(event->button()));
}

void GWindow::mouseReleaseEvent(QMouseEvent * event)
{
    g.handleEvent(event->x(), event->y(), EvtType::MouseRelease,
                  cvtMods(event->modifiers()),
                  static_cast<int>(event->button()));
}

void GWindow::mouseMoveEvent(QMouseEvent * event)
{
    g.handleEvent(event->x(), event->y(), EvtType::MouseMove,
                  cvtMods(event->modifiers()),
                  static_cast<int>(event->buttons()));
}

//void main_window::toggle_fullscreen()
//{
//    isFullScreen() ?
//        ((was_maximized_) ? showMaximized() : showNormal()), ui_->menu_view_toggle_fullscreen->setIcon(QIcon(":/fullscreen_enter")) :
//        ((was_maximized_ = isMaximized()), showFullScreen(), ui_->menu_view_toggle_fullscreen->setIcon(QIcon(":/fullscreen_exit")));
//}

void GWindow::keyPressEvent(QKeyEvent * event)
{
    if (event->key() == Qt::Key_Escape && (this->windowState() & Qt::WindowFullScreen)) {
        this->close();
    }

    g.handleEvent(0, 0, EvtType::KeyPress,
                  cvtMods(event->modifiers()),
                  event->key());
}

void GWindow::keyReleaseEvent(QKeyEvent * event)
{
    g.handleEvent(0,0, EvtType::KeyRelease,
                  cvtMods(event->modifiers()),
                  event->key());
}

