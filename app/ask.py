"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors, types

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


#def ask(question: str, temperature: float = 0.7) -> str:
#    client = genai.Client(api_key=get_api_key())
#    response = client.models.generate_content(model=MODEL, contents=question, config = types.GenerateContentConfig(temperature=temperature))

 #   usage = response.usage_metadata
  #  if usage is not None:
   #     print(
    #        f"[トークン数] 入力: {usage.prompt_token_count}, "
     #       f"出力: {usage.candidates_token_count}"
        

    #return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="AIと対話する(チャットモード)")
    #parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--temp", type=float, default=0.7, help="生成の多様性(0.0 ~ 2.0)")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[温度(temp)] {args.temp}")
    print(f"--- チャットを開始します。終了するには'exit' と入力してください ---\n")

    client = genai.Client(api_key=get_api_key())

    chat = client.chats.create(
         model=MODEL,
         config=types.GenerateContentConfig(temperature=args.temp),
    )
    try:
        while True:
            user_input = input("あなた: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "終了"]:
                print("チャットを終了します。お疲れ様でした。")
                break
            try:
                response = chat.send_message(user_input)
                usage = response.usage_metadata
                if usage is not None:
                    print(
                       f"\n[AI]: {response.text}\n"
                       f"[トークン数] 入力: {usage.prompt_token_count}, 出力: {usage.candidates_token_count}\n"
                       f"----------------------------------------"
                    )
                else:
                    print(f"\n[AI]: {response.text}\n")

            except errors.ApiError as e:
                print(api_error_message(e.code, e.message))

    except (KeyboardInterrupt, EOFError):
           print("\nチャットを終了します。お疲れさまでした。")

if __name__ == "__main__":
    main()
