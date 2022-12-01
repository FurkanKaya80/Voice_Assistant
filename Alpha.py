import time
import pyautogui  # klavye ve fare kontrolü sağlamak için
import requests as requests
from playsound import playsound  # ses dosyaları oynatma
from gtts import gTTS  # konuşan asistan
import speech_recognition as sr  # sesimizi anlama
import os  # Dosya işlemleri
from datetime import datetime  # Tarih işlemleri
import random  # rastgele işlemleri
from random import choice
import webbrowser  # internette bir şey aratmak için
import psutil  # uygulamaların açık olup olmadığını kontrol etme sistem bilgilerini de alıyor fln işte
import pywhatkit  # youtube şarkı açmak için wp flnda mesaj fln gönderiyor galiba pyautoguiye sahipmiş bir de önceden ekledik
import wikipedia  # wikipediadan bilgi çekme sadece ingilizceymiş
import requests  # web siteleri linklerine istek türkçe vikipedia denemem bunla soup
from bs4 import BeautifulSoup  # HTML dosyaları text çevirme
from deep_translator import GoogleTranslator  # Translate işlemleri için
import pyjokes  # şaka üretiyor
import screen_brightness_control as sbc #ekran parlaklığı için
########  PC ses ayarlama
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#########

r = sr.Recognizer()
######### Pycaw a ses aygıtını tanımlıyoruz
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
##########


def record(ask=False):  # Sesimizi algılamasını sağladığımız yer
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = r.listen(source)
        voice = ""
        try:
            voice = r.recognize_google(audio, language="tr-TR")
        except sr.UnknownValueError:
            print("Carmen: Anlayamadım")
        except sr.RequestError:
            print("Carmen: Sistem çalışmıyor")
        return voice


