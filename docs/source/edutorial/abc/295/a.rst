:author: nodashin
:date: 2023/04/01

####################
A - Probably English 
####################

************************************************************
`問題 <https://atcoder.jp/contests/abc295/tasks/abc295_a>`__
************************************************************

.. raw:: html

   <details>
   <summary>問題ページを開きます。</summary>
   <br>
   <iframe src="https://atcoder.jp/contests/abc295/tasks/abc295_a" height="600" width="100%">
   問題リンク
   </iframe>
   <br>
   </details>


****
解説
****

読み取った文字列を ``for`` 文を使って順番に文字列の一致判定をします。
判定は ``in`` を用いると便利です。

.. code-block:: python
   
    N = int(input())
    ans = 'No'
    for w in input().split():
        if w in {'and', 'not', 'that', 'the', 'you'}:
            ans = 'Yes'
    print(ans)