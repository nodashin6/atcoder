####################
A - Probably English 
####################

****
問題
****

.. raw:: html

   <details>
   <summary>問題ページを開きます。</summary>
   <br>
   <iframe src="https://atcoder.jp/contests/abc295/tasks/abc295_a" height="600" width="100%">
   ここはコンテンツ内容など自由に記述可能
   </iframe>
   <br>
   </details>


****
解説
****

``for`` 文で文字列を読み取り, ``in`` で文字列の一致判定をします。

.. code-block:: python
   
    N = int(input())
    ans = 'No'
    for w in input().split():
        if w in {'and', 'not', 'that', 'the', 'you'}:
            ans = 'Yes'
    print(ans)