def response(voice):  # Konuşmamıza döndürdüğü cevaplar
    txtvoice = voice
    if txtvoice == 'merhaba':
        speak("sana da merhaba")
    elif txtvoice == 'selam':
        speak("selam")
    if txtvoice == 'teşekkürler' or txtvoice == 'teşekkür ederim':
        selection = ["Rica ederim", "Önemli değil"]
        selection = random.choice(selection)
        speak(selection)
    if txtvoice == "görüşürüz":
        speak("görüşürüz")
        exit()
    if txtvoice == 'hangi gündeyiz' or txtvoice == 'bugün günlerden ne':
        today = time.strftime("%A")
        today.capitalize()
        if today == "Monday":
            today = "Pazartesi"
        if today == "Tuesday":
            today = "Salı"
        if today == "Wednesday":
            today = "Çarşamba"
        if today == "Thursday":
            today = "Perşembe"
        if today == "Friday":
            today = "Cuma"
        if today == "Saturday":
            today = "Cumartesi"
        if today == "Sunday":
            today = "Pazar"
        speak(today)
    if txtvoice == 'saat kaç':
        speak(datetime.now().strftime("%H:%M"))
    if txtvoice.startswith("google'da ara") or txtvoice.endswith("google'da ara"):
        search = txtvoice.replace("google'da ara", "")
        url = "https://www.google.com/search?q={}".format(search)
        webbrowser.get().open(url)
        # speak("{} hakkında ki sonuçlar".format(search))
    if txtvoice.startswith('uygulama aç'):  # konuşarak uygulama açma işlemlerimiz
        runApp = record()
        runApp = runApp.lower()
        if 'lol' in voice:
            os.startfile("path of exe")
            time.sleep(15)
            if "RiotClientServices.exe" in (p.name() for p in psutil.process_iter()):
                time.sleep(5)
                pyautogui.typewrite("yourid", interval=0.25)
                pyautogui.press('tab')
                pyautogui.typewrite("password", interval=0.25)
                pyautogui.press('enter')
                time.sleep(10)
                pyautogui.click(x=350, y=520)
                time.sleep(3)
                pyautogui.click(x=350, y=900)

        else:
            speak("Böyle bir uygulama listemde yok")
    if txtvoice.startswith('oynat') or txtvoice.endswith('oynat'):
        song = txtvoice.replace('oynat', '')
        speak(song + "oynatılıyor")
        pywhatkit.playonyt(song)
    if txtvoice.startswith("wikipedia") or txtvoice.endswith(
            'wikipedia'):  # yabancı wikipediadan bilgi çekiyor tr çevirtiyom 1 ilk satırı alması için
        try:  # türkçe söylediğimizde hatasız buluyorsa bu
            soru = txtvoice.replace('wikipedia', '')
            print(soru)
            info = wikipedia.summary(soru, 1)
            infotr = GoogleTranslator(source='auto', target='tr').translate(info)
            speak(infotr)
        except:  # eğer türkçe söylediğimizde bulamadıysa söylediğimiz kelimeyi ingilizce çevirip aratıyor
            try:
                soru = txtvoice.replace('wikipedia', '')
                print(soru)
                soru_en = GoogleTranslator(source='auto', target='en').translate(soru)
                print(soru_en)
                info = wikipedia.summary(soru_en, 1)
                infotr = GoogleTranslator(source='auto', target='tr').translate(info)
                speak(infotr)
            except:  # en sonunda artık bulamadıysa olmadığını söylüyor
                speak("İngilizce wikipedia da" + soru + "hakkında bir bilgi yok")

    if txtvoice.startswith('çevir') or txtvoice.endswith('çevir'):  # Söylediğimiz kelimeyi türkçeye çeviriyor
        words = txtvoice.replace("çevir", "")
        translate = GoogleTranslator(source='auto', target='tr').translate(words)
        speak(translate)
    if txtvoice == 'şaka yapabiliyor musun' or txtvoice == 'şaka yap' or txtvoice == 'şaka yapar mısın':
        joke = pyjokes.get_joke()
        translate = GoogleTranslator(source='auto', target='tr').translate(joke)
        speak(translate)
    if txtvoice == 'sevgilin var mı' or txtvoice == 'ilişkin var mı' or txtvoice == 'evli misin' or txtvoice == 'bekar mısın':
        selection = ["Böyle bir soruyu ne için sordun", "wifiın ile ciddi bir ilişkim var",
                     "cevap vermeme hakkımı kullanıyorum, başka hangi konuda yardımcı olabilirim"]
        selection = random.choice(selection)
        speak(selection)
    if txtvoice == 'sevgilim olur musun' or txtvoice == 'sevgili olalım mı' or txtvoice == 'evlenelim mi' or txtvoice == 'takılmak ister misin' or txtvoice == 'benimle evlenir misin':
        selection = ["üzgünüm biz ayrı dünyaların insan ve programlarıyız",
                     "çok ani oldu daha birbirimizi tanımıyoruz bile",
                     "cevap vermeme hakkımı kullanıyorum, başka hangi konuda yardımcı olabilirim",
                     "üzgünüm ben seni arkadaşım olarak görüyorum", "bu soruyu sormamışın gibi devam edelim mi"]
        selection = random.choice(selection)
        speak(selection)
    if ("hava durumu") in txtvoice and ('wikipedia') not in txtvoice and ("google'da ara") not in txtvoice:
        provinces = ['adana', 'adıyaman', 'afyonkarahisar', 'ağrı', 'aksaray', 'amasya', 'ankara', 'antalya', 'ardahan', 'artvin', 'aydın', 'balıkesir', 'bartın', 'batman', 'bayburt', 'bilecik', 'bingöl', 'bitlis', 'bolu', 'burdur', 'bursa', 'çanakkale', 'çankırı', 'çorum', 'denizli', 'diyarbakır', 'düzce', 'edirne', 'elazığ', 'erzincan', 'erzurum', 'eskişehir', 'gaziantep', 'giresun', 'gümüşhane', 'hakkâri', 'hatay', 'iğdır', 'isparta', 'i̇stanbul', 'i̇zmir', 'kahramanmaraş', 'karabük', 'karaman', 'kars', 'kastamonu', 'kayseri', 'kilis', 'kırıkkale', 'kırklareli', 'kırşehir', 'kocaeli', 'konya', 'kütahya', 'malatya', 'manisa', 'mardin', 'mersin', 'muğla', 'muş', 'nevşehir', 'niğde', 'ordu', 'osmaniye', 'rize', 'sakarya', 'samsun', 'şanlıurfa', 'siirt', 'sinop', 'sivas', 'şırnak', 'tekirdağ', 'tokat', 'trabzon', 'tunceli', 'uşak', 'van', 'yalova', 'yozgat', 'zonguldak']

        try:
            if any((match := substring) in txtvoice for substring in provinces):
                sehir = match
                url = "https://www.ntvhava.com/{}-hava-durumu".format(sehir)
                request = requests.get(url)
                html_icerigi = request.content
                soup = BeautifulSoup(html_icerigi, "html.parser")
                gunduz_sicakliklari = soup.find_all("div", {
                    "class": "daily-report-tab-content-pane-item-box-bottom-degree-big"})  # sabah
                gece_sicakliklari = soup.find_all("div", {
                    "class": "daily-report-tab-content-pane-item-box-bottom-degree-small"})  # akşam
                durum = soup.find_all("div", {"class": "daily-report-tab-content-pane-item-text"})  # bulutlu - güneşli
                gunduz = []
                gece = []
                hava = []
                for x in gunduz_sicakliklari:
                    x = x.text
                    gunduz.append(x)
                for y in gece_sicakliklari:
                    y = y.text
                    gece.append(y)
                for z in durum:
                    z = z.text
                    hava.append(z)
                if ('yarın') not in txtvoice and ('yarınki') not in txtvoice and ('yarın için') not in txtvoice:
                    today = "{} için bugünkü hava raporları şöyle gunduz sıcaklığı {} gece sıcaklığı {} {}".format(sehir,gunduz[0],gece[0],hava[0])
                    speak(today)
                else:
                    tomorrow = "{} için yarınki hava raporları şöyle gunduz sıcaklığı {} gece sıcaklığı {} {}".format(sehir, gunduz[1], gece[1], hava[1])
                    speak(tomorrow)
            else:
                speak("böyle bir şehir bulamadım")
        except:
            speak("Hava durumunu öğrenmek için lütfen önce şehir sonra hava durumu sonra bugün veya yarın olduğunu belirtin")

    if txtvoice.startswith('sesi arttır') or txtvoice.startswith('sesi yükselt') or txtvoice.startswith('sesi aç') or txtvoice.endswith('sesini arttır') or txtvoice.endswith('sesini yükselt') or txtvoice.endswith('sesini aç'):
        for x in range(5): # sesi aç 10 ar
            pyautogui.press("volumeup")
    if txtvoice.startswith('sesi azalt') or txtvoice.startswith('sesi kıs') or txtvoice.startswith('sesi düşür') or txtvoice.endswith('sesini azalt') or txtvoice.endswith('sesini kıs') or txtvoice.endswith('sesini düşür'):
        for x in range(5): #sesi kıs 10 ar
            pyautogui.press("volumedown")
    if txtvoice.startswith('sesi kapat') or txtvoice.endswith('sesini kapat'): # mute
        pyautogui.press("volumemute")
    if txtvoice.startswith('parlaklığı') or txtvoice.startswith('parlaklık')and txtvoice.endswith('yap'): #parlaklık arttırıp azaltma
        sayi = ['0','1','2','3','4','5','6','7','8','9','10']
        try:
            if '10' in txtvoice:
                sbc.set_brightness(100)
            if 'bir' in txtvoice:
                sbc.set_brightness(10)
            elif any((match := substring) in txtvoice for substring in sayi):
                value_str = match
                value_int = int(value_str)
                print(value_int)
                sbc.set_brightness(value_int*10)
                print(sbc.get_brightness())
        except:
            speak('parlaklık değer aralığı 1 ile 10 arasındadır')
    if txtvoice.startswith('sesi') or txtvoice.startswith('ses') and txtvoice.endswith('yap'):
        #-0.1 = 100#-1.5 = 90 # -3.2 = 80 # -5.2 = 70 # -7.4 = 60 #-10.2 = 50 #-13.6 =40 # -18.0 =30 #-23.0 = 20 # -33 =10 #-60 = 0
        try:
            if '10' in txtvoice:
                volume.SetMasterVolumeLevel(-0.1, None)
            elif '0' in txtvoice:
                volume.SetMasterVolumeLevel(-60.0, None)
            if 'bir' in txtvoice:
                volume.SetMasterVolumeLevel(-33.0, None)
            if '9' in txtvoice:
                volume.SetMasterVolumeLevel(-1.5, None)
            if '8' in txtvoice:
                volume.SetMasterVolumeLevel(-3.2, None)
            if '7' in txtvoice:
                volume.SetMasterVolumeLevel(-5.2, None)
            if '6' in txtvoice:
                volume.SetMasterVolumeLevel(-7.4, None)
            if '5' in txtvoice:
                volume.SetMasterVolumeLevel(-10.2, None)
            if '4' in txtvoice:
                volume.SetMasterVolumeLevel(-13.6, None)
            if '3' in txtvoice:
                volume.SetMasterVolumeLevel(-18.0, None)
            if '2' in txtvoice:
                volume.SetMasterVolumeLevel(-23.0, None)

        except:
            speak('ses değer aralığı 1 ile 10 arasındadır')

def speak(string):
    tts = gTTS(text=string, lang='tr', slow=False)
    file = "answer.mp3"
    tts.save(file)
    playsound(file)
    os.remove(file)


# speak('Hoşgeldin')

def wake_up(wake):
    if 'adın ne' in wake or 'ismin ne' in wake:
        speak("Bir ada sahip değilim ama bana seslenmek için Carmen diyebilirsin.")
    if 'carmen' in wake:
        playsound("ding.mp3")
        wake = record()
        if wake != '':
            voice = wake.lower()
            print(wake.capitalize())
            response(voice)


# speak("Hava çok sıcak")
while True:
    wake = record()
    if wake != '':
        wake = wake.lower()
        print(wake.capitalize())
        wake_up(wake)
