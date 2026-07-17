[app]
title = VLauncher
package.name = vlauncher
package.domain = org.wolf
source.dir = .
source.include_exts = py,png,jpg
version = 0.1
requirements = python3, kivy, pyjnius, requests
orientation = landscape
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.api = 33
android.minapi = 24
android.ndk_api = 24
android.private_storage = False

[buildozer]
log_level = 2
warn_on_root = 0
