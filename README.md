# 2023Portfolios  
## プログラムの説明  
### saitama_neko  
#### 概要  
埼玉県のホームページで公開されている猫の譲渡情報をスクレイピングしてTwitterで定期的に情報をツイートします。  
Twitterアカウント(非公開)：@SaitamaCatInf https://twitter.com/SaitamaCatInf  

公開設定されたTwitterアカウントでの稼働に関しては、埼玉県のHPにおける"著作権、リンク等の規約"を満たさないため控えておりますが、
私的利用の範囲(非公開アカウント)にて稼働テスト済みです。
~~~
ツイート例：
【2023/xx/xx】
今日の埼玉県北部・西部地区の譲渡用猫情報
募集中 : x 匹
お見合い中 : x 匹
飼い主さん決定 : x 匹
~~~
※対象のページはこちら  
・[飼い主さん募集中です！（譲渡用猫情報／県北部・県西部）](https://www.pref.saitama.lg.jp/b0716/joutoseineko-n.html)  
・[飼い主さん募集中です！（譲渡用猫情報／県南部・県東部）](https://www.pref.saitama.lg.jp/b0716/joutoseineko-s.html)  
#### 使い方  
《注意》  
ご利用の際は、Twitterアカウントを非公開にする等、私的利用の範囲に限ってのご利用をお願いいたします。  
公開アカウントで実行した場合に起こった全てのことに関しては、責任を負いかねます。  

《前提条件》
1. PythonがPCにインストールされている
2. [Twitter Developer サイト](https://developer.twitter.com)からTwitterAPIを取得している
   ~~~
   ・bearer_token
   ・consumer_key
   ・consumer_secret
   ・access_token
   ・access_token_secret
   ~~~  
#### 
《実行手順》
1. RunSchedule.pyを実行  
2. 「Do you want to run a test tweet? (y/n)」と聞かれるので"y"を入力しEnterキー押下。
3. 「Please enter your key information」と聞かれるので順番に《前提条件》で準備したキー情報を入力し、Enterキー押下。  
   (成功していれば「Successfully tweeted!」が表示され、対象のアカウントでツイートが投稿される)
4. 「Runtime? [hh:mm] : 」と聞かれるので毎日の実行時間を"hh:mm"の形式で入力し、Enter押下。
5. 「Schedule in progress...」が表示され、スケジュール実行中となる。  
※項番3, 4は2回目以降不要になります。
## 使用言語
- Python
    - バージョン
        > Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32  
    - 使用ライブラリ一覧
        ~~~
        Package            Version  
        ------------------ -----------  
        beautifulsoup4     4.11.1     
        certifi            2022.9.24  
        charset-normalizer 2.1.1      
        idna               3.4        
        pip                22.3       
        requests           2.28.1     
        schedule           1.1.0      
        setuptools         65.5.0     
        soupsieve          2.3.2.post1  
        urllib3            1.26.12  
        ~~~
## 開発環境
- Visual Studio Code
    - バージョン
        > バージョン: 1.73.1 (user setup)  
        > コミット: 6261075646f055b99068d3688932416f2346dd3b  
        >  日付: 2022-11-09T04:27:29.066Z  
        > Electron: 19.0.17  
        > Chromium: 102.0.5005.167  
        > Node.js: 16.14.2  
        > V8: 10.2.154.15-electron.0  
        > OS: Windows_NT x64 10.0.19044  
        > Sandboxed: No  
- git
    - バージョン
        > git version 2.39.0.windows.1  
## OS
- Windows
    - バージョン  
        > エディション	Windows 10 Home  
        > バージョン	21H2  
        > インストール日	2021/01/15  
        > OS ビルド	19044.2251  