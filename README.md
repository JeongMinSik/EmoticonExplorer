## release build

buildozer init
buildozer android <debug/release>

## how to sing

my-project - The directory for your project
my-new-key - The name of the key you generate: emoticon-explorer-key
my-alias - A short alias name for the key: jms-key
MyProject - The name of your project, and APK: EmoticonExplorer
version - The version of this APK (not Kivy version) : 0.1
Commands

$ cd ~
$ keytool -genkey -v -keystore ./keystores/<my-new-key>.keystore -alias <my-alias> -keyalg RSA -keysize 2048 -validity 10000
$ cd ~/<my-project>
$ source venv/bin/activate
$ buildozer android release
$ jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore ~/keystores/<my-new-key>.keystore ./<file-name>.apk <my-alias>
$ zipalign -v 4 ./bin/<file-name>.apk ./<my-project>/bin/<MyProject>.apk