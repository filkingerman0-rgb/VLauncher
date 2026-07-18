package org.wolf.volkaufengine;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.view.WindowManager;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;
import java.util.ArrayList;

public class VolkAufEngineActivity extends Activity {
    
    private VolkAufEngine engineCore;
    private ImageView splashView;
    private Spinner buildSelector;
    private Button btnLoadJar, btnLoadZip, btnMainPlay;
    private ImageButton btnFolderCriper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);

        // Показываем твоего сплющенного волка «Ауф Engine» из ресурсов drawable
        splashView = new ImageView(this);
        int imageId = getResources().getIdentifier("volk_auf", "drawable", getPackageName());
        splashView.setImageResource(imageId);
        splashView.setScaleType(ImageView.ScaleType.CENTER_CROP);
        setContentView(splashView);

        // Задержка 1.5 секунды, любуемся волком и включаем главное меню
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                initMainLauncherMenu();
            }
        }, 1500);
    }

    private void initMainLauncherMenu() {
        setContentView(getResources().getIdentifier("activity_main", "layout", getPackageName()));

        btnLoadJar = findViewById(getResources().getIdentifier("btn_load_jar", "id", getPackageName()));
        btnLoadZip = findViewById(getResources().getIdentifier("btn_load_zip", "id", getPackageName()));
        btnMainPlay = findViewById(getResources().getIdentifier("btn_main_play", "id", getPackageName()));
        btnFolderCriper = findViewById(getResources().getIdentifier("btn_folder_criper", "id", getPackageName()));
        buildSelector = findViewById(getResources().getIdentifier("build_selector", "id", getPackageName()));

        ArrayList<String> builds = new ArrayList<>();
        builds.add("Ванилла (1.20.1)");
        builds.add("DebtHunt (Сборка Nazzy)");
        builds.add("FabricMods");

        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, builds);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        buildSelector.setAdapter(adapter);

        String gameDir = getFilesDir().getAbsolutePath() + "/VLauncher";
        engineCore = new VolkAufEngine(gameDir, "1.20.1");
        engineCore.bootEngine();

        btnMainPlay.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String selected = buildSelector.getSelectedItem().toString();
                Toast.makeText(VolkAufEngineActivity.this, "VolkAufEngine: Запуск " + selected, Toast.LENGTH_SHORT).show();
                engineCore.launchVanilla1201("Vika");
            }
        });

        btnFolderCriper.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.setType("*/*");
                startActivity(intent);
            }
        });
    }
}
