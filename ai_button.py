# OpenAIのライブラリをインポート
import openai

# ラズパイのGPIOピンを制御するためのライブラリをインポート
import RPi.GPIO as GPIO
import datetime

# ピン24を入力ピンとして設定し、ボタンが押されたときにピンにHIGH（1）、押されていないときにはLOW（0）
GPIO.setmode(GPIO.BCM)
button_pin = 24
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

button_pressed_count = 0


def button_callback(channel):
    global button_pressed_count
    button_pressed_count += 1
    current_datetime = datetime.datetime.now()
    millisecond = current_datetime.microsecond // 1000  # ミリ秒を取得
    print("ミリ秒:", millisecond)
    print("ボタンが押された回数:", button_pressed_count)
    print("ボタンが押された日時:", current_datetime)

    # APIキーを設定
    openai.api_key = (
        "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"  # 前述で発行したAPIキーに置き換えてください
    )

    # GPT-3.5-turboモデルを使ってチャットの回答を生成するリクエストを作成
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "数字"
                + str(millisecond)
                + "にまつわる偉人を答えてください。そう答えた理由も50文字で教えてください。",
            },
        ],
    )

    # 返信のみを取得して変数に格納
    c_res = response["choices"][0]["message"]["content"]

    # 返信を出力
    print(c_res)


# ピン24がHIGH（1）になるとbutton_callback関数が呼び出される。バウンスタイムを100ミリ秒に設定して連続した変化を無視。
GPIO.add_event_detect(
    button_pin, GPIO.RISING, callback=button_callback, bouncetime=1000
)

try:
    while True:
        pass

except KeyboardInterrupt:
    pass

finally:
    GPIO.remove_event_detect(button_pin)
    GPIO.cleanup()
