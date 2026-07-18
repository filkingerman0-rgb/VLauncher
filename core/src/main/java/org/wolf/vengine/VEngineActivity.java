package org.wolf.vengine;

import android.app.Activity;
import android.opengl.GLSurfaceView;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;

import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.opengles.GL10;

public class VEngineActivity extends Activity implements GLSurfaceView.Renderer {
    
    private GLSurfaceView glView;
    private VEngine engineCore;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Врубаем ультимативный полноэкранный режим под Samsung и Redmi
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        
        // Прячем системные кнопки Андроида, чтобы не мешались под пальцами
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);

        // Создаем холст для графики Mali
        glView = new GLSurfaceView(this);
        glView.setEGLContextClientVersion(3); // Включаем принудительно GLES3
        glView.setRenderer(this);
        
        setContentView(glView);

        // Инициализируем наше ядро
        String gameDir = getFilesDir().getAbsolutePath() + "/VLauncher/Vanilla";
        engineCore = new VEngine(gameDir, "1.20.1");
        engineCore.bootEngine();
    }

    @Override
    public void onSurfaceCreated(GL10 gl, EGLConfig config) {
        // Как только экран создался — передаем управление нашему отрисовщику!
        engineCore.setupMaliRenderer(glView.getWidth(), glView.getHeight());
    }

    @Override
    public void onSurfaceChanged(GL10 gl, int width, int height) {
        // Реагирует, если экран повернулся или изменился размер
    }

    @Override
    public void onDrawFrame(GL10 gl) {
        // В этом цикле MediaTek будет фигачить FPS и рисовать кубы Майнкрафта!
    }
}
