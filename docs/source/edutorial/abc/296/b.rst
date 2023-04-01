:author: nodashin
:date: 2023/04/01

###############
B - Chessboard
###############

************************************************************
`問題 <https://atcoder.jp/contests/abc296/tasks/abc296_b>`__
************************************************************

.. raw:: html

   <details>
   <summary>問題ページを開きます。</summary>
   <br>
   <iframe src="https://atcoder.jp/contests/abc296/tasks/abc296_b" height="600" width="100%">
   問題リンク
   </iframe>
   <br>
   </details>


****
解説
****

行番号が下から1, 2, ..., 8と割り振られています。
対して，プログラムは上の行から読み取って実行します。
こういう時は， ``reversed`` を使用すると良いです。

.. code-block:: python

    H, W = 8, 8
    for h in reversed(range(H)):
        S = input()
        for w in range(W):
            if S[w] == '*':
                print('abcdefgh'[w] + '12345678'[h])