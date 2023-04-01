:author: nodashin
:date: 2023/04/01

###############
A - Alternately
###############

************************************************************
`問題 <https://atcoder.jp/contests/abc296/tasks/abc296_a>`__
************************************************************

.. raw:: html

   <details>
   <summary>問題ページを開きます。</summary>
   <br>
   <iframe src="https://atcoder.jp/contests/abc296/tasks/abc296_a" height="600" width="100%">
   問題リンク
   </iframe>
   <br>
   </details>


****
解説
****

``zip`` で取り出して，異なるか判定します。

.. code-block:: python

    N = int(input())
    S = input()
    ans = 'Yes'
    for si, sj in zip(S[:-1], S[1:]):
        if si == sj:
            ans = 'No'
    print(ans)


| 長さ :math:`N` の隣り合わないパターンを生成して一致を比較しても良いです。
| ``if "MFMFMF" in {"MFMFMF", "FMFMFM"} ?`` 
| のような判定になります。

.. code-block:: python

    N = int(input())
    S = input()
    uu = {('MF'*N)[:N], ('FM'*N)[:N]}
    ans = "Yes" if S in uu else "No"
    print(ans)