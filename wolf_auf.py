import os
import shutil
import urllib.request
import zipfile
from threading import Thread

# Принудительно задаем горизонтальное окно ДО импорта Kivy
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.image import Image as CoreImage
from kivy.utils import platform

# Ссылка на твой архив со сборкой в интернете (Гитхаб сам выдаст её позже)
MODS_URL = "https://githubusercontent.com"

class WolfAufApp(App):
    def build(self):
        self.root_layout = FloatLayout()
        
        # 1. Загружаем твой горизонтальный фон
        if os.path.exists('background.png'):
            bg = Image(source='background.png', allow_stretch=True, keep_ratio=False)
            self.root_layout.add_widget(bg)
            
        # 2. КНОПКА-КРИПЕР (16х16) В ПРАВОМ ВЕРХНЕМ УГЛУ
        btn_folder = Button(
            size_hint=(None, None),
            size=(70, 70),
            pos_hint={'right': 0.97, 'top': 0.95},
            border=(0, 0, 0, 0)
        )
        
        if os.path.exists('btn_folder.png'):
            core_img = CoreImage('btn_folder.png')
            core_img.texture.min_filter = 'nearest'
            core_img.texture.mag_filter = 'nearest'
            btn_folder.background_normal = 'btn_folder.png'
            btn_folder.background_down = 'btn_folder.png'
            
        btn_folder.bind(on_press=self.open_storage_folder)
        self.root_layout.add_widget(btn_folder)
            
        # 3. КОНТЕЙНЕР ДЛЯ ИГРОВЫХ КНОПОК
        self.menu_layout = BoxLayout(
            orientation='vertical', 
            padding=10, 
            spacing=20,
            size_hint=(None, None),
            size=(450, 160), 
            pos_hint={'center_x': 0.5, 'center_y': 0.35} 
        )
        
        self.btn_fabric = self.create_custom_button('Запустить Fabric (1.20.1)', self.launch_fabric)
        self.menu_layout.add_widget(self.btn_fabric)
        
        self.btn_nazzy = self.create_custom_button('🔥 Debt Hunt 🔥', self.launch_nazzy)
        self.menu_layout.add_widget(self.btn_nazzy)
        
        self.root_layout.add_widget(self.menu_layout)
        return self.root_layout

    def create_custom_button(self, text, callback):
        btn = Button(
            text=text,
            font_size='18sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=65, 
            background_normal='btn_normal.png' if os.path.exists('btn_normal.png') else '',
            background_down='btn_pressed.png' if os.path.exists('btn_pressed.png') else '',
            border=(16, 16, 16, 16)
        )
        btn.bind(on_press=callback)
        return btn

    def get_profile_path(self, profile_name):
        if platform == 'android':
            from jnius import autoclass
            Environment = autoclass('android.os.Environment')
            base_path = os.path.join(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS).getAbsolutePath(), 'VLauncher', profile_name, '.minecraft')
        else:
            base_path = os.path.join(os.path.dirname(__file__), 'VLauncher_Storage', profile_name, '.minecraft')
        return base_path

    def download_and_extract_mods(self, version, profile):
        self.btn_nazzy.text = "📥 Скачивание сборки..."
        self.btn_fabric.disabled = True
        self.btn_nazzy.disabled = True
        
        target_dir = self.get_profile_path(profile)
        os.makedirs(target_dir, exist_ok=True)
        
        zip_path = os.path.join(target_dir, "mods.zip")
        
        try:
            # Скачиваем архив по воздуху напрямую в телефон Вики
            urllib.request.urlretrieve(MODS_URL, zip_path)
            self.btn_nazzy.text = "📦 Распаковка файлов..."
            
            # Автоматически распаковываем
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
                
            os.remove(zip_path) # Удаляем временный архив за собой
            self.btn_nazzy.text = "🔥 Debt Hunt 🔥"
            self.btn_fabric.disabled = False
            self.btn_nazzy.disabled = False
            
            # Запускаем Пожав после успешного скачивания
            self.run_pojav(version, profile)
        except Exception as e:
            self.btn_nazzy.text = "❌ Ошибка загрузки!"
            self.btn_fabric.disabled = False
            self.btn_nazzy.disabled = False

    def check_and_launch(self, version, profile):
        target_dir = self.get_profile_path(profile)
        # Если папка пустая — автоматически качаем сборку из интернета
        if not os.path.exists(target_dir) or len(os.listdir(target_dir)) <= 1:
            Thread(target=self.download_and_extract_mods, args=(version, profile)).start()
        else:
            self.run_pojav(version, profile)

    def open_storage_folder(self, instance):
        if platform == 'android':
            from jnius import autoclass
            Environment = autoclass('android.os.Environment')
            target_path = os.path.join(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS).getAbsolutePath(), 'VLauncher')
        else:
            target_path = os.path.join(os.path.dirname(__file__), 'VLauncher_Storage')

        os.makedirs(target_path, exist_ok=True)
        
        if platform == 'android':
            from jnius import autoclass, cast
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            currentActivity = PythonActivity.mActivity

            intent = Intent(Intent.ACTION_GET_CONTENT)
            uri = Uri.parse(target_path)
            intent.setDataAndType(uri, "*/*")
            
            chooser = Intent.createChooser(intent, cast("java.lang.CharSequence", autoclass("java.lang.String")("Открыть VLauncher")))
            currentActivity.startActivity(chooser)
        else:
            os.startfile(target_path)

    def launch_fabric(self, instance):
        self.check_and_launch(version="1.20.1", profile="FabricMods")

    def launch_nazzy(self, instance):
        self.check_and_launch(version="1.12.2", profile="DebtHunt")

    def run_pojav(self, version, profile):
        game_dir = self.get_profile_path(profile)
        if platform == 'android':
            os.system(f"am start -n net.kdt.pojavlaunch/.MainActivity --es version {version} --es profile {profile} --es gameDir {game_dir}")

if __name__ == '__main__':
    WolfAufApp().run()
